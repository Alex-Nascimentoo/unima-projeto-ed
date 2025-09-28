import math
from .a_star import a_star  # usa teu A*

class Delivery:
    def __init__(self, id, node, demand):
        self.id = id
        self.node = node  # nó do grafo (mesmo que você passa pro A*)
        self.demand = demand


def build_distance_matrix(graph, coordinates, points):
    """
    Cria matriz de distâncias chamando o A* para cada par de pontos.
    points = lista de nós [depósito, cliente1, cliente2...]
    """
    matrix = {}
    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                path, dist = a_star(graph, points[i], points[j], coordinates)
                matrix[(points[i], points[j])] = dist
    return matrix


def nearest_neighbor_cvrp(graph, coordinates, deliveries, capacity, depot):
    """
    Heurística Vizinho Mais Próximo para CVRP.
    - graph: grafo (dict {node: {vizinho: peso}})
    - coordinates: dict {node: (lat, lon)} (usado na heurística do A*)
    - deliveries: lista de objetos Delivery
    - capacity: capacidade máxima do veículo
    - depot: nó do depósito
    """

    # ---------------------------------------------
    # Validações iniciais (evita loop infinito e soluções inválidas)
    # ---------------------------------------------
    if capacity <= 0:
        raise ValueError("Capacidade do veículo deve ser maior que 0.")

    over_capacity = [d.id for d in deliveries if d.demand > capacity]
    if over_capacity:
        raise ValueError(f"Entregas inviáveis (demanda > capacidade): {over_capacity}")

    # pontos relevantes (depósito + clientes)
    points = [depot] + [d.node for d in deliveries]

    # matriz de distâncias via A*
    dist_matrix = build_distance_matrix(graph, coordinates, points)

    # Verifica nós desconectados (A* retornou inf)
    for (i, j), dist in dist_matrix.items():
        if dist == float('inf'):
            raise ValueError(f"Nós desconectados no grafo entre {i} e {j}.")

    # clientes restantes
    remaining = deliveries[:]
    routes = []
    total_distance = 0.0

    while remaining:
        route = [depot]
        load = 0
        current = depot

        while True:
            # candidatos que cabem no veículo
            candidates = [d for d in remaining if d.demand + load <= capacity]
            if not candidates:
                break

            # escolhe o mais próximo
            best = None
            best_cost = math.inf
            for d in candidates:
                cost = dist_matrix[(current, d.node)]
                if cost < best_cost:
                    best_cost = cost
                    best = d

            # vai até o cliente escolhido
            route.append(best.node)
            total_distance += best_cost
            load += best.demand
            current = best.node
            remaining.remove(best)

        # volta ao depósito (garante que existe caminho de volta)
        return_cost = dist_matrix.get((current, depot), float('inf'))
        if return_cost == float('inf'):
            raise ValueError(f"Sem caminho de {current} para o depósito.")
        total_distance += return_cost
        route.append(depot)
        routes.append(route)

    return routes, total_distance
