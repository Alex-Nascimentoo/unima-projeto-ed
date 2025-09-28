# flask_api_example/main.py
from data import get_osm_data
from flask import Flask, jsonify, request
from grafo import osm_to_adj_list
from Dijkstra import Dijkstra, Graph
from a_star import a_star
from vrp import solve_vrp_dijkstra, solve_vrp_astar
import time


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def home():
    return jsonify(message="Hello, World!")

@app.route("/api/route/astar", methods=["GET"])
def api_route_astar():
    bbox = [-9.6379, -35.7062, -9.6339, -35.7022]
    nodes, ways = get_osm_data(bbox)
    adj_list = osm_to_adj_list(nodes, ways)
    my_graph = Graph(adj_list)

    start_id = request.args.get("start")
    end_id = request.args.get("end")
    if not start_id or not end_id:
        return jsonify(error="start and end node ids required"), 400

    id_to_vertex = {v.value: v for v in adj_list.keys()}
    start = id_to_vertex.get(start_id)
    end = id_to_vertex.get(end_id)
    if not start or not end:
        return jsonify(error="Invalid node ids"), 400

    t0 = time.time()
    result = a_star(my_graph, start, end)
    t1 = time.time()

    return jsonify(
        route=[v.value for v in result.get("path", [])],
        cost=result.get("cost", 0),
        nodes_visited=result.get("nodes_visited", 0),
        elapsed_time=round(t1-t0, 4)
    )

@app.route("/api/optimize-routes", methods=["POST"])
def api_optimize_routes():
    data = request.get_json()
    deliveries = data.get("deliveries")
    if not deliveries or not isinstance(deliveries, list):
        return jsonify(error="deliveries must be a list of node ids"), 400

    bbox = [-9.6379, -35.7062, -9.6339, -35.7022]
    nodes, ways = get_osm_data(bbox)
    adj_list = osm_to_adj_list(nodes, ways)
    my_graph = Graph(adj_list)

    id_to_vertex = {v.value: v for v in adj_list.keys()}
    delivery_vertices = [id_to_vertex.get(str(d)) for d in deliveries]
    if any(v is None for v in delivery_vertices):
        return jsonify(error="Invalid node ids in deliveries"), 400
    
    result_astar = solve_vrp_astar(my_graph, delivery_vertices)
    result_dijkstra = solve_vrp_dijkstra(my_graph, delivery_vertices)
    return jsonify(result_astar, result_dijkstra)

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
