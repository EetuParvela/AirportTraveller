from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
from Python.game import GameState

app = Flask(__name__)
CORS(app)

game_instance = GameState()


@app.route('/start_game', methods=['GET'])
def start_game():
    data = request.get_json()
    player_name = data['player_name']

    game_instance.start_game(player_name)

    return jsonify({"message": "Name recieved and player created"}), 200


@app.route("/get_player_info", methods=['GET'])
def get_player_info():
    location, money, co2 = game_instance.player.get_player_info()

    return jsonify({
        "location": location,
        "money": money,
        "co2": co2
    }), 200


@app.route('/fly_to', methods=['POST'])
def fly_to():
    data = request.get_json()
    icao = data['icao']

    if game_instance.fly_to(icao):
        if game_instance.is_over():
            return jsonify({
                "message": "Flight successful",
                "game_over": True
            })
        else:
            return jsonify({
                "message": "Flight succesfull",
                "game_over": False
            }), 200
    else:
        return jsonify({"message": "Flight failed. Not enough money",
                        "game_over": False}), 400


@app.route('/get_airports', methods=['GET'])
def get_airports():
    airports = db.get_all_airports()

    return jsonify(airports), 200


@app.route("/work", methods=['GET'])
def work():
    data = request.get_json()
    days = data['days']

    money_gained = game_instance.work(days)

    return jsonify({"message": f"Work completed! Gained ${money_gained}€"}), 200


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
