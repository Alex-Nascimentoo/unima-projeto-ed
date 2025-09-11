import requests

def get_osm_data(bbox):
    """
    Consulta a Overpass API para buscar ruas e cruzamentos dentro de um bounding box.
    bbox: [sul, oeste, norte, leste]
    Retorna: lista de nós e lista de caminhos
    """
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:25];
    way["highway"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    (._;>;);
    out body;
    """
    
    response = requests.get(overpass_url, params={'data': query})
    response.raise_for_status()
    data = response.json()
    
    # Separar nós e ways
    nodes = {}
    ways = []
    
    for el in data['elements']:
        if el['type'] == 'node':
            nodes[el['id']] = (el['lat'], el['lon'])
        elif el['type'] == 'way':
            ways.append(el['nodes'])
    
    return nodes, ways
