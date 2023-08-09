'''
Greedy Colouring Algorithm for Graph Colouring.

Created 12/03/23
Developed by Fraser Love
'''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def smallest_int(arr):
    '''Returns the smallest positive integer, i, not in arr.
    
    Keyword arguments:
    arr -- list of integers
    '''
    i = 1
    while True:
        if i not in arr:
            return i
        i += 1
        
def greedy_colouring(G, use_heuristic = False):
    '''Returns a colouring of G using greedy colouring.
    
    Keyword arguments:
    G -- nx.Graph (with vertices {0, 1, ..., n - 1})
    use_heuristic -- boolean, if true vertices are sorted by descending order of degree, reduces colouring
    '''
    C = [0] * len(G)
    verts = G.nodes
    if use_heuristic:
        # Sorting vertices in descending order of their degree.
        verts = [v[0] for v in sorted(G.degree, key = lambda x: x[1], reverse = True)]
    for v in verts:
        # Assigning the smallest colour which is not a colour of any neighbour, to v.
        C[v] = smallest_int([C[u] for u in G[v]])
    return C

n = 1000

x = np.zeros(n, dtype=int)
for i in range(n):
    G = nx.erdos_renyi_graph(100, 0.2)
    x[i] = max(greedy_colouring(G, True)) - max(greedy_colouring(G, False))

fig, ax = plt.subplots(figsize=(8, 6))

ax.hist(x, bins=range(-5, 4))
ax.set_title('Greedy colouring difference using the heuristic.')
ax.set_ylabel('Number of graphs')
ax.set_xlabel('Difference in colourings')
plt.show()