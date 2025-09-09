# flask_api_example/main.py

from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def home():
    return jsonify(message="Hello, World!")

def start():
    app.run()