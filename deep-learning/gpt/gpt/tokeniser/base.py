"""
Base Tokeniser class and a few utility functions.
Contains load/save methods for the tokeniser.
"""

def consecutive_pairs(ints: list[int], freq: dict[tuple[int, int], int] = None) -> dict[tuple[int, int], int]:
    """
    Generate a dictionary of the frequencies of consecutive integers in the list.
    Example: [1, 2, 3, 1, 2] -> {(1, 2): 2, (2, 3): 1, (3, 1): 1}
    Optionally update an existing frequency dictionary.
    """
    freq = {} if freq is None else freq
    for pair in zip(ints, ints[1:]):
        freq[pair] = freq.get(pair, 0) + 1
    return freq

def replace_pair(ints: list[int], pair: tuple[int, int], new_int: int) -> list[int]:
    """
    Replace all consecutive occurrences of a pair of integers in the list with a new integer.
    Example: ints=[1, 2, 3, 1, 2], pair=(1, 2), new_int=4 -> [4, 3, 4]
    """
    new_ints = []
    i = 0
    while i < len(ints):
        # If not at the last position AND the pair matches, replace it
        if (i < len(ints) - 1) and ints[i:i+2] == list(pair):
            new_ints.append(new_int)
            i += 2
        else:
            new_ints.append(ints[i])
            i += 1
    return new_ints

class Tokeniser:
    """Base Tokeniser."""

    def __init__(self):
        self.merges = {} # Merges of tokens (tuple[int, int] -> int)
        self.pattern = "" # Pattern for tokenisation
        self.special_tokens = {} # Special tokens to be added to the vocab (str -> int)
        self.vocab = self._build_vocab() # Vocabulary of tokens (str -> int)

    def train(self, file_name: str, vocab_size: int, verbose: bool = False) -> None:
        """Train on a text and build a vocabulary of size vocab_size."""
        raise NotImplementedError

    def encode(self, text: str) -> list[int]:
        """Encode a string into a sequence of tokens."""
        raise NotImplementedError

    def decode(self, tokens: list[int]) -> str:
        """Decode a sequence of tokens into a string."""
        raise NotImplementedError

    def _build_vocab(self) -> dict[str, int]:
        """Build the vocabulary from the merges and special tokens."""
        vocab = {i: bytes([i]) for i in range(256)} # Initialise with single bytes as tokens
        for (token_0, token_1), new_token in self.merges.items():
            vocab[new_token] = vocab[token_0] + vocab[token_1]
        for special, idx in self.special_tokens.items():
            vocab[idx] = special.encode("utf-8")
        return vocab
    
    def save(self, file_name: str) -> None:
        """Save the tokeniser to a file."""
        # Write the pattern, special tokens, and merges to the file
        with open(file_name, 'w') as f:
            f.write(f'{self.pattern}\n')
            f.write(f'{len(self.special_tokens)}\n')
            for special, token in self.special_tokens.items():
                f.write(f'{special} {token}\n')
            for token_1, token_2 in self.merges:
                f.write(f'{token_1} {token_2}\n')

    def load(self, file_name: str) -> None:
        """Load the tokeniser from a file."""
        assert file_name.endswith('.tkn')
        merges = {}
        special_tokens = {}
        new_token = 256
        # Read the pattern, special tokens, and merges from the file
        with open(file_name, 'r', encoding='utf-8') as f:
            self.pattern = f.readline().strip()
            n_special = int(f.readline().strip())
            for _ in range(n_special):
                special, token = f.readline().strip().split()
                special_tokens[special] = int(token)
            for line in f:
                token_1, token_2 = map(int, line.split())
                merges[(token_1, token_2)] = new_token
                new_token += 1
        self.merges = merges
        self.special_tokens = special_tokens
        self.vocab = self._build_vocab()

    def vocab_size(self) -> int:
        """Return the size of the vocabulary."""
        return len(self.vocab)