"""
GPT (byte-level) Byte Pair Encoding (BPE) Tokenizer.
Handles special tokens and the regular expression splitting pattern.

Based off the GPT-2 tokeniser:
https://github.com/openai/gpt-2/blob/master/src/encoder.py
"""

import regex as re
from gpt.tokeniser.base import Tokeniser, consecutive_pairs, replace_pair

# Regular expression splitting patterns for GPT-2 and GPT-4.
# See https://github.com/openai/tiktoken/blob/main/tiktoken_ext/openai_public.py
GPT2_SPLIT_PATTERN = r"'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"
GPT4_SPLIT_PATTERN = r"'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"

GPT_4_TOKENS = { '<|endoftext|>': 100257, '<|fim_prefix|>': 100258, '<|fim_middle|>': 100259, '<|fim_suffix|>': 100260, '<|endofprompt|>': 100276 }

class GPTTokeniser(Tokeniser):
    """GPT BPE Tokeniser."""

    def __init__(self, file_name: str = None, pattern: str = None, special_tokens: dict[str, int] = None, vocab_size: int = None, verbose: bool = False):
        super().__init__()

        # Default to GPT-4 pattern and special tokens
        self.pattern = GPT4_SPLIT_PATTERN if pattern is None else pattern
        self.special_tokens = GPT_4_TOKENS if special_tokens is None else special_tokens
        
        self.regex = re.compile(self.pattern) # Compiled regex pattern

        if file_name:
            if file_name.endswith('.tkn'):
                print('Loading tokeniser from file...')
                self.load(file_name)
            else:
                assert vocab_size is not None
                print('Training tokeniser...')
                self.train(file_name, vocab_size=vocab_size, verbose=verbose)

    def train(self, file_name: str, vocab_size: int, verbose: bool = False) -> None:
        """Train on a text and build a vocabulary of size vocab_size."""
        assert vocab_size >= 256
        n_merges = vocab_size - 256
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
        text_chunks = re.findall(self.regex, text) # Split the text into chunks
        tokens = [list(text_chunk.encode('utf-8')) for text_chunk in text_chunks]
        merges = {} # Dictionary to store the merges
        vocab = {i: bytes([i]) for i in range(256)}

        # Merge the most frequent pair n_merges times to create new tokens
        for i in range(n_merges):
            # Find the most frequent consecutive pair of tokens
            freq_pairs = {}
            for token_chunk in tokens:
                consecutive_pairs(token_chunk, freq_pairs)
            max_pair = max(freq_pairs, key=freq_pairs.get)
            # Create a new token and assign it to an unused integer
            new_token = 256 + i
            # Replace the pair with the new token in each chunk
            tokens = [replace_pair(token_chunk, max_pair, new_token) for token_chunk in tokens]
            # Store the merge and the new token in the vocab
            merges[max_pair] = new_token
            vocab[new_token] = vocab[max_pair[0]] + vocab[max_pair[1]]
            if verbose:
                print(f'{i+1}/{n_merges}: {max_pair} -> {new_token}')

        self.merges = merges
        self.vocab = vocab
        self.save(file_name.replace('.txt', '.tkn'))
        
    def _encode_chunk(self, text_chunk: str) -> list[int]:
        """Encode a text chunk into a sequence of tokens."""
        token_chunk = list(text_chunk.encode('utf-8'))
        while len(token_chunk) > 1:
            freq_pairs = consecutive_pairs(token_chunk)
            # Find the most frequent consecutive pair that has been merged
            most_freq = min(freq_pairs, key=lambda pair: self.merges.get(pair, float('inf')))
            # If there are no more merges avaliable the keys all be inf and most_freq will be the first pair
            if most_freq not in self.merges:
                break # No more merges to apply
            # Merge the pair into a new token
            new_token = self.merges[most_freq]
            token_chunk = replace_pair(token_chunk, most_freq, new_token)
        return token_chunk
    
    def encode_ordinary(self, text: str) -> list[int]:
        """Encode text, ignoring any special tokens."""
        text_chunks = re.findall(self.regex, text) # Split the text into chunks
        # Encode each chunk separetely and concatenate the tokens
        tokens = []
        for text_chunk in text_chunks:
            token_chunk = self._encode_chunk(text_chunk)
            tokens.extend(token_chunk)
        return tokens

    def encode(self, text: str, allowed_special: str = 'none_raise') -> list[int]:
        """
        Encode text, handling special tokens. allowed_special can be 'all'|'none'|'none_raise'
        or a custom set of special tokens. If 'none_raise', then an error is raised if any
        special token is encountered in text.
        """
        special = None
        if allowed_special == 'all':
            special = self.special_tokens
        elif allowed_special == 'none':
            special = {}
        elif allowed_special == 'none_raise':
            special = {}
            assert all(token not in text for token in self.special_tokens)
        elif isinstance(allowed_special, set):
            special = {k: v for k, v in self.special_tokens.items() if k in allowed_special}
        else:
            raise ValueError(f'Invalid value for allowed_special: {allowed_special}')
        
        if not special:
            return self.encode_ordinary(text) # No special tokens to handle
        # Split the text into chunks and special tokens
        special_pattern = f'({"|".join(re.escape(k) for k in special)})'
        special_chunks = re.split(special_pattern, text)
        tokens = []
        # Encode each chunk and special token separetely and concatenate the tokens
        for part in special_chunks:
            if part in special:
                tokens.append(special[part]) # Encode the special token as an integer
            else:
                tokens.extend(self.encode_ordinary(part)) # Encode the chunk normally
        return tokens
    
    def decode(self, tokens: list[int]) -> str:
        """Decode a sequence of tokens into a string."""
        byte_chunk = []
        # Invert the special tokens for quick lookup
        inv_special_tokens = {v: k for k, v in self.special_tokens.items()}
        # Decode each token into a byte chunk and concatenate them
        for token in tokens:
            if token in self.vocab:
                byte_chunk.append(self.vocab[token])
            elif token in inv_special_tokens: # Token is a special token
                byte_chunk.append(inv_special_tokens[token].encode('utf-8'))
            else:
                raise ValueError(f'Invalid token: {token}')
        bytes_ = b''.join(byte_chunk)
        text = bytes_.decode('utf-8', errors='replace') # Replace unknown characters
        return text