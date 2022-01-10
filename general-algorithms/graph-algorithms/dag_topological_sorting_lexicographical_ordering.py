"""
Lexicographically Smallest Topological Sorting for a Directed Acyclic Graph

Created 10/01/22
Developed by Fraser Love

Topologically sorts a DAG graph of connected nodes, if two or more nodes do not have any parent node then
the node with the smallest number appears first in the ordering. Has uses for example mapping and ordering
items which rely on other items as depenencies (i.e. university modules).
"""

import sys
import heapq as hq

class Graph:
    def __init__(self, size):
        self.graph = [[] for i in range(size)]
        self.size = size
        
    def add_edge(self, x, y):
        self.graph[x].append(y)
 
    def topological_sort(self):
        in_degree = [0] * self.size

        for i in range(self.size):
            for j in self.graph[i]:
                in_degree[j] += 1
        
        nodes = []
        for i in range(self.size):
            if in_degree[i] == 0:
                hq.heappush(nodes, i)
        
        stack = []
        while nodes:
            # Extract node with min order
            n = hq.heappop(nodes)
            stack.append(n)

            for i in self.graph[n]:
                in_degree[i] -= 1
                if in_degree[i] == 0:
                    hq.heappush(nodes, i)
        return stack

# Creating a graph of prerequisits    
n = int(sys.stdin.readline())
graph = Graph(n)

for line in sys.stdin:
    node_relation = line.split()
    parent = node_relation[0]
    for child in node_relation[1:]:
        graph.add_edge(int(parent), int(child))

# Running lexiographically smallest topological sort        
result = graph.topological_sort()
print(" ".join([str(i) for i in result]))