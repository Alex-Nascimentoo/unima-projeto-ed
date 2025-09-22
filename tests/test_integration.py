import pytest
from unima_projeto_ed.priority_queue import PriorityQueue
from unima_projeto_ed.a_star import heuristic, a_star
from unima_projeto_ed.weighted_graph import WeightedDirectedGraph
from unima_projeto_ed.grafo import haversine, build_graph


def test_priority_queue_integration():
    """Testa se a PriorityQueue funciona corretamente com o A*"""
    pq = PriorityQueue()
    
    # Testa operações básicas
    pq.push(3.0, 'A')
    pq.push(1.0, 'B')
    pq.push(2.0, 'C')
    
    assert pq.pop() == 'B'  # Menor prioridade
    assert pq.pop() == 'C'
    assert pq.pop() == 'A'
    assert pq.is_empty()


def test_weighted_graph_with_a_star():
    """Testa integração entre WeightedDirectedGraph e A*"""
    # Cria grafo usando a classe WeightedDirectedGraph
    wg = WeightedDirectedGraph()
    
    # Adiciona vértices e arestas
    wg.add_undirected_edge('A', 'B', 4)
    wg.add_undirected_edge('A', 'C', 2)
    wg.add_undirected_edge('B', 'D', 3)
    wg.add_undirected_edge('C', 'D', 1)
    wg.add_undirected_edge('D', 'E', 2)
    
    # Converte para formato compatível com A*
    graph = wg.edges
    coordinates = {
        'A': (0, 0),
        'B': (1, 1),
        'C': (0, 2),
        'D': (2, 2),
        'E': (3, 3)
    }
    
    # Executa A*
    path, cost = a_star(graph, 'A', 'E', coordinates)
    
    assert path == ['A', 'C', 'D', 'E']
    assert cost == 5


def test_haversine_with_a_star():
    """Testa integração com coordenadas geográficas reais"""
    # Coordenadas de exemplo (lat, lon)
    coords = {
        'SP': (-23.5505, -46.6333),  # São Paulo
        'RJ': (-22.9068, -43.1729),  # Rio de Janeiro
        'BH': (-19.9167, -43.9345)   # Belo Horizonte
    }
    
    # Cria grafo com distâncias reais
    graph = {
        'SP': {'RJ': haversine(coords['SP'], coords['RJ']), 
               'BH': haversine(coords['SP'], coords['BH'])},
        'RJ': {'SP': haversine(coords['RJ'], coords['SP']),
               'BH': haversine(coords['RJ'], coords['BH'])},
        'BH': {'SP': haversine(coords['BH'], coords['SP']),
               'RJ': haversine(coords['BH'], coords['RJ'])}
    }
    
    # Converte coordenadas para formato euclidiano (aproximação)
    euclidean_coords = {
        'SP': (0, 0),
        'RJ': (1, 1),
        'BH': (0.5, 2)
    }
    
    # Testa se A* encontra caminho
    path, cost = a_star(graph, 'SP', 'BH', euclidean_coords)
    
    assert 'SP' in path
    assert 'BH' in path
    assert cost > 0


def test_complete_workflow():
    """Teste completo do fluxo: grafo → coordenadas → A* → resultado"""
    # 1. Cria grafo com WeightedDirectedGraph
    wg = WeightedDirectedGraph()
    
    # 2. Adiciona rede de ruas simulada
    streets = [
        ('Centro', 'Norte', 5),
        ('Centro', 'Sul', 3),
        ('Norte', 'Leste', 4),
        ('Sul', 'Leste', 2),
        ('Leste', 'Destino', 1)
    ]
    
    for origem, destino, peso in streets:
        wg.add_undirected_edge(origem, destino, peso)
    
    # 3. Define coordenadas dos pontos
    coordinates = {
        'Centro': (0, 0),
        'Norte': (0, 3),
        'Sul': (0, -2),
        'Leste': (4, 0),
        'Destino': (5, 0)
    }
    
    # 4. Executa A*
    path, cost = a_star(wg.edges, 'Centro', 'Destino', coordinates)
    
    # 5. Verifica resultado
    assert path[0] == 'Centro'
    assert path[-1] == 'Destino'
    assert cost == 6  # Centro → Sul → Leste → Destino (3+2+1)
    
    # 6. Testa heurística separadamente
    h_dist = heuristic('Centro', 'Destino', coordinates)
    assert h_dist == 5.0  # Distância euclidiana


def test_error_handling():
    """Testa tratamento de erros"""
    # Testa PriorityQueue vazia
    pq = PriorityQueue()
    with pytest.raises(IndexError):
        pq.pop()
    
    with pytest.raises(IndexError):
        pq.peek()
    
    # Testa A* com grafo desconectado
    graph = {'A': {}, 'B': {}}
    coordinates = {'A': (0, 0), 'B': (1, 1)}
    
    path, cost = a_star(graph, 'A', 'B', coordinates)
    assert cost == float('inf')  # Sem caminho possível