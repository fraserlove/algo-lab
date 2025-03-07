# GPT

A small PyTorch implementation of a GPT model (Decoder-only Transformer), with a focus on simplicity and readability. This model was built following [nanoGPT](https://github.com/karpathy/nanoGPT) by Andrej Karpathy.

The model is trained on the [Tiny Shakespeare](https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt) dataset. This repository includes a tokeniser module containing two tokenisers `BasicTokeniser` and `GPTTokeniser` which follow the Byte Pair Encoding (BPE) algorithm. Note that `BasicTokeniser` is a basic tokeniser that does not handle any special tokens or the regular expression splitting pattern. `GPTTokeniser` is a more advanced tokeniser that can handle special tokens and the regular expression splitting pattern as in the [GPT-2](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) paper. Both tokenisers have the ability to save and load a tokeniser model from `.tkn` files. The tokeniser can be trained from scratch on a text file or loaded from a `.tkn` file. If the tokeniser is loaded from a `.tkn` file, the tokeniser will not be trained.

## Installation

Before installing the package, consider using a virtual environment for the installation to avoid conflicts with other Python packages.
```sh
python -m venv .venv
source .venv/bin/activate
```

Clone the repository and install the package:
```sh
git clone https://github.com/fraserlove/pylab.git
cd pylab/deep-learning/gpt
pip install .
```

## Usage

Import the `GPTLanguageModel`, `GPTTokeniser` and `GPTConfig` classes from the `gpt` module.

```python
from gpt import GPTLanguageModel, GPTTokeniser, GPTConfig
```

From there, you can use the `GPTLanguageModel` class to create a model, and the `GPTTokeniser` class to tokenise and detokenise text.

```python
tokeniser = GPTTokeniser('data/tinyshakespeare.tkn')

config = GPTConfig(
    block_size=2048,
    vocab_size=tokeniser.vocab_size(),
    n_layer=12,
    n_head=12,
    n_embd=768
)

model = GPTLanguageModel(config).to(device)
```

An example training and inference script is provided in `train.py`. At the end of training a file called `output.txt` containing the generated text will be created in the root directory.
