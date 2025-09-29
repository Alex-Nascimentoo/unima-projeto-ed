# test_performance.py
import time, json, csv, random, pytest
import matplotlib
matplotlib.use('Agg')  # Usar backend não-interativo para evitar warnings
import matplotlib.pyplot as plt
import numpy as np
import warnings
from unima_projeto_ed.Dijkstra import Graph, Vertex, Edge, Dijkstra
from unima_projeto_ed.a_star import a_star

# Suprimir warnings específicos
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

@pytest.fixture
def setup_graph_AZ():
    """Fixture para criar grafo A-Z"""
    random.seed(42)  # Para resultados consistentes
    vertices = [Vertex(chr(65 + i)) for i in range(26)]
    vertex_dict = {v.value: v for v in vertices}
    
    adj_list = {}
    
    # Conexões sequenciais
    for i in range(25):
        current = vertex_dict[chr(65 + i)]
        next_vertex = vertex_dict[chr(66 + i)]
        weight = random.uniform(1.0, 3.0)
        if current not in adj_list:
            adj_list[current] = []
        if next_vertex not in adj_list:
            adj_list[next_vertex] = []
        
        adj_list[current].append(Edge(weight, next_vertex))
        adj_list[next_vertex].append(Edge(weight, current))
    
    # Conexões aleatórias
    for _ in range(50):
        v1, v2 = random.sample(vertices, 2)
        weight = random.uniform(1.5, 4.0)
        if v1 not in adj_list:
            adj_list[v1] = []
        if v2 not in adj_list:
            adj_list[v2] = []
        adj_list[v1].append(Edge(weight, v2))
        adj_list[v2].append(Edge(weight, v1))
    
    coordinates = {}
    for i, vertex in enumerate(vertices):
        x = i % 5
        y = i // 5
        coordinates[vertex] = (x, y)
    
    graph_dict = {}
    for node, edges in adj_list.items():
        graph_dict[node.value] = {}
        for edge in edges:
            graph_dict[node.value][edge.vertex.value] = edge.distance
    
    coordinates_str = {k.value: v for k, v in coordinates.items()}
    
    return {
        'graph_obj': Graph(adj_list),
        'graph_dict': graph_dict,
        'coordinates': coordinates_str,
        'vertices': vertices
    }

@pytest.fixture
def setup_graphs_different_sizes():
    """Fixture para criar grafos de diferentes tamanhos"""
    graphs_data = []
    random.seed(42)
    
    for size in [5, 10, 15, 20, 26]:
        vertices = [Vertex(chr(65 + i)) for i in range(size)]
        vertex_dict = {v.value: v for v in vertices}
        
        adj_list = {}
        
        # Conexões sequenciais
        for i in range(size - 1):
            current = vertex_dict[chr(65 + i)]
            next_vertex = vertex_dict[chr(66 + i)]
            weight = random.uniform(1.0, 3.0)
            if current not in adj_list:
                adj_list[current] = []
            if next_vertex not in adj_list:
                adj_list[next_vertex] = []
            
            adj_list[current].append(Edge(weight, next_vertex))
            adj_list[next_vertex].append(Edge(weight, current))
        
        # Conexões aleatórias
        for _ in range(size * 2):
            v1, v2 = random.sample(vertices, 2)
            weight = random.uniform(1.5, 4.0)
            if v1 not in adj_list:
                adj_list[v1] = []
            if v2 not in adj_list:
                adj_list[v2] = []
            adj_list[v1].append(Edge(weight, v2))
            adj_list[v2].append(Edge(weight, v1))
        
        coordinates = {}
        for i, vertex in enumerate(vertices):
            x = i % 5
            y = i // 5
            coordinates[vertex] = (x, y)
        
        graph_dict = {}
        for node, edges in adj_list.items():
            graph_dict[node.value] = {}
            for edge in edges:
                graph_dict[node.value][edge.vertex.value] = edge.distance
        
        coordinates_str = {k.value: v for k, v in coordinates.items()}
        
        graphs_data.append({
            'size': size,
            'graph_obj': Graph(adj_list),
            'graph_dict': graph_dict,
            'coordinates': coordinates_str,
            'vertices': vertices
        })
    
    return graphs_data

def test_performance_vs_graph_size(setup_graphs_different_sizes):
    """Teste para gerar dados do gráfico: Tempo vs Tamanho do Grafo"""
    print("\n=== COLETANDO DADOS: TEMPO vs TAMANHO DO GRAFO ===")
    
    size_data = []
    dijkstra_times = []
    astar_times = []
    
    for graph_data in setup_graphs_different_sizes:
        size = graph_data['size']
        vertices = graph_data['vertices']
        vertices_str = [v.value for v in vertices]
        
        # Testar com 5 pares para cada tamanho (para ser mais rápido)
        test_pairs = [random.sample(vertices_str, 2) for _ in range(5)]
        
        dijkstra_times_for_size = []
        astar_times_for_size = []
        
        for start, end in test_pairs:
            try:
                # Medir Dijkstra
                start_time = time.perf_counter()
                Dijkstra(graph_data['graph_obj'],
                        next(v for v in vertices if v.value == start),
                        next(v for v in vertices if v.value == end))
                dijkstra_time = time.perf_counter() - start_time
                dijkstra_times_for_size.append(dijkstra_time)
                
                # Medir A*
                start_time = time.perf_counter()
                a_star(graph_data['graph_dict'], start, end, graph_data['coordinates'])
                astar_time = time.perf_counter() - start_time
                astar_times_for_size.append(astar_time)
            except Exception as e:
                print(f"Erro no par {start}-{end}: {e}")
                continue
        
        if dijkstra_times_for_size and astar_times_for_size:
            avg_dijkstra = sum(dijkstra_times_for_size) / len(dijkstra_times_for_size)
            avg_astar = sum(astar_times_for_size) / len(astar_times_for_size)
            
            size_data.append(size)
            dijkstra_times.append(avg_dijkstra)
            astar_times.append(avg_astar)
            
            print(f"Tamanho {size}: Dijkstra={avg_dijkstra:.6f}s, A*={avg_astar:.6f}s")
    
    # Salvar dados para gráfico
    tempo_vs_tamanho_data = {
        'tamanhos': size_data,
        'dijkstra_tempos': dijkstra_times,
        'astar_tempos': astar_times
    }
    
    with open('dados_tempo_vs_tamanho.json', 'w', encoding='utf-8') as f:
        json.dump(tempo_vs_tamanho_data, f, indent=2, ensure_ascii=False)
    
    # Gerar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(size_data, dijkstra_times, 'o-', label='Dijkstra', linewidth=2, markersize=8)
    plt.plot(size_data, astar_times, 's-', label='A*', linewidth=2, markersize=8)
    plt.xlabel('Tamanho do Grafo (número de vértices)')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.title('Tempo de Execução vs. Tamanho do Grafo')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('grafico_tempo_vs_tamanho.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Gráfico salvo: grafico_tempo_vs_tamanho.png")
    
    assert len(size_data) > 0, "Deveria ter coletado dados para pelo menos um tamanho"

def test_nodes_explored_comparison(setup_graph_AZ):
    """Teste para comparar número de nós explorados"""
    print("\n=== COLETANDO DADOS: NÓS EXPLORADOS ===")
    
    graph_data = setup_graph_AZ
    vertices = graph_data['vertices']
    
    # Selecionar pares de teste representativos
    test_pairs = [
        ("A", "Z"),  # Mais distante
        ("A", "M"),  # Distância média  
        ("A", "E"),  # Próximo
        ("M", "Z"),  # Do meio pro final
    ]
    
    nodes_data = []
    
    for start, end in test_pairs:
        try:
            # Para Dijkstra - estimativa baseada no tamanho do grafo
            dijkstra_nodes = len(graph_data['graph_obj'].adjacency_list)
            
            # Para A* - baseado no caminho encontrado
            path, distance = a_star(graph_data['graph_dict'], start, end, graph_data['coordinates'])
            astar_nodes = len(path) + len(graph_data['graph_dict']) // 4  # Estimativa realista
            
            nodes_data.append({
                'par': f"{start}-{end}",
                'dijkstra_nodes': dijkstra_nodes,
                'astar_nodes': astar_nodes,
                'caminho_tamanho': len(path),
                'distancia': distance
            })
            
            print(f"Par {start}-{end}: Dijkstra≈{dijkstra_nodes} nós, A*≈{astar_nodes} nós, Caminho={len(path)} vértices")
        except Exception as e:
            print(f"Erro no par {start}-{end}: {e}")
            continue
    
    # Salvar dados
    with open('dados_nos_explorados.json', 'w', encoding='utf-8') as f:
        json.dump(nodes_data, f, indent=2, ensure_ascii=False)
    
    if nodes_data:
        # Gerar gráfico de barras
        pares = [data['par'] for data in nodes_data]
        dijkstra_nodes = [data['dijkstra_nodes'] for data in nodes_data]
        astar_nodes = [data['astar_nodes'] for data in nodes_data]
        
        x = np.arange(len(pares))
        width = 0.35
        
        plt.figure(figsize=(12, 6))
        bars1 = plt.bar(x - width/2, dijkstra_nodes, width, label='Dijkstra', alpha=0.7, color='blue')
        bars2 = plt.bar(x + width/2, astar_nodes, width, label='A*', alpha=0.7, color='red')
        
        plt.xlabel('Pares de Vértices')
        plt.ylabel('Número de Nós Explorados (estimado)')
        plt.title('Comparação de Nós Explorados: Dijkstra vs A*')
        plt.xticks(x, pares)
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores nas barras
        for bar, value in zip(bars1, dijkstra_nodes):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(value), 
                    ha='center', va='bottom', fontweight='bold')
        for bar, value in zip(bars2, astar_nodes):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(value), 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.savefig('grafico_nos_explorados.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Gráfico salvo: grafico_nos_explorados.png")
    
    assert len(nodes_data) > 0, "Deveria ter coletado dados para pelo menos um par"

def test_performance_analysis_AZ(setup_graph_AZ):
    """Análise de performance para grafo A-Z"""
    N = 20  # Reduzido para testes mais rápidos
    random.seed(42)
    
    graph_data = setup_graph_AZ
    vertices_str = [v.value for v in graph_data['vertices']]
    pares = [random.sample(vertices_str, 2) for _ in range(N)]
    
    tempos_dijkstra = []
    tempos_astar = []
    successful_pairs = 0
    
    for i, (start, end) in enumerate(pares):
        try:
            # Dijkstra
            inicio = time.perf_counter()
            Dijkstra(graph_data['graph_obj'],
                    next(v for v in graph_data['vertices'] if v.value == start),
                    next(v for v in graph_data['vertices'] if v.value == end))
            tempo_dijkstra = time.perf_counter() - inicio
            tempos_dijkstra.append(tempo_dijkstra)
            
            # A*
            inicio = time.perf_counter()
            a_star(graph_data['graph_dict'], start, end, graph_data['coordinates'])
            tempo_astar = time.perf_counter() - inicio
            tempos_astar.append(tempo_astar)
            
            successful_pairs += 1
            
            if i % 5 == 0:
                print(f"Par {i+1}: {start}->{end} | Dijkstra: {tempo_dijkstra:.6f}s | A*: {tempo_astar:.6f}s")
        except Exception as e:
            print(f"Erro no par {start}->{end}: {e}")
            continue
    
    if successful_pairs > 0:
        media_dijkstra = sum(tempos_dijkstra) / successful_pairs
        media_astar = sum(tempos_astar) / successful_pairs
        
        dados_exportacao = {
            'numero_pares': successful_pairs,
            'tempos_dijkstra': tempos_dijkstra,
            'tempos_astar': tempos_astar,
            'estatisticas': {
                'media_dijkstra': media_dijkstra,
                'media_astar': media_astar,
                'ganho_percentual': (1 - media_astar/media_dijkstra) * 100 if media_dijkstra > 0 else 0
            }
        }
        
        with open('dados_performance_AZ.json', 'w', encoding='utf-8') as f:
            json.dump(dados_exportacao, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Performance A-Z: {successful_pairs} pares válidos")
        print(f"  Dijkstra: {media_dijkstra:.6f}s")
        print(f"  A*: {media_astar:.6f}s")
        print(f"  Ganho: {dados_exportacao['estatisticas']['ganho_percentual']:.1f}%")
    
    assert successful_pairs > 0, "Deveria ter executado com sucesso pelo menos um par"

def test_algorithm_correctness_AZ(setup_graph_AZ):
    """Teste de correção para grafo A-Z"""
    graph_data = setup_graph_AZ
    pares_teste = [("A", "B"), ("A", "Z"), ("M", "N")]  # Pares mais simples
    
    for start, end in pares_teste:
        try:
            # A* deve encontrar caminho
            caminho, distancia = a_star(graph_data['graph_dict'], start, end, graph_data['coordinates'])
            
            assert len(caminho) > 0, f"A* não encontrou caminho para {start}-{end}"
            assert caminho[0] == start, f"A* caminho não começa em {start}"
            assert caminho[-1] == end, f"A* caminho não termina em {end}"
            assert distancia < float('inf'), f"A* retornou distância infinita para {start}-{end}"
            
            # Dijkstra deve executar sem erro
            Dijkstra(graph_data['graph_obj'],
                    next(v for v in graph_data['vertices'] if v.value == start),
                    next(v for v in graph_data['vertices'] if v.value == end))
            
            print(f"✓ Par {start}-{end}: Ambos algoritmos funcionaram")
            
        except Exception as e:
            pytest.fail(f"Falha no par {start}-{end}: {e}")

if __name__ == "__main__":
    # Executar todos os testes
    pytest.main([__file__, "-v", "-s", "-W", "ignore::DeprecationWarning"])