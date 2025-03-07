# Adjacent

A library for graph algorithms built on top of NetworkX.

## Installation

Before installing the package, consider using a virtual environment for the installation to avoid conflicts with other Python packages.
```sh
python -m venv .venv
source .venv/bin/activate
```

Clone the repository and install the package:
```sh
git clone https://github.com/fraserlove/adjacent.git
cd adjacent
pip install .
```

## Usage
Import the functions you need from the `adjacent` module. For example:

```python
import networkx as nx

from adjacent import tree_diameter, hamiltonian_cycle, is_eulerian, satisfies_eulers_theorem

G = nx.Graph([{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 1}, {1, 3}, {0, 3}])
assert is_eulerian(G)
assert satisfies_eulers_theorem(G)
```
