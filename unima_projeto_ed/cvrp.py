# unima_projeto_ed/cvrp.py
import math
from .a_star import a_star  # default

class Delivery:
    def __init__(self, id, node, demand):
        self.id = id
        self.node = node
        self.demand = demand

def build_distance_matrix(graph, coordinates, points, shortest_path_fn):
    """
    Cria matriz de distâncias chamando a função de menor caminho para cada par.
    shortest_path_fn: (graph, start, goal, coordinates) -> (path, dist)
    """
    matrix = {}
    for i in range(len(points)):
        for j in range(len(points)):
            a, b = points[i], points[j]
            if i == j:
                matrix[(a, b)] = 0.0
            else:
                _, dist = shortest_path_fn(graph, a, b, coordinates)
                matrix[(a, b)] = dist
    return matrix

def nearest_neighbor_cvrp(graph, coordinates, deliveries, capacity, depot, sp="a_star"):
    """
    sp: 'a_star' (default) ou 'dijkstra' — algoritmo p/ matriz de distâncias.
    """
    if capacity <= 0:
        raise ValueError("Capacidade do veículo deve ser maior que 0.")

    over_capacity = [d.id for d in deliveries if d.demand > capacity]
    if over_capacity:
        raise ValueError(f"Entregas inviáveis (demanda > capacidade): {over_capacity}")

    # escolhe a função de menor caminho
    if sp == "a_star":
        sp_fn = a_star
    elif sp == "dijkstra":
        from .dijkstra_adapter import dijkstra_adapter
        sp_fn = dijkstra_adapter
    else:
        raise ValueError("Parâmetro 'sp' deve ser 'a_star' ou 'dijkstra'.")

    points = [depot] + [d.node for d in deliveries]
    dist_matrix = build_distance_matrix(graph, coordinates, points, sp_fn)

    # valida desconexão
    for (i, j), dist in dist_matrix.items():
        if dist == float('inf'):
            raise ValueError(f"Nós desconectados no grafo entre {i} e {j}.")

    remaining = deliveries[:]
    routes = []
    total_distance = 0.0

    while remaining:
        route = [depot]
        load = 0
        current = depot

        while True:
            candidates = [d for d in remaining if d.demand + load <= capacity]
            if not candidates:
                break

            best = None
            best_cost = math.inf
            for d in candidates:
                cost = dist_matrix[(current, d.node)]
                if cost < best_cost:
                    best_cost = cost
                    best = d

            route.append(best.node)
            total_distance += best_cost
            load += best.demand
            current = best.node
            remaining.remove(best)

        return_cost = dist_matrix.get((current, depot), float('inf'))
        if return_cost == float('inf'):
            raise ValueError(f"Sem caminho de {current} para o depósito.")
        total_distance += return_cost
        route.append(depot)
        routes.append(route)

    return routes, total_distance
