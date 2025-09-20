from unima_projeto_ed import __version__
from unima_projeto_ed.a_star import heuristic, a_star


def test_version():
    assert __version__ == '0.1.0'


def test_heuristic():
    coordinates = {'A': (0, 0), 'B': (3, 4)}
    distance = heuristic('A', 'B', coordinates)
    assert distance == 5.0


def test_a_star():
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'D': 3},
        'C': {'D': 1, 'E': 5},
        'D': {'E': 2},
        'E': {}
    }
    coordinates = {
        'A': (0, 0),
        'B': (1, 1),
        'C': (0, 2),
        'D': (2, 2),
        'E': (3, 3)
    }
    
    path, cost = a_star(graph, 'A', 'E', coordinates)
    assert path == ['A', 'C', 'D', 'E']
    assert cost == 5
