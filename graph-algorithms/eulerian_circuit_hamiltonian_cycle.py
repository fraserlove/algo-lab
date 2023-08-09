'''
Eulerian Circuit and Hamiltionian Cycle Algorithms.

Created 24/03/23
Developed by Fraser Love
'''

import networkx as nx

def eulerian_circuit(G):
    '''
    Finds an Eulerian circuit in a connected graph G(V, E), if one exists, in O(|E|).
    
    Parameters:
    G - a NetworkX graph.
    
    Returns:
    A list of vertices representing an Eulerian circuit in G if one exists, 
    or None if G does not have an Eulerian circuit.
    '''
    
    # Making a copy of the edges so we return the same graph we started with.
    edges = list(G.edges).copy()
    
    # Check if every vertex in G has even degree, Euler's Theorem - 0(|V|).
    if any(deg % 2 != 0 for v, deg in G.degree()):
        return None
    
    # Initialise a stack of vertices and an output circuit.
    stack = [0]
    circuit = []
    
    # Finding a Eulerian circuit for G - O(|E|).
    while stack:
        v = stack[-1]
        
        # If there are any edges from v that haven't already been considered.
        if G[v]:
            # Pick one such edge {v, u} and remove as cannot be used again (from either direction).
            u = next(iter(G[v]))
            G.remove_edge(v, u)
            stack.append(u) 
            
        # If there are no such edges, then pop v from the stack and append it to circuit.
        else:
            circuit.append(stack.pop())
      
    # Adding back in all the edges we deleted.
    G.add_edges_from(edges)
            
    return circuit


def depth_first_traversal(G, u):
    '''
    Performs depth first traversal on G(V, E) from a starting vertex u in O(|E|).
    
    Parameters:
    G - a NetworkX graph.
    u - starting vertex (int: 0 ≤ u ≤ |V|).
    
    Returns:
    A set describing the elements seen.
    '''
    
    # Create a stack and set of seen vertices for depth-first traversal.
    stack = [u]
    seen = set()
    
    # Performing depth-first traversal.
    while stack:
        v = stack.pop()
        if v not in seen:
            seen.add(v)
            stack.extend(u for u in G[v])
    return seen


def first_vertex_of_positive_degree(G):
    '''
    Returns the first vertex of G(V, E) with positive degree in O(|V|).
    
    Parameters:
    G - a NetworkX graph.
    
    Returns:
    The first vertex of positive degree.
    '''
    
    u = None
    for v in G:
        if G.degree(v) > 0:
            u = v
            break
    return u
    

def all_positive_degree_vertices_connected(G):
    '''
    Checks if G(V, E) is a graph where all the postitive degree vertices are connected in O(|V| + |E|).
    
    Parameters:
    G - a NetworkX graph.
    
    Returns:
    A boolean value describing if all the positive degree vertices are connected.
    '''
    
    # Find the first vertex with positive degree - O(|V|).
    u = first_vertex_of_positive_degree(G)

    # If all vertices have zero degree, positive degree vertices are trivially connected.
    if u is None:
        return True
            
    # Perform depth-first traversal - O(|E|).
    seen = depth_first_traversal(G, u)
    # Check if all nodes of positive degree are connected via depth first traversal - O(|V|).
    return all(v in seen for v in G if G.degree(v) > 0)


def hamiltonian_cycle(G):
    '''
    Finds a Hamiltonian cycle in a graph G(V, E), if one exists.
    
    Parameters:
    G - a NetworkX graph.
    
    Returns:
    A list of vertices representing a Hamiltonian cycle in G if one exists, 
    or None if G does not have a Hamiltonian cycle.
    '''

    def backtrack(path):
        # Base case: check if the current path is a valid Hamiltonian cycle.
        if len(path) == len(G) and path[-1] in G[path[0]]:
            return path

        # Recursive case: try extending the path with each unused neighbor of the last node.
        for u in G[path[-1]]:
            if u not in path:
                new_path = backtrack(path + [u])
                if new_path is not None:
                    return new_path

        # If no Hamiltonian cycle was found, return None.
        return None

    # Start the backtracking search from each vertex in the graph.
    for v in G.nodes():
        cycle = backtrack([v])
        if cycle is not None:
            return cycle + [v]

    # If no Hamiltonian cycle was found, return None.
    return None

# Finding a Hamiltonian cycle in the Hoffman-Singleton graph.
G = nx.hoffman_singleton_graph()
print(hamiltonian_cycle(G))

def is_eulerian(G):
    '''
    Checks if a graph is Eulerian by first checking if all positive degree vertices are
    connected and if the connected component of these positive degree vertices contains
    an Eulerian circuit.
    
    Parameters:
    G - a NetworkX graph.

    Returns:
    Boolean value describing if is Eulerian.
    '''
    
    if all_positive_degree_vertices_connected(G):
        # Finding first vertex of positive degree - O(|V|).
        u = first_vertex_of_positive_degree(G)
        # Find all vertices reachable from G - O(|E|).
        vertices = depth_first_traversal(G, u)
        # Create subgraph of connected vertices, hence removing isolated vertices - O(|V|).
        sG = G.subgraph(vertices).copy()
        # If the connected subgraph sG contains a eulerian circuit, G is eulerian - O(|E|).
        return eulerian_circuit(sG) is not None
    return False


def verify_by_eulers_theorem(G):
    '''
    Checks whether a given graph satisfies Euler's Theorem: A graph has an Eulerian circuit
    if and only if every vertex has even degree, and all of the vertices of positive degree
    are in one connected component.

    Parameters:
    G - a NetworkX graph.

    Returns:
    Boolean value describing if the graph satisfies the theorem.
    '''

    # Finding first vertex of positive degree - O(|V|).
    u = first_vertex_of_positive_degree(G)
    # Find all vertices reachable from G - O(|E|).
    seen = depth_first_traversal(G, u)
    # Check if the degree of every vertex is even and if all the vertices of positive 
    # degree are in the component with vertices in seen - O(|V| + |E|).
    return all(v in seen and G.degree(v) % 2 == 0 for v in G if G.degree(v) > 0)
    

# Tests
G = nx.Graph([{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 1}, {1, 3}, {0, 3}])
print(is_eulerian(G), verify_by_eulers_theorem(G))

G.remove_edge(4, 1)
print(is_eulerian(G), verify_by_eulers_theorem(G))

G.add_edge(4, 1)
G.add_nodes_from(range(5, 8))
print(is_eulerian(G), verify_by_eulers_theorem(G))

G = nx.caveman_graph(3, 5)
print(is_eulerian(G), verify_by_eulers_theorem(G))

G = nx.Graph([{0, 1}, {1, 2}, {2, 3}, {3, 0}, {4, 2}])
print(is_eulerian(G), verify_by_eulers_theorem(G))

G = nx.random_degree_sequence_graph([2,2,2,2,2,2,4,4,4,6])
print(is_eulerian(G), verify_by_eulers_theorem(G))