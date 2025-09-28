# astar.py
from .priority_queue import PriorityQueue
from .utils import haversine  # usar a mesma unidade (km) das arestas

def heuristic(node1, node2, coordinates):
    lat1, lon1 = coordinates[node1]
    lat2, lon2 = coordinates[node2]
    return haversine(lat1, lon1, lat2, lon2)  # km

def a_star(graph, start, goal, coordinates):
    pq = PriorityQueue()
    distances = {node: float('inf') for node in graph}
    distances[start] = 0.0
    previous = {}
    visited = set()

    pq.push(heuristic(start, goal, coordinates), start)

    while not pq.is_empty():
        current = pq.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbor, weight in graph[current].items():
            new_distance = distances[current] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                f_score = new_distance + heuristic(neighbor, goal, coordinates)
                pq.push(f_score, neighbor)

    # sem caminho
    if distances[goal] == float('inf'):
        return [], float('inf')

    # reconstrói caminho
    path = []
    cur = goal
    while cur in previous:
        path.append(cur)
        cur = previous[cur]
    path.append(start)
    path.reverse()
    return path, distances[goal]
