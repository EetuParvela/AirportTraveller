from Python.player import Player
import database as db

class GameState:
    def __init__(self):
        self.players = []
        self.airports = None
        self.current_player = 0 # 0 = pelaaja 1, 1 = pelaaja 2

    @classmethod
    def set_players(cls, p1, p2):
        cls.players = [p1, p2]

    @classmethod
    def cache_airports(cls, airport_data):
        cls.airports = airport_data

    @classmethod
    def get_airports(cls):
        return cls.airports

    def get_current_player(self):
        return self.players[self.current_player]

