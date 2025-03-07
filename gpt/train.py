import os
import torch
import torch.nn as nn

from gpt import GPTLanguageModel, GPTConfig, GPTTokeniser

block_size = 2048 # Maximum context length for predictions
batch_size = 128 # Sequences to process in parallel
max_iters = 10000 # Iterations to train the model
eval_iters = 100 # Iterations to average the loss over
lr = 1e-5 # Learning rate

device = 'cuda' if torch.cuda.is_available() else 'cpu' # Use GPU if available
device_name = f' ({torch.cuda.get_device_name(0)})' if device == 'cuda' else ''
print(f'Device: {device}{device_name}')

script_dir = os.path.dirname(os.path.abspath(__file__))
# or train the model with
# tokeniser = GPTTokeniser(os.path.join(script_dir, 'data/tinyshakespeare.txt'), vocab_size=1000, verbose=True)
tokeniser = GPTTokeniser(os.path.join(script_dir, 'data/tinyshakespeare.tkn'))

with open(os.path.join(script_dir, 'data/tinyshakespeare.txt'), 'r', encoding='utf-8') as f:
    text = f.read()

# Train and validation splits
data = torch.tensor(tokeniser.encode(text, 'all'), dtype=torch.long)
split = int(len(data) * 0.9) # 90% train, 10% val
train_data, val_data = data[:split], data[split:]

def get_batch(split: str) -> tuple[torch.Tensor, torch.Tensor]:
    """Generate a random batch of context and target sequences."""
    data = train_data if split == 'train' else val_data
    # Randomly sample batch_size number of starting indices
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y

@torch.no_grad()
def estimate_loss(model: nn.Module) -> dict[str, float]:
    """Estimate the mean loss of the model on the train and val sets."""
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for i in range(eval_iters):
            xb, yb = get_batch(split)
            _, loss = model(xb, yb)
            losses[i] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out 

config = GPTConfig(
    block_size = block_size,
    vocab_size = tokeniser.vocab_size(),
    n_layer = 12,
    n_head = 12,
    n_embd = 768
)

model = GPTLanguageModel(config).to(device)

total_params = sum(param.numel() for param in model.parameters())
print(f'Model parameters: {total_params}')

# Training the model
optimiser = torch.optim.AdamW(model.parameters(), lr=lr)

for i in range(max_iters):
    
    if i % (max_iters // 10) == 0 or i == max_iters - 1:
        losses = estimate_loss(model)
        print(f'Iteration {i:2d} | Train Loss: {losses["train"]:.4f} | Val Loss: {losses["val"]:.4f}')

    # Get a batch of context and target sequences
    xb, yb = get_batch('train')

    # Compute the gradients and update the weights
    _, loss = model(xb, yb) # Forward pass
    optimiser.zero_grad(set_to_none=True)
    loss.backward()
    optimiser.step()

# Generate
context = torch.zeros((1, 1), dtype=torch.long, device=device)
with open('output.txt', 'w') as f:
    f.write(tokeniser.decode(model.generate(context, max_tokens=512)[0].tolist()))