# AutoDiff

A reverse-mode (backpropagation) automatic differentiation library built over a Direct Acyclic Graph (DAG) of operations with a small feedforward neural network library built on top of it. The library is built from the ground up, and is built with a PyTorch-like API. Only scalar operations are supported, hence the library is not optimised for performance via GPU acceleration with tensor operations.

In order to visualise and debug backpropagation via automatically generated DAGs, `graphviz` must be installed on your system.

## Installation

Before installing the package, consider using a virtual environment for the installation to avoid conflicts with other Python packages.
```sh
python -m venv .venv
source .venv/bin/activate
```

Clone the repository and install the package:
```sh
git clone https://github.com/fraserlove/pylab.git
cd pylab/deep-learning/autodiff
pip install .
```

## Usage

Import the `Value` and `MLP` classes from the `autodiff` module.

```python
from autodiff import Value, MLP
```

From there, you can use the `Value` class to create a new value, and the `MLP` class to create a new feedforward neural network.

```python
a = Value(1.0)
b = Value(2.0)
c = a + b
c.backward()
```

```python
n = MLP(2, [4, 4, 1])
```

Further examples can be found in the `examples` directory.