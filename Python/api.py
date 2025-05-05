from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
import game
from Python.game import GameState
from Python.player import Player

app = Flask(__name__)
CORS(app)

@app.route("/start_game", methods=["GET"])
def start_game():
    if GameState.get_airports() is None:
        all_airports = db.get_all_airports()
        GameState.cache_airports(all_airports)


@app.route("/get_names", methods=["POST"])
def get_names():
    data = request.get_json()
    player1_name = data.get("player1")
    player2_name = data.get("player2")

    if not player1_name or not player2_name:
        return jsonify({"error": "Both player names are required."}), 400

    start_airport = db.get_airport_info("EFHK")

    player1 = Player(player1_name, start_airport)
    player2 = Player(player2_name, start_airport)

    GameState.set_players(player1, player2)

    return jsonify({
        "message": "Players created successfully",
        "players": [player1.name, player2.name],
        "starting_airport": start_airport
    }), 200


@app.route("/get_airport_info", methods=["GET"])
def get_every_airport():
    airports = db.get_all_airports()

    return jsonify(airports), 200

@app.route("/get_player_destination", methods=["POST"])
def get_player_destination():
    data = request.json
    destination = data

    return jsonify({"message": "Destination recieved"})


@app.route("/closest_airports/<icao>", methods=["GET"])
def closest_airports(icao):
    if not icao:
        return jsonify({"error": "Missing required parameter: icao"}), 400

    result = db.get_closest_airports(icao)

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
