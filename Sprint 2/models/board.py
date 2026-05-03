"""Board, city, and route classes."""

from models.core import CardColor


class City:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, City) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


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
        self.twin_route = None

    def claim(self, player):
        self.owner = player

    def is_available(self, total_players_in_game, player=None):
        if self.owner is not None:
            return False
            
        if self.twin_route is not None:
            if player is not None and self.twin_route.owner == player:
                return False

            if total_players_in_game == 2 and self.twin_route.owner is not None:
                return False
                
        return True

    def can_accept(self, cards):
        if len(cards) != self.length:
            return False

        if self.colour == CardColor.GRAY:
            colours_used = set()

            for card in cards:
                if card.colour != CardColor.LOCOMOTIVE:
                    colours_used.add(card.colour)

            return len(colours_used) <= 1

        for card in cards:
            if not card.matches(self.colour):
                return False

        return True

    def points(self, score_table):
        return score_table.get(self.length, 0)


class BoardMap:
    def __init__(self, map_definition=None):
        self.cities = {}
        self.routes = []
        self.route_scores = {}
        self.districts = []

        if map_definition is not None:
            self.route_scores = getattr(map_definition, "route_scores", {}).copy()
            self.districts = getattr(map_definition, "districts", []).copy()

            for name in map_definition.cities:
                self.cities[name] = City(name)

            route_pairs = {}

            for route_data in map_definition.routes:
                c1 = self.cities[route_data["start"]]
                c2 = self.cities[route_data["end"]]
                route = Route(c1, c2, route_data["color"], route_data["length"])
                self.routes.append(route)

                pair_key = tuple(sorted([c1.name, c2.name]))
                if pair_key in route_pairs:
                    twin = route_pairs[pair_key]
                    route.twin_route = twin
                    twin.twin_route = route
                else:
                    route_pairs[pair_key] = route

    def claimed_routes(self, player):
        claimed = []

        for route in self.routes:
            if route.owner == player:
                claimed.append(route)

        return claimed
