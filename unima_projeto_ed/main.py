# flask_api_example/main.py
from grafo import build_graph
from data import get_osm_data
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def home():
    return jsonify(message="Hello, World!")

def start():
    app.run()


if __name__ == "__main__":
    # UNIMA Afya | Maceió-AL
    # sul, oeste, norte, leste
    bbox = [-9.6379, -35.7062, -9.6339, -35.7022]

    nodes, ways = get_osm_data(bbox)
    print("Nós:", len(nodes), "Ways:", len(ways))
    G = build_graph(nodes, ways)
    print("Grafo:", len(G.nodes), "Nós,", len(G.edges), "Arestas")