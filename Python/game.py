from Python.player import Player
import database as db


class GameState:
    def __init__(self):
        self.players = []
        self.current_player = 0  # 0 on pelaaja 1, 1 on pelaaja 2
        self.multiplier = 1
        self.player1 = None
        self.player2 = None
        self.airports = None
        self.is_over = 0

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

    def get_current_player_stats(self):
        current_player = self.get_current_player()
        return self.players[current_player].get_stats()

    def fly_to(self, destination):
        self.change_player_stats(self.players[self.current_player], destination)

    def handle_bonus(self, dice):
        self.multiplier = 2

    # Vaihtaa pelaajien välillä
    def change_current_player(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

    def change_player_stats(self, player, next_location):
        current_player = self.players[player]

        distance = db.calculate_distance((current_player["current_airport"]["latitude_deg"],
                                          current_player["current_airport"]["longitude_deg"]),
                                         (next_location["latitude_deg"],
                                          next_location["longitude_deg"]))

        points, fuel, co2 = self.calculate_info(distance, 1)
        player.update_score(points)
        player.update_fuel(fuel)
        player.update_co2(co2)

    def calculate_info(self, distance):
        cruise_speed = 833
        fuel_consumption = 889.571769
        fuel_used = (distance / cruise_speed) * fuel_consumption

        co2_per_l = 2.52
        co2_emitted = fuel_used * co2_per_l

        if self.multiplier == 2:
            earned_points = distance * (0.1 + distance / 1000) * 2
            self.multiplier = 1
        else:
            earned_points = distance * (0.1 + distance / 1000) * 1

        return earned_points, fuel_used, co2_emitted
