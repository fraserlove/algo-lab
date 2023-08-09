"""
Topological Sorting for a Directed Acyclic Graph

Created 10/01/22
Developed by Fraser Love

Topologically sorts a DAG graph of connected nodes. Has uses for example mapping and ordering items which
rely on other items as depenencies (i.e. university modules).
"""

import sys

class Graph:
    def __init__(self, size):
        self.graph = [[] for i in range(size)]
        self.size = size
        
    def add_edge(self, x, y):
        self.graph[x].append(y)
        
    def sort(self, n, visited, stack):
        visited[n] = True
        for i in self.graph[n]:
            if visited[i] == False:
                self.sort(i, visited, stack)
        stack.append(n)
        
    def topological_sort(self):
        stack = []
        visited = [False] * self.size
        for i in range(self.size):
            if visited[i] == False:
                self.sort(i, visited, stack)
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