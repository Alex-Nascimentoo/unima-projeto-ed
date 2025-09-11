from math import radians, cos, sin, asin, sqrt
import networkx as nx

# Função para calcular a distância haversine entre dois pontos geográficos
def haversine(coord1, coord2): 
    # Distância em metros entre duas coordenadas (lat, lon).
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371000  # raio da Terra em metros
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def build_graph(nodes, ways):
    G = nx.DiGraph()
    for way in ways:
        for i in range(len(way) - 1):
            n1, n2 = way[i], way[i+1]
            if n1 in nodes and n2 in nodes:
                dist = haversine(nodes[n1], nodes[n2])
                G.add_edge(n1, n2, weight=dist)
                G.add_edge(n2, n1, weight=dist)  
    return G
