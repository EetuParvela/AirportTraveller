from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
import utils as gm
import player

app = Flask(__name__)
CORS(app)

players = {}


@app.route("/get_name", methods=["POST"])
def get_player_names():
    data = request.json
    name1 = data["player1"]
    name2 = data["player2"]

    players["1"] = player.Player(name1)
    players["2"] = player.Player(name2)

    return jsonify({"message": "Names recieved"})


@app.route("/get_player_destination", methods=["POST"])
def get_player_destination():
    data = request.json
    destination = data

    return jsonify({"message": "Destination recieved"})

@app.route("/get_single_airport/<icao>", methods=["GET"])
def airport_info(icao):
    if not icao:
        return jsonify({"error": "Missing required parameter: icao"}), 400

    result = db.get_airport_info(icao)

    return jsonify(result), 200


@app.route("/closest_airports/<icao>", methods=["GET"])
def closest_airports(icao):
    if not icao:
        return jsonify({"error": "Missing required parameter: icao"}), 400

    result = db.get_closest_airports(icao)

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
