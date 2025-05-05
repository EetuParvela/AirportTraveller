import game_manager as gm


class Player:
    def __init__(self, name):
        self.name = name
        self.stats = PlayerStats()

    def fly_to(self, destination):
        coordinates = destination["latitude_deg"], destination["longitude_deg"]
        distance = gm.calculate_distance(self.stats.location, coordinates)
        cruise_speed = 833 # Nopeus km/h
        fuel_consumption = 889.571769
        fuel_needed = distance / cruise_speed * fuel_consumption

        co2_per_l = 2.52
        co2_emitted = fuel_needed * co2_per_l

        points_earned = distance * (1 + (distance / 2000))

        if self.stats.use_fuel(fuel_needed):
            self.stats.location = destination
            self.stats.update_score(points_earned)
            self.stats.update_co2(co2_emitted)
            self.stats.update_distance(distance)
        else:
            print(f"{self.name} doesn't have enough fuel to fly to {destination}!")

    def __str__(self):
        return (f"Player: {self.name}\n"
                f"Location: {self.stats.location}\n"
                f"Fuel: {self.stats.fuel}\n"
                f"Score: {self.stats.score}")


class PlayerStats:
    def __init__(self):
        self.location = []
        self.fuel = 0
        self.score = 0
        self.co2 = 0
        self.distance = 0

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
