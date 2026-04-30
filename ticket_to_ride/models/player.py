"""Player classes."""


class ScoringMarker:
    pass


class Player:
    def __init__(self, name, trains_left=45):
        self.name = name
        self.train_cards = []
        self.trains_left = trains_left
        self.score = 0
        self.destination_tickets = []

    def matching_cards(self, route_colour):
        matching = []

        for card in self.train_cards:
            if card.matches(route_colour):
                matching.append(card)

        return matching

    def remove_cards(self, cards):
        for card in cards:
            self.train_cards.remove(card)

