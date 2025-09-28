# unima_projeto_ed/dijkstra.py
from .priority_queue import PriorityQueue
from .weighted_graph import WeightedDirectedGraph
from .stack import Stack

# -------------------------------------------------
# Dijkstra: menor caminho em grafos com pesos >= 0
# Usa min-heap (PriorityQueue) e reconstrói caminho
# com uma PILHA (Stack) explicitamente (LIFO).
# -------------------------------------------------

def Dijkstra(graph, start, end):
    """
    graph: WeightedDirectedGraph
    start, end: nós existentes no grafo
    Retorna: (path:list, dist:float)
    """
    # Caso trivial
    if start == end:
        return [start], 0.0

    vertices = graph.get_vertices()

    # Tabelas auxiliares
    previous = {v: None for v in vertices}        # pai no caminho ótimo
    visited  = {v: False for v in vertices}       # já finalizado?
    distances = {v: float("inf") for v in vertices}
    distances[start] = 0.0

    # Fila de prioridade: (distância acumulada, nó)
    queue = PriorityQueue()
    queue.push(0.0, start)

    while not queue.is_empty():
        u = queue.pop()
        if visited[u]:
            continue
        visited[u] = True
        dist_u = distances[u]

        # Se alcançou o destino, reconstrói com PILHA (LIFO)
        if u == end:
            stack = Stack()
            cur = end
            while cur is not None:
                stack.push(cur)
                cur = previous[cur]

            path = []
            while not stack.is_empty():
                path.append(stack.pop())
            return path, distances[end]

        # Relaxa arestas que saem de u
        for v, w in graph.get_neighbors_with_weights(u):
            if visited[v]:
                continue
            if w < 0:
                # Dijkstra não suporta pesos negativos; ignora por sanidade
                continue

            alt = dist_u + w
            if alt < distances[v]:
                distances[v] = alt
                previous[v] = u
                queue.push(alt, v)

    # Não há caminho alcançável até 'end'
    return [], float("inf")


# -------------------------------------------------
# Exemplo simples (execução direta)
# -------------------------------------------------
if __name__ == "__main__":
    # Cria o grafo usando WeightedDirectedGraph
    my_graph = WeightedDirectedGraph()

    # Adiciona as arestas (não direcionadas)
    my_graph.add_undirected_edge("A", "B", 1.8)
    my_graph.add_undirected_edge("A", "C", 1.5)
    my_graph.add_undirected_edge("A", "D", 1.4)
    my_graph.add_undirected_edge("B", "E", 1.6)
    my_graph.add_undirected_edge("C", "E", 1.8)
    my_graph.add_undirected_edge("C", "F", 2.1)
    my_graph.add_undirected_edge("D", "F", 2.7)
    my_graph.add_undirected_edge("D", "G", 2.4)
    my_graph.add_undirected_edge("E", "F", 1.4)
    my_graph.add_undirected_edge("E", "H", 1.6)
    my_graph.add_undirected_edge("F", "G", 1.3)
    my_graph.add_undirected_edge("F", "H", 1.2)
    my_graph.add_undirected_edge("G", "H", 1.5)

    # Executa Dijkstra do A até H
    path, dist = Dijkstra(my_graph, start="A", end="H")
    print(f"shortest distance to H: {dist}")
    print(f"path to H: {path}")
