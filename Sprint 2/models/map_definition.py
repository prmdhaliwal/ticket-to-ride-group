"""Configuration data for specific board layouts."""

from models.core import CardColor


class MapDefinition:
    def __init__(self, map_name, min_players, max_players, initial_train_pieces):
        self.map_name = map_name
        self.min_players = min_players
        self.max_players = max_players
        self.initial_train_pieces = initial_train_pieces
        
        self.cities = []
        self.routes = []
        self.tickets = []
        self.districts = []
        
        # Scoring table specific to the London map
        self.route_scores = {
            1: 1, 
            2: 2, 
            3: 4, 
            4: 7
        }

    def add_city(self, city_name):
        self.cities.append(city_name)

    def add_route(self, city_a, city_b, colour, length):
        self.routes.append({
            "start": city_a, 
            "end": city_b, 
            "color": colour, 
            "length": length
        })

    def add_ticket(self, city_a, city_b, points):
        self.tickets.append({
            "start": city_a, 
            "end": city_b, 
            "points": points
        })

    def add_district(self, district_name, locations, points):
        self.districts.append({
            "name": district_name,
            "locations": locations,
            "points": points
        })

    @classmethod
    def create_london_map(cls):
        # Initializing London with 17 initial train pieces per UML/London rules
        london = cls("London", 2, 4, 17)
        
        # Comprehensive city list
        cities = [
            "Hyde Park", "Covent Garden", "Tower of London", "Waterloo", "Big Ben",
            "Baker Street", "Regent's Park", "Chelsea", "Brick Lane", "King's Cross", 
            "Victoria", "Notting Hill", "Elephant & Castle", "Paddington", "London Bridge", 
            "Piccadilly Circus", "St. Paul's", "Westminster", "Spitalfields", "British Museum", 
            "Trafalgar Square", "Camden", "Soho", "Shoreditch", "Kensington", "South Bank", 
            "Mayfair", "The Shard", "Marylebone", "Borough Market", "The Gherkin", 
            "Fleet Street", "Knightsbridge", "Bank", "Greenwich", "St Pancras",
            "Buckingham Palace"
        ]
        for city in cities:
            london.add_city(city)
        
        # Example routes
        london.add_route("Hyde Park", "Covent Garden", CardColor.BLACK, 2)
        london.add_route("Covent Garden", "Tower of London", CardColor.PINK, 3)
        london.add_route("Covent Garden", "Waterloo", CardColor.YELLOW, 1)
        london.add_route("Buckingham Palace", "Big Ben", CardColor.GRAY, 1)
        london.add_route("Big Ben", "Trafalgar Square", CardColor.BLUE, 1)
        london.add_route("Trafalgar Square", "Piccadilly Circus", CardColor.GREEN, 1)
        london.add_route("Covent Garden", "British Museum", CardColor.ORANGE, 1)

        london.add_district(
            "District 1",
            ["Covent Garden", "British Museum"],
            1
        )

        london.add_district(
            "District 2",
            ["Buckingham Palace", "Big Ben", "Trafalgar Square", "Piccadilly Circus"],
            2
        )
        
        # Complete Destination Ticket deck
        tickets_data = [
            ("Baker Street", "Covent Garden", 3), ("Hyde Park", "Tower of London", 6),
            ("Regent's Park", "Waterloo", 4), ("Chelsea", "Brick Lane", 5),
            ("King's Cross", "Victoria", 4), ("Notting Hill", "Elephant & Castle", 6),
            ("Paddington", "London Bridge", 5), ("Piccadilly Circus", "St. Paul's", 3),
            ("Westminster", "Spitalfields", 5), ("British Museum", "Big Ben", 3),
            ("Trafalgar Square", "Camden", 4), ("Soho", "Shoreditch", 4),
            ("Kensington", "South Bank", 5), ("Mayfair", "The Shard", 6),
            ("Marylebone", "Borough Market", 4), ("Covent Garden", "The Gherkin", 4),
            ("Hyde Park", "Fleet Street", 4), ("Knightsbridge", "Bank", 5),
            ("Victoria", "Greenwich", 7), ("St Pancras", "Westminster", 4)
        ]
        for city_a, city_b, points in tickets_data:
            london.add_ticket(city_a, city_b, points)
        
        return london
