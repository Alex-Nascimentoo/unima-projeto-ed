from flask import Flask, jsonify
from .data import get_osm_data
from .grafo import osm_to_adj_list
from .cvrp import Delivery, nearest_neighbor_cvrp

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/")
def home():
    return jsonify(message="API de Roteamento pronta!")


def start():
    app.run()


if __name__ == "__main__":
    # -----------------------------
    # 1. Definir a área de estudo
    # -----------------------------
    # Bounding Box de Maceió (ajuste se quiser maior/menor área)
    bbox = [-9.6379, -35.7062, -9.6339, -35.7022]

    # -----------------------------
    # 2. Buscar dados do OSM
    # -----------------------------
    nodes, ways = get_osm_data(bbox)

    # nodes: {node_id: (lat, lon)}
    # ways: lista de sequências de nós conectados

    # -----------------------------
    # 3. Montar o grafo
    # -----------------------------
    # Aqui ajustei o osm_to_adj_list para devolver:
    # {node: {vizinho: peso, ...}}
    graph = osm_to_adj_list(nodes, ways)
    coordinates = nodes  # usado na heurística do A*

    # -----------------------------
    # 4. Definir depósito e clientes
    # -----------------------------
    depot = list(graph.keys())[0]  # escolhe o primeiro nó como depósito

    deliveries = [
        Delivery("C1", list(graph.keys())[1], 2),
        Delivery("C2", list(graph.keys())[2], 1),
        Delivery("C3", list(graph.keys())[3], 2),
    ]

    # Capacidade máxima do veículo
    capacity = 3

    # -----------------------------
    # 5. Resolver CVRP
    # -----------------------------
    routes, total_distance = nearest_neighbor_cvrp(graph, coordinates, deliveries, capacity, depot)

    # -----------------------------
    # 6. Exibir resultado
    # -----------------------------
    print("\nRotas geradas (Vizinho Mais Próximo + A*):")
    for idx, r in enumerate(routes, start=1):
        print(f"Rota {idx}: {' -> '.join(str(x) for x in r)}")
    print("Distância total:", total_distance)
