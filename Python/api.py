from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db

app = Flask(__name__)
CORS(app)


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
