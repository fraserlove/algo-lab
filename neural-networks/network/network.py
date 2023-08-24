import random
from network.value import Value

class Module:

    def zero_grad(self) -> None:
        for p in self.parameters():
            p.grad = 0

    def parameters(self) -> list:
        return []

class Neuron(Module):

    def __init__(self, nin: int) -> None:
        self.weights = [Value(random.uniform(-1, 1)) for _ in range(nin)]
        self.bias = Value(random.uniform(-1, 1))

    def __call__(self, x: list[int | float]) -> Value:
        act = sum(wi * xi for wi, xi in zip(self.weights, x)) + self.bias
        return act.tanh()
    
    def parameters(self) -> list[Value]:
        return self.weights + [self.bias]
    
    def __repr__(self):
        return f'Neuron({len(self.weights)})'
    
class Layer(Module):

    def __init__(self, nin: int, nout: int) -> None:
        self.neurons = [Neuron(nin) for _ in range(nout)]

    def __call__(self, x: list[int | float]) -> list[Neuron]:
        out = [neuron(x) for neuron in self.neurons]
        return out[0] if len(out) == 1 else out
    
    def parameters(self) -> list[Value]:
        return [param for neuron in self.neurons for param in neuron.parameters()]
    
    def __repr__(self):
        return f'Layer of [{", ".join(str(neuron) for neuron in self.neurons)}]'
    
class MLP(Module):

    def __init__(self, nin: int, nouts: list[int | float]) -> None:
        sizes = [nin] + nouts
        self.layers = [Layer(sizes[i], sizes[i+1]) for i in range(len(nouts))]

    def __call__(self, x: list[int | float]) -> list[Neuron]:
        for layer in self.layers:
            x = layer(x)
        return x
    
    def parameters(self) -> list[Value]:
        return [param for layer in self.layers for param in layer.parameters()]
    
    def __repr__(self):
        return f'MLP of [{", ".join(str(layer) for layer in self.layers)}]'