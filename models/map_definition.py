from models.core import CardColor

class MapDefinition:
    """Configuration class for specific board layouts (London)."""
    
    def __init__(self, name, min_players, max_players, initial_pieces):
        self.name = name
        self.min_players = min_players
        self.max_players = max_players
        self.initial_pieces = initial_pieces
        
        self.cities = []
        self.routes = []
        self.tickets = []
        
        # Route length to point value mapping (London scoring rules)
        self.route_scores = {
            1: 1,
            2: 2,
            3: 4,
            4: 7
        }

    def add_city(self, city_name):
        self.cities.append(city_name)

    def add_route(self, city_a, city_b, color: CardColor, length: int):
        self.routes.append({
            "start": city_a,
            "end": city_b,
            "color": color,
            "length": length
        })

    def add_ticket(self, city_a, city_b, points: int):
        self.tickets.append({
            "start": city_a,
            "end": city_b,
            "points": points
        })

    @classmethod
    def create_london_map(cls):
        """Factory method to generate the London Map Definition."""
        # London rules: max 4 players, 17 buses each
        london = cls("London", min_players=2, max_players=4, initial_pieces=17)
        
        # 1. Add all the unique cities required for the tickets
        cities = [
            "Hyde Park", "Covent Garden", "Tower of London", "Waterloo", "Big Ben",
            "Baker Street", "Regent's Park", "Chelsea", "Brick Lane", "King's Cross", 
            "Victoria", "Notting Hill", "Elephant & Castle", "Paddington", "London Bridge", 
            "Piccadilly Circus", "St. Paul's", "Westminster", "Spitalfields", "British Museum", 
            "Trafalgar Square", "Camden", "Soho", "Shoreditch", "Kensington", "South Bank", 
            "Mayfair", "The Shard", "Marylebone", "Borough Market", "The Gherkin", 
            "Fleet Street", "Knightsbridge", "Bank", "Greenwich", "St Pancras"
        ]
        for city in cities:
            london.add_city(city)
        
        # 2. Add some initial routes using the Enum 
        london.add_route("Hyde Park", "Covent Garden", CardColor.BLACK, 2)
        london.add_route("Covent Garden", "Tower of London", CardColor.PINK, 3)
        london.add_route("Covent Garden", "Waterloo", CardColor.YELLOW, 1)
        
        # 3. Add the complete 20-card Destination Ticket deck
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