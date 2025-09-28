from flask import Flask, jsonify
from .data import get_osm_data
from .grafo import osm_to_adj_list
from .cvrp import Delivery, nearest_neighbor_cvrp
from .queue import Queue  # Fila FIFO manual (implementada por você)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ---------------------------------------------
# API Flask
# ---------------------------------------------

@app.route("/")
def home():
    return jsonify(message="API de Roteamento pronta!")

def start():
    """Sobe a API Flask."""
    app.run()

# ---------------------------------------------
# Execução em modo batch (CLI)
# ---------------------------------------------

def run_batch(sp="a_star"):
    # 1) Área de estudo (bbox de Maceió)
    bbox = [-9.6379, -35.7062, -9.6339, -35.7022]

    # 2) Buscar dados do OSM
    nodes, ways = get_osm_data(bbox)

    # 3) Montar o grafo (dict de adjacência) e coordenadas
    graph = osm_to_adj_list(nodes, ways)
    coordinates = nodes  # usado na heurística do A*

    # Sanity check
    keys = list(graph.keys())
    if len(keys) < 4:
        raise RuntimeError("Área muito pequena: menos de 4 nós para montar o exemplo.")

    # 4) Depósito e clientes (usando FILA FIFO explícita)
    depot = keys[0]  # escolhe o primeiro nó como depósito

    # Enfileira pedidos na ordem de chegada (FIFO manual)
    pedidos = Queue()
    pedidos.enqueue(("C1", keys[1], 2))
    pedidos.enqueue(("C2", keys[2], 1))
    pedidos.enqueue(("C3", keys[3], 2))

    # Consome a fila em ordem e monta as entregas
    deliveries = []
    while not pedidos.is_empty():
        cid, node, demand = pedidos.dequeue()
        deliveries.append(Delivery(cid, node, demand))

    # Capacidade do veículo
    capacity = 3

    # 5) Resolver CVRP (usando A* ou Dijkstra conforme 'sp')
    routes, total_distance = nearest_neighbor_cvrp(
        graph, coordinates, deliveries, capacity, depot, sp=sp
    )

    # 6) Exibir resultado
    print(f"\nRotas geradas (Vizinho Mais Próximo + {sp.upper()}):")
    for idx, r in enumerate(routes, start=1):
        print(f"Rota {idx}: {' -> '.join(str(x) for x in r)}")
    print("Distância total (km):", total_distance)

# ---------------------------------------------
# Escolha do modo (API vs batch)
# ---------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Roteamento: API Flask ou execução batch (CVRP)."
    )
    parser.add_argument(
        "--mode",
        choices=["api", "batch"],
        default="batch",
        help="Escolha 'api' para Flask ou 'batch' para executar o CVRP (default: batch).",
    )
    parser.add_argument(
        "--sp",
        choices=["a_star", "dijkstra"],
        default="a_star",
        help="Algoritmo de menor caminho na matriz (default: a_star).",
    )
    args = parser.parse_args()

    if args.mode == "api":
        start()
    else:
        run_batch(sp=args.sp)
