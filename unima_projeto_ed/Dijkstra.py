import itertools
from heapq import heappush, heappop

# ---------------------------------------------
# Dijkstra (pré-requisitos e ideia geral)
# ---------------------------------------------
# - Temos um grafo, um nó inicial (start) e um nó final (end).
# - Os pesos das arestas DEVEM ser não negativos (Dijkstra não funciona com peso negativo).
# - A estratégia: manter uma dist[] com a menor distância conhecida até cada vértice
#   e usar uma fila de prioridade (min-heap) para sempre expandir o vértice com a menor distância atual.

# ---------------------------------------------
# Estruturas básicas do grafo
# ---------------------------------------------

class Graph:
    def __init__(self, adjacency_list):
        # adjacency_list: dicionário { Vertex -> [Edge, Edge, ...] }
        # Para cada vértice, guardamos uma lista de arestas (Edge) que saem dele.
        self.adjacency_list = adjacency_list

class Vertex:
    def __init__(self, value):
        # value: um rótulo/identificador do vértice (ex.: "A", "B", ...)
        self.value = value
        # OBS: não definimos __eq__ e __hash__, então o Python usa a identidade do objeto.
        # Isso permite usar Vertex como chave de dicionário (baseado em id do objeto).

class Edge:
    def __init__(self, distance, vertex):
        # distance: peso da aresta (custo/distância)
        # vertex: vértice de destino (objeto Vertex)
        self.distance = distance
        self.vertex = vertex


# ---------------------------------------------
# Implementação do Dijkstra
# ---------------------------------------------

def Dijkstra(graph, start, end):
    # previous: guarda o "pai" no caminho ótimo (para reconstruir o caminho no final)
    previous = {v: None for v in graph.adjacency_list.keys()}

    # visited: marca quais vértices já foram "finalizados" (não precisam mais ser relaxados)
    visited = {v: False for v in graph.adjacency_list.keys()}

    # distances: distância mínima conhecida até cada vértice (inicialmente infinito)
    distances = {v: float("inf") for v in graph.adjacency_list.keys()}
    distances[start] = 0  # distância do início até ele mesmo é 0

    # Fila de prioridade (min-heap). Armazena pares (distância, vértice).
    queue = PriorityQueue()
    queue.add_task(0, start)

    # 'path' será usado para reconstruir/imprimir o caminho
    path = []

    # Enquanto houver itens na fila
    while queue:
        # Remove o vértice com a MENOR distância atual (menor prioridade)
        removed_distance, removed = queue.pop_task()
        # Marca como visitado/finalizado
        visited[removed] = True

        # Se chegamos ao destino, reconstruímos o caminho e encerramos
        # ATENÇÃO: aqui é usado "is" (identidade de objeto). Como start/end/A/B/... são os MESMOS objetos,
        # isso funciona. Se você recriasse objetos iguais porém diferentes, preferiria "==" com __eq__ definido.
        if removed is end:
            # Sobe encadeando 'previous' até o início
            while previous[removed]:
                path.append(removed.value)       # adiciona o rótulo do vértice atual
                removed = previous[removed]      # vai para o pai no caminho ótimo
            path.append(start.value)             # por fim, coloca o início
            # Imprime a distância mínima encontrada até 'end'
            print(f"shortest distance to {end.value:}: ", distances[end])
            # O 'path' foi construído de trás pra frente, então invertimos para exibir do início ao fim
            print(f"path to {end.value}: ", path[::-1])
            return

        # Relaxamento das arestas que saem de 'removed'
        for edge in graph.adjacency_list[removed]:
            # Se o destino já foi finalizado, ignoramos
            if visited[edge.vertex]:
                continue

            # Custo de chegar ao vizinho (edge.vertex) passando por 'removed'
            new_distance = removed_distance + edge.distance

            # Se encontramos um caminho melhor, atualiza dist e previous
            if new_distance < distances[edge.vertex]:
                distances[edge.vertex] = new_distance
                previous[edge.vertex] = removed
                # Empurra para a fila a nova melhor distância conhecida desse vizinho
                queue.add_task(new_distance, edge.vertex)

    # Se a fila esvaziar sem encontrar 'end', não há caminho (ou não foi alcançado)
    return


# ---------------------------------------------
# Fila de Prioridade (Priority Queue) com heapq
# ---------------------------------------------

class PriorityQueue:
    def __init__(self):
        self.pq = []                # lista que o heapq usa como heap (min-heap)
        self.entry_finder = {}      # mapeia task -> entry (para localizar a entrada da task)
        self.counter = itertools.count()  # contador incremental (para desempate estável)

    def __len__(self):
        # retorna o número de entradas físicas no heap (não é o "tamanho lógico" se houvesse entradas inválidas)
        return len(self.pq)

    def add_task(self, priority, task):
        # Se a task já está no heap, tenta atualizar a prioridade
        if task in self.entry_finder:   # já existe?
            self.update_priority(priority, task)  # ATENÇÃO: ver comentário do update_priority
            return self

        # Gera um número único para desempate
        count = next(self.counter)
        # Cada entrada é uma lista [priority, count, task]
        entry = [priority, count, task]
        # Guarda no dicionário para acesso rápido depois
        self.entry_finder[task] = entry
        # Insere no heap mantendo a propriedade de min-heap
        heappush(self.pq, entry)

    def update_priority(self, priority, task):
        # Pega a entrada atual da task
        entry = self.entry_finder[task]
        # Novo carimbo de desempate (para não empatar com a versão anterior)
        count = next(self.counter)
        # *** CUIDADO ***
        # Aqui estamos MUDANDO a entrada por dentro (in-place).
        # O heapq não sabe que isso aconteceu; em geral, isso pode DESORGANIZAR o heap.
        entry[0], entry[1] = priority, count

    def pop_task(self):
        # Remove e retorna a entrada com menor [priority, count]
        # (heappop retira a raiz do heap)
        while self.pq:
            priority, count, task = heappop(self.pq)
            # Remove do dicionário de "entradas ativas"
            del self.entry_finder[task]
            # Retorna par (prioridade, tarefa)
            return priority, task
        # Se tentar tirar de um heap vazio, levanta erro
        raise KeyError("pop from an empty priority queue")


# ---------------------------------------------
# Montagem do grafo de exemplo
# ---------------------------------------------

# Cria 8 vértices com rótulos "A"..."H"
vertices = [Vertex("A"), Vertex("B"), Vertex("C"), Vertex("D"),
            Vertex("E"), Vertex("F"), Vertex("G"), Vertex("H")]
A, B, C, D, E, F, G, H = vertices  # apenas açucar para nomear

# Lista de adjacência:
# Para cada vértice, lista de arestas (peso, destino).
# Aqui o grafo é essencialmente "não direcionado" porque você colocou a aresta nos dois sentidos (A<->B, A<->C, ...).
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

# Instancia o grafo
my_graph = Graph(adj_list)

# Executa Dijkstra do A até H
Dijkstra(my_graph, start=A, end=H)
