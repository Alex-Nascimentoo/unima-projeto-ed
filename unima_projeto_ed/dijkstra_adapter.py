# unima_projeto_ed/dijkstra_adapter.py
from .dijkstra import Dijkstra as Dijkstra_on_WDG
from .weighted_graph import WeightedDirectedGraph

def _dict_to_wdg(graph_dict):
    wdg = WeightedDirectedGraph()
    for u, nbrs in graph_dict.items():
        for v, w in nbrs.items():
            wdg.add_edge(u, v, w)
    return wdg

def dijkstra_adapter(graph_dict, start, goal, _coordinates_unused=None):
    """
    Assinatura compatível com A*: (graph, start, goal, coordinates) -> (path, dist)
    'coordinates' é ignorado para Dijkstra.
    """
    wdg = _dict_to_wdg(graph_dict)
    return Dijkstra_on_WDG(wdg, start, goal)
