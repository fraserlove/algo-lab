# Algorithmic Trading
A collection of algorithmic trading scripts.

## Installation and Usage
These scripts use the Alpaca trading API with the `keyring` package to import Alpaca API keys from the Apple Keychain on macOS. Please make sure you have generated your Alapca API keys and stored them in the Apple Keychain with service name `'alpaca'` and account names `'secret_key'` and `'api_key'`. This can be used for both live and paper trading. The code below can be used to add the correct API keys to your Apple Keychain. Replace `<API_KEY>` and `<SECRET_KEY>` with your generated keys. If you want to use paper trading, you can also replace  `<API_KEY_PAPER>` and `<SECRET_KEY_PAPER>` with your corresponding paper keys.

```python
import keyring

# Live Trading API.
keyring.set_password('alpaca', 'api_key', '<API_KEY>')
keyring.set_password('alpaca', 'secret_key', '<SECRET_KEY>')

# Paper Trading API.
keyring.set_password('alpaca', 'api_key_paper', '<API_KEY_PAPER>')
keyring.set_password('alpaca', 'secret_key_paper', '<SECRET_KEY_PAPER>')
```
Setup your environment and install the required dependencies as follows:

1. **Clone the Repository:**
```bash
git clone https://github.com/fraserlove/pylab.git
cd pylab/trading
```

2. **Create a Python Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Install Dependencies via PIP:**

```bash
pip install -r requirements.txt
```

4. **Run Any Strategy:**

Ensure you pass in the parameters for the strategy you want to change as command line arguments. These can be found by entering `-h` or `--help` after the entering the Python file name of strategy you want to run. An example is given below.
``` bash
python senate_long/strategy.py --live --position_length 60 --rebalance_frequency 7
```