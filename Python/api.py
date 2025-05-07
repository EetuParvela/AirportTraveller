from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
from Python.game import GameState

app = Flask(__name__)
CORS(app)

game_instance = GameState()


@app.route("/start_game", methods=["GET"])
def start_game():
    all_airports = db.get_all_airports()
    game_instance.cache_airports(all_airports)

    return jsonify({
        "airports": game_instance.get_airports()
    }), 200


@app.route("/get_names", methods=["POST"])
def get_names():
    data = request.get_json()
    player1_name = data.get("player1")
    player2_name = data.get("player2")

    if not player1_name or not player2_name:
        return jsonify({"error": "Both player names are required."}), 400

    start_airport = db.get_airport_info("EFHK")

    game_instance.set_players(player1_name, start_airport, player2_name, start_airport)

    return jsonify({
        "message": "Players created successfully",
        "players": [player1_name, player2_name],
        "starting_airport": start_airport
    }), 200


@app.route("/fly_to", methods=["POST"])
def change_player_location():
    data = request.get_json()
    destination = data
    game_instance.fly_to(destination)

    return jsonify({"message": "Player flew to next airport"}), 200

@app.route("/change_player_stats", methods=["POST"])
def change_player_stats():
    data = request.get_json()
    current_player = data["current_player"]
    next_location = data["next_location"]

    game_instance.change_player_stats(current_player, next_location)

@app.route("/change_turn", methods=["GET"])
def change_turn():
    game_instance.check_if_ended()

@app.route("/get_current_player", methods=["GET"])
def get_current_player_info():
    player = game_instance.get_current_player()

    return jsonify(player), 200

@app.route("/get_all_airport_info", methods=["GET"])
def get_every_airport():
    airports = db.get_all_airports()

    return jsonify(airports), 200

@app.route("/get_airports_from_cache", methods=["GET"])
def get_airports_from_cache():
    airports = game_instance.airports

    return jsonify(airports), 200


@app.route("/closest_airports/<icao>", methods=["GET"])
def closest_airports(icao):
    if not icao:
        return jsonify({"error": "Missing required parameter: icao"}), 400

    result = db.get_closest_airports(icao)

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
