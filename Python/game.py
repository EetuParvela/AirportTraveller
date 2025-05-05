from enum import Enum, auto
import game_manager as gm
import player as pl
from Python.player import Player

airports = gm.airport_infos()

player_data = {}
destination = {}

class GameState(Enum):
    START_TURN = auto()
    FLY = auto()
    APPLY_BONUS = auto()
    CHECK_STATUS = auto()
    SWITCH_PLAYER = auto()
    GAME_OVER = auto()

class Peli:
    def __init__(self):
        self.state = GameState.START_TURN
        self.current_player = 0
        self.players = [
            Player(player_data["player1"]),
            Player(player_data["player2"])
        ]
        self.players_out_of_fuel = [False, False]

    def run(self):
        while self.state != GameState.GAME_OVER:
            self.handle_state()

    def handle_state(self):
        player = self.players[self.current_player]

        match self.state:

            case GameState.START_TURN:
                print(f"\nPlayer {self.current_player + 1}'s turn begins.")

                self.state = GameState.FLY

            case GameState.FLY:
                self.players[self.current_player].fly_to(destination)
                self.state = GameState.APPLY_BONUS

            case GameState.APPLY_BONUS:
                print("Applying bonus/event...")

                self.state = GameState.CHECK_STATUS

            case GameState.CHECK_STATUS:
                if player.stats.fuel <= 0:
                    print(f"{player.name} is out of fuel!")
                    self.players_out_of_fuel[self.current_player] = True

                if all(self.players_out_of_fuel):
                    print("Both players are out of fuel. Game over!")
                    self.state = GameState.GAME_OVER
                else:
                    self.state = GameState.SWITCH_PLAYER

            case GameState.SWITCH_PLAYER:
                self.current_player = 1 - self.current_player
                self.state = GameState.START_TURN

            case GameState.GAME_OVER:
                print("Game over!")
