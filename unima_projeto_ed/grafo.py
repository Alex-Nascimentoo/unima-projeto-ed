import math
from data import get_osm_data
from Dijkstra import Vertex, Edge

def haversine(lat1, lon1, lat2, lon2):
    # Calcula a distância entre dois pontos geográficos (em km)
    R = 6371  # raio da Terra em km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def osm_to_adj_list(nodes, ways):
    # Cria Vertex para cada nó
    id_to_vertex = {nid: Vertex(str(nid)) for nid in nodes}
    adj_list = {v: [] for v in id_to_vertex.values()}

    # Para cada caminho (way), conecta os nós consecutivos
    for way in ways:
        for i in range(len(way)-1):
            n1, n2 = way[i], way[i+1]
            v1, v2 = id_to_vertex[n1], id_to_vertex[n2]
            lat1, lon1 = nodes[n1]
            lat2, lon2 = nodes[n2]
            dist = haversine(lat1, lon1, lat2, lon2) / 100000
            adj_list[v1].append(Edge(dist, v2))
            adj_list[v2].append(Edge(dist, v1))  # bidirecional

    return adj_list
