from models.core import CardColor

class City:
    """Represents a named location on the board."""
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return isinstance(other, City) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Route:
    """Represents a connection between two cities."""
    def __init__(self, city_a: City, city_b: City, color: CardColor, length: int):
        self.city_a = city_a
        self.city_b = city_b
        self.color = color
        self.length = length
        self.owner = None
        self.twin_route = None  # Points to a parallel route, if it exists

    def claim(self, player):
        self.owner = player

    def is_available(self, total_players_in_game: int) -> bool:
        """Checks if the route can be claimed based on player count and twin routes."""
        if self.owner is not None:
            return False
            
        # London rules: In 2 or 3 player games, only one twin route can be used.
        if self.twin_route and total_players_in_game <= 3:
            if self.twin_route.owner is not None:
                return False
                
        return True

class BoardMap:
    """The main board containing the graph of cities and routes."""
    def __init__(self, map_definition):
        self.cities = {name: City(name) for name in map_definition.cities}
        self.routes = []
        
        # Temporary dictionary to find twin routes efficiently during setup
        route_pairs = {}

        for route_data in map_definition.routes:
            c1 = self.cities[route_data["start"]]
            c2 = self.cities[route_data["end"]]
            route = Route(c1, c2, route_data["color"], route_data["length"])
            self.routes.append(route)
            
            # Logic to detect and link double-routes
            pair_key = tuple(sorted([c1.name, c2.name]))
            if pair_key in route_pairs:
                twin = route_pairs[pair_key]
                route.twin_route = twin
                twin.twin_route = route
            else:
                route_pairs[pair_key] = route