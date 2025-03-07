import math
import graphviz
from typing import Any, Self

class Value:
    """Represents a node in a computation graph. Each node has a value and a gradient."""

    def __init__(self, v: Any, _prev: set[tuple[Self, float]] = None, _op: str = '', label: str = ''):
        self.v = v
        self.dv = 0
        self._prev = _prev if _prev is not None else set() # Previous nodes and their gradients
        self._op = _op
        self.label = label

    def __repr__(self) -> str:
        return f'Value({self.v}, dv={self.dv})'

    def __add__(self, other: Any) -> Self:
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.v + other.v, _prev=[(self, 1), (other, 1)], _op='+')

    def __mul__(self, other: Any) -> Self:
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.v * other.v, _prev=[(self, other.v), (other, self.v)], _op='*')

    def __pow__(self, other: Any) -> Self:
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.v ** other.v, _prev=[(self, other.v * self.v**(other.v - 1))], _op=f'**{other.v}')

    def exp(self) -> Self:
        return Value(math.exp(self.v), _prev=[(self, math.exp(self.v))], _op='exp')

    def log(self) -> Self:
        return Value(math.log(self.v), _prev=[(self, 1 / self.v)], _op='log')

    def sin(self) -> Self:
        return Value(math.sin(self.v), _prev=[(self, math.cos(self.v))], _op='sin')

    def cos(self) -> Self:
        return Value(math.cos(self.v), _prev=[(self, -math.sin(self.v))], _op='cos')
    
    def relu(self) -> Self:
        return Value(max(0, self.v), _prev=[(self, int(self.v > 0))], _op='relu')
    
    def tanh(self) -> Self:
        tanh = (math.exp(2 * self.v) - 1) / (math.exp(2 * self.v) + 1)
        return Value(tanh, _prev=[(self, 1 - tanh**2)], _op='tanh')

    def __neg__(self) -> Self:
        return self * -1

    def __sub__(self, other: Any) -> Self:
        return self + (-other)

    def __truediv__(self, other: Any) -> Self:
        return self * other**-1

    def __radd__(self, other: Any) -> Self:
        return self + other

    def __rsub__(self, other: Any) -> Self:
        return -self + other

    def __rmul__(self, other: Any) -> Self:
        return self * other

    def __rtruediv__(self, other: Any) -> Self:
        return self**-1 * other
    
    def _build(self) -> tuple[list[Self], set[Self], set[tuple[Self, Self]]]:
        """Builds a computation graph starting from this node."""

        topo = [] # Nodes in reverse topological order
        vertices, edges = set(), set()
        
        def dfs(v):
            if v not in vertices:
                vertices.add(v)
                for prev, _ in v._prev:
                    edges.add((prev, v))
                    dfs(prev)
                topo.append(v)
        
        dfs(self)
        topo = reversed(topo)
        return topo, vertices, edges

    def backward(self) -> None:
        """Backpropagate the gradient through the graph."""

        topo, _, _ = self._build()

        self.dv = 1 # Final node has a gradient of 1
        # Apply the chain rule to each node to get its gradient
        for node in topo:
            for prev, dv in node._prev:
                prev.dv += dv * node.dv # Chain rule

    def graph(self) -> graphviz.Digraph:
        """Returns a graph comprised of Value objects with values and gradients."""

        graph = graphviz.Digraph(format='svg', graph_attr={'rankdir' : 'LR'}) # Draw left to right.
        _, vertices, edges = self._build()

        for v in vertices:
            uid = str(id(v))
            # For any value in the graph, create a rectangular node for it.
            graph.node(name=uid, label=f'{{ {v.label} | data {v.v:.2f} | grad {v.dv:.2f} }}', shape='record')
            if v._op:
                # If this value is a result of some operation, create a circular node for it
                graph.node(name=uid + v._op, label=v._op)
                graph.edge(uid + v._op, uid)

        for u, v in edges:
            # Connect n1 to the op node of n2
            graph.edge(str(id(u)), str(id(v)) + v._op)

        return graph