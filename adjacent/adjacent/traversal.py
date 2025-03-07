import networkx as nx
from collections import deque

def dft(G: nx.Graph, u: int = 0) -> list[int]:
    '''Performs depth first traversal on G, starting at vertex u (default 0), and returns the set of seen vertices.'''
    stack = [u]
    seen = []

    while stack:
        v = stack.pop()
        if v not in seen:
            seen.append(v)
            stack.extend(u for u in G[v])
    return seen

def bft(G: nx.Graph, u: int = 0) -> list[int]:
    '''Performs breadth first traversal of G, starting at vertex u (default 0), and returns the set of seen vertices.'''
    queue = deque([u])
    seen = []

    while queue:
        v = queue.popleft()
        if v not in seen:
            seen.append(v)
            queue.extend(G[v])
    return seen