# flask_api_example/main.py
from data import get_osm_data
from flask import Flask, jsonify
from grafo import osm_to_adj_list
from Dijkstra import Dijkstra, Graph

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
    adj_list = osm_to_adj_list(nodes, ways)
    my_graph = Graph(adj_list)
    
    start = list(adj_list.keys())[0]
    end = list(adj_list.keys())[-1]
    Dijkstra(my_graph, start, end)
   