
import random
from .value import Value

class Module:
    """Base class for all neural network modules."""

    def zero_grad(self) -> None:
        """Zero the gradients of all parameters."""
        for p in self.parameters():
            p.grad = 0

    def parameters(self) -> list:
        """Return a list of all parameters of the module."""
        return []

class Neuron(Module):
    """Neuron in a neural network."""

    def __init__(self, nin: int):
        self.weights = [Value(random.uniform(-1, 1)) for _ in range(nin)]
        self.bias = Value(random.uniform(-1, 1))

    def __call__(self, x: list[int | float]) -> Value:
        act = sum(wi * xi for wi, xi in zip(self.weights, x)) + self.bias
        return act.tanh()
    
    def __repr__(self) -> str:
        return f'Neuron({len(self.weights)})'
    
    def parameters(self) -> list[Value]:
        return self.weights + [self.bias]
    
class Layer(Module):
    """Layer in a neural network."""

    def __init__(self, nin: int, nout: int):
        self.neurons = [Neuron(nin) for _ in range(nout)]

    def __call__(self, x: list[int | float]) -> list[Neuron]:
        out = [neuron(x) for neuron in self.neurons]
        return out[0] if len(out) == 1 else out
    
    def __repr__(self) -> str:
        return f'Layer of [{", ".join(str(neuron) for neuron in self.neurons)}]'
    
    def parameters(self) -> list[Value]:
        return [param for neuron in self.neurons for param in neuron.parameters()]
    
class MLP(Module):
    """Multi-layer perceptron."""

    def __init__(self, nin: int, nouts: list[int]):
        sizes = [nin] + nouts
        self.layers = [Layer(sizes[i], sizes[i+1]) for i in range(len(nouts))]

    def __call__(self, x: list[float]) -> list[Neuron]:
        for layer in self.layers:
            x = layer(x)
        return x
    
    def __repr__(self) -> str:
        return f'MLP of [{", ".join(str(layer) for layer in self.layers)}]'
    
    def parameters(self) -> list[Value]:
        return [param for layer in self.layers for param in layer.parameters()]
