# unima_projeto_ed/grafo.py

from .utils import haversine  # distancia em km

def osm_to_adj_list(nodes, ways):
    """
    Converte dados do OSM em lista de adjacência no formato:
      { node_id: { vizinho_id: peso_km, ... }, ... }

    Parâmetros:
      nodes: dict {node_id: (lat, lon)}
      ways:  list de listas [ [node_id1, node_id2, ...], ... ]

    Retorna:
      adj_list: dict adequado para o teu A* (graph[current].items())
    """
    # inicializa cada nó com um dicionário de vizinhos
    adj_list = {nid: {} for nid in nodes}

    # para cada "way", liga nós consecutivos (bidirecional)
    for way in ways:
        for i in range(len(way) - 1):
            n1, n2 = way[i], way[i + 1]
            # ignora pares que não estejam no dict nodes (sanidade)
            if n1 not in nodes or n2 not in nodes:
                continue

            lat1, lon1 = nodes[n1]
            lat2, lon2 = nodes[n2]

            # distância em quilômetros (sem dividir por 100000)
            dist_km = haversine(lat1, lon1, lat2, lon2)

            # como muitas ruas são mão dupla, colocamos dos dois lados
            # se já existir uma aresta, mantém o menor custo
            prev12 = adj_list[n1].get(n2)
            prev21 = adj_list[n2].get(n1)
            if prev12 is None or dist_km < prev12:
                adj_list[n1][n2] = dist_km
            if prev21 is None or dist_km < prev21:
                adj_list[n2][n1] = dist_km

    return adj_list
