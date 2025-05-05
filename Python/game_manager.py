from player import Player
from game import Peli

class GameManager:
    def __init__(self):
        self.players = {}
        self.current_player = None
        self.state = None

    def add_player(self, name):
        player_id = len(self.players) + 1
        self.players[player_id] = Player(name)

    def get_current_player(self):
        return self.players[self.current_player]

    def update_player_status(self):

