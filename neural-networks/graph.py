import graphviz

from value import Value

'''
Important: The graphviz package must be installed on the users system before use. 

    brew install graphviz
    sudo apt install graphviz

'''

def trace(root: Value) -> tuple[set, set]:
    ''' Builds a set of vertices and edges in a connected graph of Value objects. '''

    vertices, edges = set(), set()
    def build(v):
        if v not in vertices:
            vertices.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)

    build(root)
    return vertices, edges


def draw_graph(root: Value) -> graphviz.Digraph:
    ''' Draws a graph comprised of Value objects with corresponding gradients. '''
    
    graph = graphviz.Digraph(format='svg', graph_attr={'rankdir' : 'LR'}) # Draw left to right.
    vertices, edges = trace(root)

    for v in vertices:
        uid = str(id(v))
        # For any value in the graph, create a rectangular node for it.
        graph.node(name=uid, label=f'{{ {v.label} | data {v.data:.2f} | grad {v.grad:.2f} }}', shape='record')
        if v._op:
            # If this value is a result of some operation, create a circular node for it.
            graph.node(name=uid + v._op, label=v._op)
            graph.edge(uid + v._op, uid)

    for u, v in edges:
        # Connect n1 to the op node of n2.
        graph.edge(str(id(u)), str(id(v)) + v._op)

    return graph