# Importa a função para calcular distância entre coordenadas geográficas
from .grafo import haversine

# Grafo direcionado e ponderado para representar redes de ruas
class WeightedDirectedGraph:
    def __init__(self):
        # Conjunto de todos os vértices (cruzamentos/pontos)
        self.vertices = set()
        # Dicionário que armazena as arestas: {origem: {destino: peso}}
        self.edges = {}
    
    # Adiciona um novo vértice ao grafo
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        # Inicializa lista de vizinhos vazia se não existir
        if vertex not in self.edges:
            self.edges[vertex] = {}
    
    # Adiciona uma aresta com peso específico
    def add_edge(self, source, target, weight):
        # Garante que ambos os vértices existam
        self.add_vertex(source)
        self.add_vertex(target)
        # Cria a conexão direcionada com o peso
        self.edges[source][target] = weight
    
    # Adiciona uma aresta não-direcionada (bidirecional)
    def add_undirected_edge(self, source, target, weight):
        # Adiciona aresta em ambas as direções
        self.add_edge(source, target, weight)
        self.add_edge(target, source, weight)
    
    # Adiciona aresta calculando o peso automaticamente pela distância geográfica
    def add_edge_with_coords(self, source, target, source_coords, target_coords):
        # Calcula a distância real entre as coordenadas
        weight = haversine(source_coords, target_coords)
        self.add_edge(source, target, weight)
    
    # Adiciona aresta não-direcionada com coordenadas
    def add_undirected_edge_with_coords(self, source, target, source_coords, target_coords):
        # Calcula a distância real entre as coordenadas
        weight = haversine(source_coords, target_coords)
        self.add_undirected_edge(source, target, weight)
    
    # Retorna o peso de uma aresta específica
    def get_weight(self, source, target):
        return self.edges.get(source, {}).get(target)
    
    # Retorna lista dos vizinhos de um vértice
    def get_neighbors(self, vertex):
        return list(self.edges.get(vertex, {}).keys())
    
    # Retorna vizinhos com seus respectivos pesos
    def get_neighbors_with_weights(self, vertex):
        return list(self.edges.get(vertex, {}).items())
    
    # Verifica se um vértice existe no grafo
    def has_vertex(self, vertex):
        return vertex in self.vertices
    
    # Verifica se existe uma aresta entre dois vértices
    def has_edge(self, source, target):
        return target in self.edges.get(source, {})
    
    # Remove uma aresta específica
    def remove_edge(self, source, target):
        if source in self.edges and target in self.edges[source]:
            del self.edges[source][target]
    
    # Remove uma aresta não-direcionada (ambas as direções)
    def remove_undirected_edge(self, source, target):
        self.remove_edge(source, target)
        self.remove_edge(target, source)
    
    # Retorna lista de todos os vértices
    def get_vertices(self):
        return list(self.vertices)
    
    # Conta o número total de vértices
    def vertex_count(self):
        return len(self.vertices)
    
    # Conta o número total de arestas
    def edge_count(self):
        return sum(len(neighbors) for neighbors in self.edges.values())