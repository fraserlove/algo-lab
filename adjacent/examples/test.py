import networkx as nx

from adjacent import tree_diameter, hamiltonian_cycle, is_eulerian, satisfies_eulers_theorem

G = nx.hoffman_singleton_graph()
assert hamiltonian_cycle(G) == [0, 1, 17, 4, 3, 5, 12, 11, 2, 10, 18,6, 22, 13, 30, 19, 7,
                                34, 15, 35, 25, 9, 32, 23, 14, 31, 20, 37, 29, 16, 33, 27,
                                44, 43, 42, 26, 38, 24, 41, 40, 21, 36, 39, 28, 48, 47, 45,
                                46, 49, 8, 0]

G = nx.Graph([{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 1}, {1, 3}, {0, 3}])
assert is_eulerian(G) == satisfies_eulers_theorem(G)

G.remove_edge(4, 1)
assert is_eulerian(G) == satisfies_eulers_theorem(G)

G.add_edge(4, 1)
G.add_nodes_from(range(5, 8))
assert is_eulerian(G) == satisfies_eulers_theorem(G)

G = nx.caveman_graph(3, 5)
assert is_eulerian(G) == satisfies_eulers_theorem(G)

G = nx.Graph([{0, 1}, {1, 2}, {2, 3}, {3, 0}, {4, 2}])
assert is_eulerian(G) == satisfies_eulers_theorem(G)

G = nx.random_degree_sequence_graph([2,2,2,2,2,2,4,4,4,6])
assert is_eulerian(G) == satisfies_eulers_theorem(G)

G = nx.from_graph6_bytes(b'Y????????????????????????????w?F?o??o??GW?@?W?A?B?Q?K?`?')
assert tree_diameter(G) == 9