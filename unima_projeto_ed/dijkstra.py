from priority_queue import PriorityQueue
from weighted_graph import WeightedDirectedGraph

# ---------------------------------------------
# Dijkstra (pré-requisitos e ideia geral)
# ---------------------------------------------
# - Temos um grafo, um nó inicial (start) e um nó final (end).
# - Os pesos das arestas DEVEM ser não negativos (Dijkstra não funciona com peso negativo).
# - A estratégia: manter uma dist[] com a menor distância conhecida até cada vértice
#   e usar uma fila de prioridade (min-heap) para sempre expandir o vértice com a menor distância atual.


# ---------------------------------------------
# Implementação do Dijkstra
# ---------------------------------------------

def Dijkstra(graph, start, end):
    # previous: guarda o "pai" no caminho ótimo (para reconstruir o caminho no final)
    previous = {v: None for v in graph.get_vertices()}

    # visited: marca quais vértices já foram "finalizados" (não precisam mais ser relaxados)
    visited = {v: False for v in graph.get_vertices()}

    # distances: distância mínima conhecida até cada vértice (inicialmente infinito)
    distances = {v: float("inf") for v in graph.get_vertices()}
    distances[start] = 0  # distância do início até ele mesmo é 0

    # Fila de prioridade (min-heap). Armazena pares (distância, vértice).
    queue = PriorityQueue()
    queue.push(0, start)

    # 'path' será usado para reconstruir/imprimir o caminho
    path = []

    # Enquanto houver itens na fila
    while not queue.is_empty():
        # Remove o vértice com a MENOR distância atual (menor prioridade)
        removed = queue.pop()
        removed_distance = distances[removed]
        # Marca como visitado/finalizado
        visited[removed] = True

        # Se chegamos ao destino, reconstruímos o caminho e encerramos
        if removed == end:
            # Sobe encadeando 'previous' até o início
            while previous[removed]:
                path.append(removed)       # adiciona o vértice atual
                removed = previous[removed]      # vai para o pai no caminho ótimo
            path.append(start)             # por fim, coloca o início
            # Imprime a distância mínima encontrada até 'end'
            print(f"shortest distance to {end}: ", distances[end])
            # O 'path' foi construído de trás pra frente, então invertemos para exibir do início ao fim
            print(f"path to {end}: ", path[::-1])
            return

        # Relaxamento das arestas que saem de 'removed'
        for neighbor, weight in graph.get_neighbors_with_weights(removed):
            # Se o destino já foi finalizado, ignoramos
            if visited[neighbor]:
                continue

            # Custo de chegar ao vizinho passando por 'removed'
            new_distance = removed_distance + weight

            # Se encontramos um caminho melhor, atualiza dist e previous
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = removed
                # Empurra para a fila a nova melhor distância conhecida desse vizinho
                queue.push(new_distance, neighbor)

    # Se a fila esvaziar sem encontrar 'end', não há caminho (ou não foi alcançado)
    return


# ---------------------------------------------
# Montagem do grafo de exemplo
# ---------------------------------------------

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
Dijkstra(my_graph, start="A", end="H")