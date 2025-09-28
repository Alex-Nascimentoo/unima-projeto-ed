from Dijkstra import Dijkstra
from a_star import a_star

def solve_vrp_dijkstra(graph, delivery_vertices):
    route = []
    total_cost = 0
    nodes_visited = 0
    for i in range(len(delivery_vertices) - 1):
        result = Dijkstra(graph, delivery_vertices[i], delivery_vertices[i+1])
        if result is None:
            continue
        route.extend(result.get("path", []))
        total_cost += result.get("cost", 0)
        nodes_visited += result.get("nodes_visited", 0)
    return {
        "route": [v.value for v in route],
        "cost": total_cost,
        "nodes_visited": nodes_visited,
        "details": "VRP sequencial com Dijkstra"
    }

def solve_vrp_astar(graph, delivery_vertices):
    route = []
    total_cost = 0
    nodes_visited = 0
    for i in range(len(delivery_vertices) - 1):
        result = a_star(graph, delivery_vertices[i], delivery_vertices[i+1])
        if result is None:
            continue
        route.extend(result.get("path", []))
        total_cost += result.get("cost", 0)
        nodes_visited += result.get("nodes_visited", 0)
    return {
        "route": [v.value for v in route],
        "cost": total_cost,
        "nodes_visited": nodes_visited,
        "details": "VRP sequencial com A*"
    }