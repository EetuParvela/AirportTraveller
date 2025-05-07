from Python.player import Player
import database as db


class GameState:
    def __init__(self):
        self.players = []
        self.current_player = 0  # 0 on pelaaja 1, 1 on pelaaja 2
        self.player1 = None
        self.player2 = None
        self.airports = None
        self.is_over = False

    def cache_airports(self, airport_data):
        self.airports = airport_data

    def get_airports(self):
        return self.airports

    def get_current_player(self):
        return self.current_player

    def set_players(self, p1, p1_start, p2, p2_start):
        self.player1 = Player(p1, p1_start)
        self.player2 = Player(p2, p2_start)
        self.players.append(self.player1)  # Pelaaja 1 on indeksi 0
        self.players.append(self.player2)  # Pelaaja 2 on indeksi 1

    def fly_to(self, destination):
        self.change_player_stats(self.players[self.current_player], destination)

    # Vaihtaa pelaajien välillä
    def change_current_player(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

    # Vaihtaa vuoron toiselle pelaajalle
    def end_turn(self):
        self.change_current_player()

    # Tarkistaa onko peli loppunut
    def check_if_ended(self):
        if self.is_over:
            return True
        else:
            return False

    @staticmethod
    def change_player_stats(player, next_location):
        distance = db.calculate_distance((player.current_airport["latitude_deg"],
                                          player.current_airport["longitude_deg"]),
                                         (next_location["latitude_deg"],
                                          next_location["longitude_deg"]))

        points, fuel, co2 = calculate_info(distance, 1)
        player.update_score(points)
        player.update_fuel(fuel)
        player.update_co2(co2)

    @staticmethod
    def get_next_airport(next_airport):
        destination = next_airport


def calculate_info(distance, multiplier):
    cruise_speed = 833
    fuel_consumption = 889.571769
    fuel_used = (distance / cruise_speed) * fuel_consumption

    co2_per_l = 2.52
    co2_emitted = fuel_used * co2_per_l

    earned_points = distance * (0.1 + distance / 1000) * multiplier

    return earned_points, fuel_used, co2_emitted
