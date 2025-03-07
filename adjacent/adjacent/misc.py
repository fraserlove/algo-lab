import networkx as nx
from collections import deque

from .utils import smallest_int
from .traversal import bft

def greedy_colouring(G: nx.Graph, use_heuristic: bool = False) -> list[int]:
    '''Returns a colouring of G using greedy colouring.'''
    
    C = [0] * len(G)
    verts = G.nodes
    # If use_heuristic is true, sort vertices by descending order of degree, reduces colouring.
    if use_heuristic:
        # Sorting vertices in descending order of their degree.
        verts = [v[0] for v in sorted(G.degree, key = lambda x: x[1], reverse = True)]
    for v in verts:
        # Assigning the smallest colour which is not a colour of any neighbour, to v.
        C[v] = smallest_int([C[u] for u in G[v]])
    return C

def shortest_path(G: nx.Graph, u: int = 0, v: int = 0) -> list[int]:
    '''Returns the shortest path from u to v in a graph G.'''
    queue = deque([u])
    ancestor = [None] * len(G)
    ancestor[u] = -1
    
    # While there are still vertices in the queue.
    while queue:
        # Get the first vertex in the queue.
        x = queue.popleft()
        
        # Add all unvisited neighbours of current_vertex to the end of the queue.
        for y in G[x]:
            if ancestor[y] is None:
                ancestor[y] = x
                queue.append(y)
        
        # Check if the target vertex v has been reached.
        if x == v:
            # Trace back from v to u to obtain the path.
            path = []
            while x != -1:
                path.append(x)
                x = ancestor[x]
            return path[::-1]

def tree_diameter(T: nx.Graph) -> int:
    '''Returns the diameter of any tree T.'''
    if not nx.is_tree(T):
        raise ValueError('Input must be a tree.')
    
    # Find the farthest vertex v from any arbitray vertex.
    v = bft(T)[-1]
    # Find the farthest vertex w from v.
    w = bft(T, v)[-1]
    return len(shortest_path(T, v, w)) - 1
