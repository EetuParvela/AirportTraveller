import database as db

class Player:
    def __init__(self, name):
        self.name = name
        self.location = None
        self.money = 500
        self.co2 = 0
        self.places_visited = 0

    def update_location(self, location):
        self.location = location

    def update_money(self, money):
        self.money += money

    def update_co2(self, amount):
        self.co2 += amount

    def get_player_stats(self):
        name = self.name
        location = self.location
        money = self.money
        co2 = self.co2
        places_visited = self.places_visited
        return name, location, money, co2, places_visited

    def reset_stats(self):
        self.name = "Player"
        self.location = None
        self.money = 500
        self.co2 = 0
        self.places_visited = 0

    def check_is_over(self):
        if self.places_visited == 2:
            return True
        return False


class GameState:
    def __init__(self):
        self.days = 0
        self.player = None

    def start_game(self, name):
        self.player = Player(name)
        self.player.location = db.get_airport_info("EFHK")

    def get_distance(self, icao):
        current_airport = self.player.location
        next_location = db.get_airport_info(icao)
        distance = db.calculate_distance((current_airport['latitude_deg'],
                                          current_airport["longitude_deg"]),
                                         (next_location['latitude_deg'],
                                          next_location['longitude_deg']))
        return distance

    def calculate_co2(self, icao):
        distance = self.get_distance(icao)
        co2_emitted = distance * 0.050
        self.player.update_co2(co2_emitted)

    def fly_to(self, icao):
        if self.check_if_enough_money(icao):
            location = db.get_airport_info(icao)
            self.calculate_co2(icao)
            self.player.update_location(location)
            self.player.places_visited += 1
            self.days += 1
            return True
        else:
            return False

    def work(self, days):
        money = 50 * days
        self.days += days
        self.player.update_money(money)
        return money

    def check_if_enough_money(self, icao):
        distance = self.get_distance(icao)
        money_needed = distance * 0.5

        if money_needed < self.player.money:
            self.player.update_money(-money_needed)
            return True
        else:
            return False

    def is_over(self):
        if self.player.check_is_over():
            return True
        else:
            return False