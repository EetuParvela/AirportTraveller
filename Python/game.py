from enum import Enum, auto
import player
import api


class GameState(Enum):
    START_TURN = auto()
    CHOOSE_DESTINATION = auto()
    FLY = auto()
    ARRIVE = auto()
    APPLY_BONUS = auto()
    CHECK_STATUS = auto()
    SWITCH_PLAYER = auto()
    GAME_OVER = auto()


class Peli:
    def __init__(self):
        self.state = GameState.START_TURN
        self.current_player = None
        self.players = [
            {}
        ]

    def run(self):
        while self.state != GameState.GAME_OVER:
            self.handle_state(self.current_player)

    def handle_state(self, current_player):
        match self.state:
            case GameState.START_TURN:
                print(f"\nPlayer {self.current_player}'s turn begins.")
                self.state = GameState.CHOOSE_DESTINATION

            case GameState.CHOOSE_DESTINATION:
                print("Choosing destination...")
                self.state = GameState.FLY

            case GameState.FLY:
                print("Flying to destination...")
                self.state = GameState.ARRIVE

            case GameState.ARRIVE:
                print("Arrived at airport.")
                self.state = GameState.APPLY_BONUS

            case GameState.APPLY_BONUS:
                print("Applying bonus/event...")
                self.state = GameState.CHECK_STATUS

            case GameState.CHECK_STATUS:
                player = self.players[self.current_player]
                if player["fuel"] <= 0:
                    print("Out of fuel! Game over.")
                    self.state = GameState.GAME_OVER
                else:
                    self.state = GameState.SWITCH_PLAYER

            case GameState.SWITCH_PLAYER:
                self.current_player = 1 if self.current_player == 2 else 2
                self.state = GameState.START_TURN

            case GameState.GAME_OVER:
                print("Game over!")
