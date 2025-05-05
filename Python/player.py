import database as db

class Player:
    def __init__(self, name, start_airport):
        self.name = name
        self.current_airport = start_airport
        self.stats = PlayerStats()

    @staticmethod
    def calculate_fuel(self, distance):
        cruise_speed = 833
        fuel_consumption = 889.571769
        return (distance / cruise_speed) * fuel_consumption

    @staticmethod
    def calculate_co2(self, fuel_used):
        co2_per_l = 2.52
        return fuel_used * co2_per_l

    @staticmethod
    def calculate_points(distance):
        return distance * (1 + (distance / 2000))


class PlayerStats:
    def __init__(self):
        self.location = []
        self.fuel = 0.0
        self.score = 0.0
        self.co2 = 0.0
        self.distance = 0.0

    def update_location(self, new_location):
        self.location = new_location

    def use_fuel(self, amount):
        if self.fuel >= amount:
            self.fuel -= amount
            return True
        return False

    def update_score(self, points):
        self.score += points

    def update_co2(self, amount):
        self.co2 += amount

    def update_distance(self, amount):
        self.distance += amount

