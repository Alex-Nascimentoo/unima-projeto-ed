import pytest
from unittest.mock import patch, MagicMock
from unima_projeto_ed import data, grafo, main

def test_haversine():
    coord1 = (-9.6379, -35.7062)
    coord2 = (-9.6379, -35.7063)
    distance = grafo.haversine(coord1, coord2)
    assert distance > 0
    assert distance < 20
    assert grafo.haversine(coord1, coord1) == 0

def test_build_graph():
    nodes = {
        1: (-9.6379, -35.7062),
        2: (-9.6378, -35.7062),
        3: (-9.6377, -35.7062)
    }
    ways = [[1, 2], [2, 3]]
    
    G = grafo.build_graph(nodes, ways)
    
    assert len(G.nodes) == 3
    assert len(G.edges) == 4
    assert G.has_edge(1, 2)
    assert G.has_edge(2, 1)
    assert G.has_edge(2, 3)
    assert G.has_edge(3, 2)

@patch('unima_projeto_ed.data.requests.get')
def test_get_osm_data(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'elements': [
            {'type': 'node', 'id': 1, 'lat': -9.6379, 'lon': -35.7062},
            {'type': 'node', 'id': 2, 'lat': -9.6378, 'lon': -35.7062},
            {'type': 'way', 'nodes': [1, 2]}
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    bbox = [-9.6379, -35.7062, -9.6339, -35.7022]
    nodes, ways = data.get_osm_data(bbox)
    
    assert len(nodes) == 2
    assert len(ways) == 1
    assert 1 in nodes
    assert 2 in nodes
    assert ways[0] == [1, 2]

def test_flask_home_route():
    with main.app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.json == {'message': 'Hello, World!'}

def test_graph_connectivity():
    nodes = {
        1: (-9.6379, -35.7062),
        2: (-9.6378, -35.7062),
        3: (-9.6377, -35.7062),
        4: (-9.6376, -35.7062)
    }
    ways = [[1, 2], [2, 3]]
    
    G = grafo.build_graph(nodes, ways)
    
    assert G.has_edge(1, 2)
    assert G.has_edge(2, 3)
    assert not G.has_edge(3, 4)

def test_edge_weights():
    nodes = {
        1: (-9.6379, -35.7062),
        2: (-9.6378, -35.7062)
    }
    ways = [[1, 2]]
    
    G = grafo.build_graph(nodes, ways)
    
    weight = G[1][2]['weight']
    assert 100 < weight < 120

@patch('unima_projeto_ed.data.requests.get')
def test_osm_api_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_get.return_value = mock_response
    
    with pytest.raises(Exception):
        data.get_osm_data([-9.6379, -35.7062, -9.6339, -35.7022])
