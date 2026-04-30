"""Board, city, and route classes."""


class City:
    def __init__(self, name):
        self.name = name


class Route:
    def __init__(self, city_a, city_b, colour, length):
        # route connects two cities and starts unclaimed
        self.cities = [city_a, city_b]
        self.city_a = city_a
        self.city_b = city_b
        self.colour = colour
        self.length = length
        self.owner = None
        self.placed_trains = []

    def is_available(self):
        return self.owner is None


class BoardMap:
    def __init__(self, routes=None):
        if routes is None:
            self.routes = []
        else:
            self.routes = routes

    def claimed_routes(self, player):
        claimed = []

        for route in self.routes:
            if route.owner == player:
                claimed.append(route)

        return claimed
