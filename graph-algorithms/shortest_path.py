'''
Finds the Shortest Path and the Diameter of a Graph.

Created 16/03/23
Developed by Fraser Love
'''

import networkx as nx
from collections import deque

def shortest_path(G, u = 0, v = 0):
    '''
    Returns the shortest path from u (default 0) to v (default 0) in G as an array.
    Vertices of G are assumed to be {0, 1, ..., n - 1}
    '''
    
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
        
def breadth_first_traversal(G, u = 0):
    '''
    Performs breadth_first_traversal of G, starting at vertex u (default 0),
    and returns the last vertex v in the queue which has not been seen.
    '''

    seen = set()
    queue = deque([u])
    v = None
    while queue:
        u = queue.popleft()
        if u not in seen:
            seen.add(u)
            v = u
            queue.extend(T[u])
    return v

def tree_diameter(T):
    '''
    Returns the diameter of any tree T.
    '''
    
    # Breadth-first traversal from any vertex to find the farthest vertex from any arbitray vertex.
    v = breadth_first_traversal(T)
    # Breadth-first traversal from the farthest vertex to find the vertex farthest from it.
    w = breadth_first_traversal(T, v)
    # Finally, return the distance between the two farthest vertices.
    return len(shortest_path(T, v, w)) - 1

T = nx.from_graph6_bytes(b"Y????????????????????????????w?F?o??o??GW?@?W?A?B?Q?K?`?")
print(f"Diameter of T: {tree_diameter(T)}")