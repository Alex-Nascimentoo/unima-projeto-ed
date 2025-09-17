import itertools
from heapq import heappush, heappop

#how dijkstra algorithm works
#first of all, i need to understand the pre-requisites of the algorithm
#we need a graph, a starting node, and an ending node
#we can't have a graph with negative weights

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        
class Vertex:
    def __init__(self, value):
        self.value = value
        
class Edge:
    def __init__(self, distance, vertex):
        self.distance = distance
        self.vertex = vertex


def Dijkstra(graph, start, end):
    previous = {v: None for v in graph.adjacency_list.keys()}
    visited = {v: False for v in graph.adjacency_list.keys()}
    distances = {v: float("inf") for v in graph.adjacency_list.keys()}
    distances[start] = 0
    queue = PriorityQueue()
    queue.add_task(0, start)
    path = []
    while queue:
        removed_distance, removed = queue.pop_task()
        visited[removed] = True
        
        if removed is end:
            while previous[removed]:
                path.append(removed.value)
                removed = previous[removed]
            path.append(start.value)
            print(f"shortest distance to {end.value}: ", distances[end])
            print(f"path to {end.value}: ", path[::-1])
            return
        
        for edge in graph.adjacency_list[removed]:
            if visited[edge.vertex]:
                continue
            new_distance = removed_distance + edge.distance
            if new_distance < distances[edge.vertex]:
                distances[edge.vertex] = new_distance
                previous[edge.vertex] = removed
                queue.add_task(new_distance, edge.vertex)
    return
    
class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()
        
    def __len__(self):
        return len(self.pq)
    
    def add_task(self, priority, task):
        if task in self.entry_finder:
            self.update_priority(priority, task)
            return self
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)
        
    def update_priority(self, priority, task):
        entry = self.entry_finder[task]
        count = next(self.counter)
        entry[0], entry[1] = priority, count
        
    def pop_task(self):
        while self.pq:
            priority, count, task = heappop(self.pq)
            del self.entry_finder[task]
            return priority, task
        raise KeyError("pop from an empty priority queue")

vertices = [Vertex("A"), Vertex("B"), Vertex("C"), Vertex("D"), Vertex("E"), Vertex("F"), Vertex("G"), Vertex("H")]
A, B, C, D, E, F, G, H = vertices

adj_list = {
    A: [Edge(1.8, B), Edge(1.5, C), Edge(1.4, D)],
    B: [Edge(1.8, A), Edge(1.6, E)],
    C: [Edge(1.5, A), Edge(1.8, E), Edge(2.1, F)],
    D: [Edge(1.4, A), Edge(2.7, F), Edge(2.4, G)],
    E: [Edge(1.6, B), Edge(1.8, C), Edge(1.4, F), Edge(1.6, H)],
    F: [Edge(2.1, C), Edge(2.7, D), Edge(1.4, E), Edge(1.3, G), Edge(1.2, H)],
    G: [Edge(2.4, D), Edge(1.3, F), Edge(1.5, H)],
    H: [Edge(1.6, E), Edge(1.2, F), Edge(1.5, G)],
}

my_graph = Graph(adj_list)

Dijkstra(my_graph, start=A, end=H)