from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
import game


app = Flask(__name__)
CORS(app)

@app.route("/get_airport_info", methods=["GET"])
def get_airport_info():
    airports = game.airports

    return jsonify(airports), 200





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
