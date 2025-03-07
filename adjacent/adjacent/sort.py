import networkx as nx
import heapq as hq

def topological_sort(G: nx.DiGraph) -> list[int]:
    '''Topologically sorts a DAG G of connected nodes and returns a topological ordering of the graph.'''
    stack = []
    visited = {node: False for node in G.nodes()}
    
    def dfs(n):
        visited[n] = True
        for neighbor in G.successors(n):
            if not visited[neighbor]:
                dfs(neighbor)
        stack.append(n)
    
    for node in G.nodes():
        if not visited[node]:
            dfs(node)
    
    return stack[::-1]  # Reverse to get correct order

def topological_sort_lexicographical(G: nx.DiGraph) -> list[int]:
    '''Topologically sorts a DAG G of connected nodes and returns the lexicographically smallest topological ordering of the graph.'''
    in_degree = {node: 0 for node in G.nodes()}
    for _, v in G.edges():
        in_degree[v] += 1
    
    nodes = []
    for node in G.nodes():
        if in_degree[node] == 0:
            hq.heappush(nodes, node)
    
    stack = []
    while nodes:
        # Extract node with min order
        n = hq.heappop(nodes)
        stack.append(n)
        
        for neighbor in G.successors(n):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                hq.heappush(nodes, neighbor)
    
    return stack

# Example usage
G = nx.DiGraph()
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5)]
G.add_edges_from(edges)

# Running topological sort
result = topological_sort(G)
print(" ".join([str(i) for i in result]))

# Running lexicographically smallest topological sort
result = topological_sort_lexicographical(G)
print(" ".join([str(i) for i in result]))