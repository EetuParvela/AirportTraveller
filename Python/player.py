import utils as gm

class Player:
    cruise_speed = 833
    fuel_consumption = 889.571769
    co2_per_l = 2.52

    def __init__(self, name):
        self.name = name
        self.stats = PlayerStats()

    def fly_to(self, destination):
        coordinates = (destination["latitude_deg"], destination["longitude_deg"])
        distance = gm.calculate_distance(self.stats.location, coordinates)

        fuel_needed = self.calculate_fuel(distance)
        co2_emitted = self.calculate_co2(fuel_needed)
        points_earned = self.calculate_points(distance)

        if self.stats.use_fuel(fuel_needed):
            self.stats.update_location(coordinates)
            self.stats.update_score(points_earned)
            self.stats.update_co2(co2_emitted)
            self.stats.update_distance(distance)
            return True
        else:
            print(f"{self.name} doesn't have enough fuel to fly to {destination['name']}!")
            return False

    def calculate_fuel(self, distance):
        return (distance / self.cruise_speed) * self.fuel_consumption

    def calculate_co2(self, fuel_used):
        return fuel_used * self.co2_per_l

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

