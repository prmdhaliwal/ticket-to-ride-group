"""Destination ticket class."""


class DestinationTicket:
    def __init__(self, from_city, to_city, points):
        self.from_city = from_city
        self.to_city = to_city
        self.points = points

    def value(self):
        return self.points

    def is_complete(self, board, player):
        connected_cities = []
        connected_cities.append(self.from_city)
        changed = True

        # follow claimed routes until no more cities can be reached
        while changed:
            changed = False
            claimed_routes = board.claimed_routes(player)

            for route in claimed_routes:
                if route.city_a in connected_cities and route.city_b not in connected_cities:
                    connected_cities.append(route.city_b)
                    changed = True

                if route.city_b in connected_cities and route.city_a not in connected_cities:
                    connected_cities.append(route.city_a)
                    changed = True

        if self.to_city in connected_cities:
            return True

        return False
