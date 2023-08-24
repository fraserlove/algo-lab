import math
from typing import Self, Any

class Value:
    ''' Stores a singular value and its gradient. '''

    def __init__(self, data: Any, _children: set=(), _op: str='', label: str='') -> None:
        self.data = data
        self.grad = 0
        self._backward = lambda: None

        # Variables used for debugging
        self._prev = set(_children)
        self._op = _op
        self.label = label
    
    def __add__(self, other: Any) -> Self:
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward(): 
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
    
    def __mul__(self, other: Any) -> Self:
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    
    def __pow__(self, other: Any) -> Self:
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data ** other.data, (self, ), f'**{other.data}')

        def _backward():
            self.grad += other.data * self.data**(other.data-1) * out.grad
        out._backward = _backward
        return out
    
    def exp(self) -> Self:
        out = Value(math.exp(self.data), (self, ), 'exp')

        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward
        return out
    
    def relu(self) -> Self:
        out = Value(0 if self.data < 0 else self.data, (self, ), 'relu')

        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out
    
    def tanh(self) -> Self:
        tanh = (math.exp(2 * self.data) - 1) / (math.exp(2 * self.data) + 1)
        out = Value(tanh, (self, ), 'tanh')

        def _backward():
            self.grad += (1 - tanh**2) * out.grad
        out._backward = _backward
        return out
     
    def backward(self) -> None:
        # Topologically order all the nodes in the graph.
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # Apply the chain rule to each node to get its gradient.
        self.grad = 1
        for node in reversed(topo):
            node._backward()

    def __neg__(self) -> Self:
        # -self
        return self * -1
    
    def __sub__(self, other: Any) -> Self:
        return self + (-other)
    
    def __truediv__(self, other: Any) -> Self:
        return self * other**-1

    def __radd__(self, other: Any) -> Self:
        return self + other
    
    def __rsub__(self, other: Any) -> Self:
        return (-self) + other
    
    def __rmul__(self, other: Any) -> Self:
        return self * other
    
    def __rtruediv__(self, other: Any) -> Self:
        return self**-1 * other

    def __repr__(self) -> str:
        return f'Value(data={self.data})'