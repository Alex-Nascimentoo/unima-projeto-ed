# unima_projeto_ed/astar.py
from .priority_queue import PriorityQueue
from .utils import haversine  # usar a mesma unidade (km) das arestas
from .stack import Stack      # pilha (LIFO) manual para reconstrução

def heuristic(node1, node2, coordinates):
    lat1, lon1 = coordinates[node1]
    lat2, lon2 = coordinates[node2]
    return haversine(lat1, lon1, lat2, lon2)  # km

def a_star(graph, start, goal, coordinates):
    """
    A* sobre grafo no formato dict de adjacência:
      graph[u] = {v: peso_km, ...}
    coordinates: dict {node: (lat, lon)}
    Retorna: (path, distance)
    """
    # caso trivial
    if start == goal:
        return [start], 0.0

    pq = PriorityQueue()
    distances = {node: float('inf') for node in graph}  # g(n)
    distances[start] = 0.0
    previous = {}
    visited = set()

    # prioridade = (f, g) como tie-breaker; f = g + h
    h0 = heuristic(start, goal, coordinates)
    pq.push((h0, 0.0), start)

    while not pq.is_empty():
        current = pq.pop()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            # Reconstrução com PILHA (LIFO) explícita
            stack = Stack()
            cur = goal
            while cur in previous:
                stack.push(cur)
                cur = previous[cur]
            stack.push(start)

            path = []
            while not stack.is_empty():
                path.append(stack.pop())
            return path, distances[goal]

        for neighbor, weight in graph[current].items():
            # sanidade: ignorar pesos negativos
            if weight < 0:
                continue
            new_g = distances[current] + weight
            if new_g < distances[neighbor]:
                distances[neighbor] = new_g
                previous[neighbor] = current
                f_score = new_g + heuristic(neighbor, goal, coordinates)
                pq.push((f_score, new_g), neighbor)

    # sem caminho
    return [], float('inf')
