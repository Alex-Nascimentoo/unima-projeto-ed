#how dijkstra algorithm works
#first of all, i need to understand the pre-requisites of the algorithm
#we need a graph, a starting node, and an ending node
#we can't have a graph with negative weights

class Graph:
  def __init__(self, graph: dict = {}):
    self.graph = graph
    
  def add_edge(self, node1, node2, weight):
    if node1 not in self.graph:
      self.graph[node1] = {}
    self.graph[node1][node2] = weight
    
  def shortest_distances(self, source: str):
    distances = {node: float("inf") for node in self.graph}
    distances[source] = 0
    
    
graph = {
   "A": {"B": 3, "C": 3},
   "B": {"A": 3, "D": 3.5, "E": 2.8},
   "C": {"A": 3, "E": 2.8, "F": 3.5},
   "D": {"B": 3.5, "E": 3.1, "G": 10},
   "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
   "F": {"G": 2.5, "C": 3.5},
   "G": {"F": 2.5, "E": 7, "D": 10},
}

G = Graph(graph=graph)
print(G.graph)