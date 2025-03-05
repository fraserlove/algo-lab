"""
GPT Model.

Based off the GPT-2 model:
https://github.com/openai/gpt-2/blob/master/src/model.py
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class GPTConfig:
    block_size: int = 256 # Maximum context length for predictions
    vocab_size: int = 256 # Number of unique tokens
    n_layer: int = 4 # Number of transformer blocks
    n_head: int = 4 # Self-attention heads
    n_embd: int = 128 # Embedding dimensions
    dropout: float = 0.2 # Dropout probability

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

# B - batch size, T - block size (time step), C - embedding dimension, C' - vocab size, H - head size   

class Head(nn.Module):
    """Single head of self-attention."""
    
    def __init__(self, config: GPTConfig):
        super().__init__()
        head_size = config.n_embd // config.n_head
        self.key = nn.Linear(config.n_embd, head_size, bias=False) # (B,T,C) -> (B,T,H)
        self.query = nn.Linear(config.n_embd, head_size, bias=False) # (B,T,C) -> (B,T,H)
        self.value = nn.Linear(config.n_embd, head_size, bias=False) # (B,T,C) -> (B,T,H)
        self.register_buffer('tril', torch.tril(torch.ones(config.block_size, config.block_size)))
        self.Dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)
        # Compute attention scores ('affinities')
        W = q @ k.transpose(-2, -1) * (k.shape[-1] ** -0.5) # (B,T,H) @ (B,H,T) -> (B,T,T)
        W = W.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        W = F.softmax(W, dim=-1)
        W = self.Dropout(W)
        # Perform the attention-weighted sum
        v = self.value(x)
        out = W @ v # (B,T,T) @ (B,T,H) -> (B,T,H)
        return out

class MultiHead(nn.Module):
    """Multi-head self-attention."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        head_size = config.n_embd // config.n_head
        self.heads = nn.ModuleList([Head(config) for _ in range(config.n_head)])
        self.proj = nn.Linear(head_size * config.n_head, config.n_embd)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out
    
class FeedForward(nn.Module):
    """Single non-linear feed-forward layer."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.ReLU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
            nn.Dropout(config.dropout)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
    
class Block(nn.Module):
    """Transformer block. A multi-head self-attention layer and a feed-forward layer."""
    
    def __init__(self, config: GPTConfig):
        super().__init__()
        self.sa_heads = MultiHead(config)
        self.feed_forward = FeedForward(config)
        self.layer_norm1 = nn.LayerNorm(config.n_embd)
        self.layer_norm2 = nn.LayerNorm(config.n_embd)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Apply self-attention and feed-forward layers with residual connections and layer normalisation.
        x = self.layer_norm1(self.sa_heads(x) + x)
        x = self.layer_norm2(self.feed_forward(x) + x)
        return x

class GPTLanguageModel(nn.Module):
    """GPT language model. Consists of an embedding layer, transformer blocks, and a linear head."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.config = config
        self.token_embd_table = nn.Embedding(config.vocab_size, config.n_embd) # (B,T) -> (B,T,C)
        self.position_embd_table = nn.Embedding(config.block_size, config.n_embd) # (T) -> (T,C)
        self.blocks = nn.Sequential(*[Block(config) for _ in range(config.n_layer)])
        self.layer_norm = nn.LayerNorm(config.n_embd)
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size) # (B,T,C) -> (B,T,C')

    def forward(self, x: torch.Tensor, y: torch.Tensor = None) -> tuple[torch.Tensor, torch.Tensor]:
        B, T = x.shape
        token_embd = self.token_embd_table(x)
        position_embd = self.position_embd_table(torch.arange(T, device=x.device))
        embed = token_embd + position_embd
        embed = self.blocks(embed)
        embed = self.layer_norm(embed)
        logits = self.lm_head(embed)

        if y is None:
            loss = None
        else:
            B, T, C = logits.shape
            # Flatten batch and sequence dimensions to use F.cross_entropy
            logits = logits.view(B*T, C)
            y = y.view(B*T)
            loss = F.cross_entropy(logits, y)
        return logits, loss

    def generate(self, x: torch.Tensor, max_tokens: int) -> torch.Tensor:
        for _ in range(max_tokens):
            # Crop the sequence context to the last block_size tokens
            x_last = x[:, -self.config.block_size:]
            # Get the previous predictions
            logits, _ = self(x_last)
            # Keep only the last prediction
            logits = logits[:, -1, :] # (B,C)
            # Apply softmax to convert logits into probabilities
            probs = F.softmax(logits, dim=-1) # (B,C)
            # Sample from the probability distribution
            x_next = torch.multinomial(probs, num_samples=1) # (B,1)
            # Concatenate the new prediction to the previous context
            x = torch.cat([x, x_next], dim=1) # (B,T+1)
        return x