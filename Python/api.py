from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
import game_manager as gm
import game
from game import player_data, destination

app = Flask(__name__)


@app.route("/get_name", methods=["POST"])
def get_names():
    data = request.get_json()
    player_data["player1"] = data.get('uname1')
    player_data["player2"] = data.get('uname2')

    return jsonify({"message": "Players recieved"}), 200


@app.route("/get_airport_info", methods=["GET"])
def get_airport_info():
    airports = game.airports

    return jsonify(airports), 200


@app.route("/fly_to", methods=["POST"])
def fly_to():
    data = request.get_json()
    destination["airport"] = data["destination"]

    return jsonify({"message": "Destination recieved"}), 200


@app.route("/closest_airports/<icao>", methods=["GET"])
def closest_airports(icao):
    if not icao:
        return jsonify({"error": "Missing required parameter: icao"}), 400

    result = db.get_closest_airports(icao)

    return jsonify(result), 200


@app.route("/get_airport_info/<icao>", methods=["GET"])
def airport_info(icao):
    if not icao:
        return jsonify({"error": "Missing required parameter: icao"}), 400

    result = db.get_airport_info(icao)

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
