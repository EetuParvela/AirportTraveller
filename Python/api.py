from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
from Python.game import GameState

app = Flask(__name__)
CORS(app)

game_instance = GameState()

@app.route("/reset_player_stats", methods=["GET"])
def reset_stats():
    game_instance.player.reset_stats()

    return jsonify({"message": "Player stats reset"})


@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    player_name = data['player_name']

    game_instance.start_game(player_name)

    return jsonify({"message": "Name recieved and player created"}), 200


@app.route("/get_player_info", methods=['GET'])
def get_player_info():
    name, location, money, co2, score, places_visited = game_instance.player.get_player_stats()
    days = game_instance.days
    print(location)

    return jsonify({
        "name": name,
        "location": location,
        "money": money,
        "co2": co2,
        "score": score,
        "places_visited": places_visited,
        "days": days
    }), 200


@app.route('/fly_to', methods=['POST'])
def fly_to():
    data = request.get_json()
    icao = data['icao']['icao']

    if game_instance.fly_to(icao):
        if game_instance.is_over():
            return jsonify({
                "message": "Flight successful",
                "can_fly": True,
                "game_over": True
            }), 200
        else:
            return jsonify({
                "message": "Flight succesful",
                "can_fly": True,
                "game_over": False
            }), 200
    else:
        return jsonify({"message": "Flight failed. Not enough money",
                        "can_fly": False,
                        "game_over": False}), 200


@app.route('/get_airports', methods=['GET'])
def get_airports():
    airports = db.get_all_airports()

    return jsonify(airports), 200


@app.route("/work", methods=['POST'])
def work():
    data = request.get_json()
    days = data['days']

    money_gained = game_instance.work(days)
    print(money_gained)

    return jsonify({"message": f"Work completed! Gained ${money_gained}€"}), 200


@app.route('/get_highscore', methods=['GET'])
def get_highscore_route():
    scoreboard = db.get_highscore()
    print(scoreboard)

    return jsonify(scoreboard), 200

@app.route("/update_database_highscore", methods=["GET"])
def update_highscore():
    with db.get_db_connection() as conn:
        with db.get_db_cursor(conn) as cursor:
            player_name = game_instance.player.name
            points = game_instance.player.score

            query = "INSERT INTO highscore (player, points) VALUES (%s, %s);"
            cursor.execute(query, (player_name, points))
        conn.commit()

    return jsonify(), 200

@app.route('/get_distance', methods=['GET']) # lähetetään etäisyys lennon hinnan laskettamiseksi
def get_distance():
    icao = request.args.get('icao')
    distance = game_instance.get_distance(icao)
    return jsonify({'distance': distance}), 200


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
