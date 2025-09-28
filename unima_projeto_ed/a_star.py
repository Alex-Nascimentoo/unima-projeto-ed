import math
from priority_queue import PriorityQueue

def heuristic(node1, node2, coordinates):
    # Calcula a distância euclidiana entre dois pontos.
    x1, y1 = coordinates[node1]
    x2, y2 = coordinates[node2]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def a_star(graph, start, goal, coordinates):
    """
    Algoritmo A* - Dijkstra otimizado com heurística.
    f(n) = g(n) + h(n)
    """
    pq = PriorityQueue()
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {}
    
    pq.push(heuristic(start, goal, coordinates), start)
    
    while not pq.is_empty():
        current = pq.pop()
        
        if current == goal:
            break
            
        for neighbor, weight in graph[current].items():
            new_distance = distances[current] + weight
            
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                f_score = new_distance + heuristic(neighbor, goal, coordinates)
                pq.push(f_score, neighbor)
    
    # Reconstrói o caminho
    path = []
    current = goal
    while current in previous:
        path.append(current)
        current = previous[current]
    path.append(start)
    path.reverse()
    
    return path, distances[goal]