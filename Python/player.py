class Player:
    def __init__(self, name, start_airport):
        self.name = name
        self.current_airport = start_airport
        self.fuel = 10000
        self.score = 0.0
        self.co2 = 0.0
        self.total_distance = 0.0

    def check_fuel(self):
        if self.fuel <= 0:
            return True
        return False

    def get_stats(self):
        return {
            "name": self.name,
            "current_airport": self.current_airport,
            "fuel": self.fuel,
            "score": self.score,
            "co2": self.co2,
            "total_distance": self.total_distance
        }

    def update_airport_data(self, next_airport):
        self.current_airport = next_airport

    def update_score(self, points):
        self.score += points

    def update_fuel(self, amount):
        self.fuel -= amount

    def update_co2(self, amount):
        self.co2 += amount

    def update_distance(self, amount):
        self.total_distance += amount