import time, json, csv, random, pytest
from unima_projeto_ed.Dijkstra import Graph, Vertex, Edge, Dijkstra
from unima_projeto_ed.a_star import a_star

@pytest.fixture
def setup_graph():
    vertices = [Vertex("A"), Vertex("B"), Vertex("C"), Vertex("D"),
                Vertex("E"), Vertex("F"), Vertex("G"), Vertex("H")]
    A, B, C, D, E, F, G, H = vertices

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

    coordinates = {
        A: (0, 0), B: (1, 0), C: (0, 1), D: (-1, 0),
        E: (1, 1), F: (0, 2), G: (-1, 2), H: (1, 2)
    }

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

def salvar_dados_json(dados, arquivo="dados_performance.json"):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def salvar_dados_csv(dados, arquivo="dados_performance.csv"):
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['par', 'algoritmo', 'tempo_segundos', 'start', 'end'])
        
        for i, par in enumerate(dados['pares_teste']):
            start, end = par
            writer.writerow([f"{start}-{end}", 'Dijkstra', dados['tempos_dijkstra'][i], start, end])
            writer.writerow([f"{start}-{end}", 'A_Star', dados['tempos_astar'][i], start, end])

def test_performance_analysis(setup_graph):
    N = 100
    random.seed(42)
    
    vertices_str = [v.value for v in setup_graph['vertices']]
    pares = [random.sample(vertices_str, 2) for _ in range(N)]
    
    tempos_dijkstra = []
    tempos_astar = []
    
    for i, (start, end) in enumerate(pares):
        # Medir tempo do Dijkstra
        inicio = time.perf_counter()
        Dijkstra(setup_graph['graph_obj'], 
                next(v for v in setup_graph['vertices'] if v.value == start), 
                next(v for v in setup_graph['vertices'] if v.value == end))
        fim = time.perf_counter()
        tempo_dijkstra = fim - inicio
        tempos_dijkstra.append(tempo_dijkstra)
        
        # Medir tempo do A*
        inicio = time.perf_counter()
        caminho, distancia = a_star(setup_graph['graph_dict'], start, end, setup_graph['coordinates'])
        fim = time.perf_counter()
        tempo_astar = fim - inicio
        tempos_astar.append(tempo_astar)
        
        if i % 20 == 0:
            print(f"Par {i+1}: {start} -> {end} | Dijkstra: {tempo_dijkstra:.6f}s | A*: {tempo_astar:.6f}s")
    
    # Análise estatística
    media_dijkstra = sum(tempos_dijkstra) / N
    media_astar = sum(tempos_astar) / N
    
    # Preparar dados para exportação
    dados_exportacao = {
        'numero_pares': N,
        'pares_teste': pares,
        'tempos_dijkstra': tempos_dijkstra,
        'tempos_astar': tempos_astar,
        'estatisticas': {
            'dijkstra': {
                'media': media_dijkstra,
                'maximo': max(tempos_dijkstra),
                'minimo': min(tempos_dijkstra),
                'soma': sum(tempos_dijkstra)
            },
            'astar': {
                'media': media_astar,
                'maximo': max(tempos_astar),
                'minimo': min(tempos_astar),
                'soma': sum(tempos_astar)
            },
            'comparacao': {
                'diferenca_media': media_dijkstra - media_astar,
                'razao_media': media_dijkstra / media_astar,
                'ganho_percentual': (1 - media_astar/media_dijkstra) * 100
            }
        },
        'metadata': {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'semente_aleatoria': 42
        }
    }
    
    salvar_dados_json(dados_exportacao)
    salvar_dados_csv(dados_exportacao)
    
    print(f"\n=== DADOS EXPORTADOS ===")
    print(f"Arquivo JSON: dados_performance.json")
    print(f"Arquivo CSV: dados_performance.csv")
    print(f"\n=== RESUMO ===")
    print(f"Pares analisados: {N}")
    print(f"Tempo médio Dijkstra: {media_dijkstra:.6f}s")
    print(f"Tempo médio A*: {media_astar:.6f}s")
    print(f"Ganho do A*: {dados_exportacao['estatisticas']['comparacao']['ganho_percentual']:.1f}%")
    
    assert media_astar > 0
    assert media_dijkstra > 0
    assert len(tempos_dijkstra) == N
    assert len(tempos_astar) == N

def test_specific_pairs_analysis(setup_graph):
    pares_especificos = [("A", "H"), ("B", "G"), ("C", "F"), ("D", "E"), ("A", "G")]
    
    resultados_detalhados = []
    
    for start, end in pares_especificos:
        tempos_dijkstra = []
        tempos_astar = []
        
        for _ in range(5):
            # Dijkstra
            inicio = time.perf_counter()
            Dijkstra(setup_graph['graph_obj'], 
                    next(v for v in setup_graph['vertices'] if v.value == start), 
                    next(v for v in setup_graph['vertices'] if v.value == end))
            tempos_dijkstra.append(time.perf_counter() - inicio)
            
            # A*
            inicio = time.perf_counter()
            caminho, distancia = a_star(setup_graph['graph_dict'], start, end, setup_graph['coordinates'])
            tempos_astar.append(time.perf_counter() - inicio)
        
        resultados_detalhados.append({
            'par': f"{start}-{end}",
            'dijkstra_media': sum(tempos_dijkstra) / len(tempos_dijkstra),
            'astar_media': sum(tempos_astar) / len(tempos_astar),
            'dijkstra_detalhes': tempos_dijkstra,
            'astar_detalhes': tempos_astar
        })
    
    with open('dados_pares_especificos.json', 'w', encoding='utf-8') as f:
        json.dump(resultados_detalhados, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== DADOS PARES ESPECÍFICOS EXPORTADOS ===")
    print(f"Arquivo: dados_pares_especificos.json")
    
    for resultado in resultados_detalhados:
        print(f"{resultado['par']}: Dijkstra={resultado['dijkstra_media']:.6f}s, A*={resultado['astar_media']:.6f}s")
    
    # Asserts
    assert len(resultados_detalhados) == len(pares_especificos)

def test_algorithm_correctness(setup_graph):
    """Teste para verificar que ambos algoritmos encontram caminhos válidos"""
    pares_teste = [("A", "H"), ("B", "G"), ("C", "F")]
    
    for start, end in pares_teste:
        # A* deve encontrar um caminho
        caminho, distancia = a_star(setup_graph['graph_dict'], start, end, setup_graph['coordinates'])
        
        assert len(caminho) > 0
        assert caminho[0] == start
        assert caminho[-1] == end
        assert distancia < float('inf')

        try:
            Dijkstra(setup_graph['graph_obj'], 
                    next(v for v in setup_graph['vertices'] if v.value == start), 
                    next(v for v in setup_graph['vertices'] if v.value == end))
            assert True
        except Exception:
            assert False, "Dijkstra falhou na execução"