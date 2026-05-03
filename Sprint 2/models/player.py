"""Player classes."""

from models.core import CardColor


class ScoringMarker:
    def __init__(self):
        self.position = 0

    def move_by(self, points):
        self.position += points


class Player:
    def __init__(self, name, trains_left=17):
        self.name = name
        self.train_cards = []
        self.trains_left = trains_left
        self.score = 0  # Added this so your teammate's scoring logic works
        self.destination_tickets = []
        self.marker = ScoringMarker()

    def matching_cards(self, route_colour):
        # cards that can be used on this route
        matching = []

        for card in self.train_cards:
            if card.matches(route_colour):
                matching.append(card)

        return matching

    def choose_cards_for_route(self, route):
        if route.colour == CardColor.GRAY:
            return self.choose_cards_for_gray_route(route)

        matching_cards = self.matching_cards(route.colour)
        coloured_cards = [c for c in matching_cards if c.colour != CardColor.LOCOMOTIVE]
        loco_cards = [c for c in matching_cards if c.colour == CardColor.LOCOMOTIVE]
        
        cards_to_use = []

        for card in coloured_cards:
            if len(cards_to_use) < route.length:
                cards_to_use.append(card)

        for card in loco_cards:
            if len(cards_to_use) < route.length:
                cards_to_use.append(card)

        if route.can_accept(cards_to_use):
            return cards_to_use

        return []

    def choose_cards_for_gray_route(self, route):
        wild_cards = []
        cards_by_colour = {}

        for card in self.train_cards:
            if card.colour == CardColor.LOCOMOTIVE:
                wild_cards.append(card)
            else:
                if card.colour not in cards_by_colour:
                    cards_by_colour[card.colour] = []

                cards_by_colour[card.colour].append(card)

        sorted_colours = sorted(cards_by_colour.keys(), key=lambda c: len(cards_by_colour[c]), reverse=True)

        for colour in sorted_colours:
            cards_to_use = []

            for card in cards_by_colour[colour]:
                if len(cards_to_use) < route.length:
                    cards_to_use.append(card)

            for card in wild_cards:
                if len(cards_to_use) < route.length:
                    cards_to_use.append(card)

            if route.can_accept(cards_to_use):
                return cards_to_use

        cards_to_use = []

        for card in wild_cards:
            if len(cards_to_use) < route.length:
                cards_to_use.append(card)

        if route.can_accept(cards_to_use):
            return cards_to_use

        return []

    def take_train_card(self, card):
        if card:
            self.train_cards.append(card)

    def remove_cards(self, cards):
        for card in cards:
            if card in self.train_cards:
                self.train_cards.remove(card)

    def can_claim_route(self, route, cards):
        return route.can_accept(cards)

    def take_tickets(self, new_tickets):
        self.destination_tickets.extend(new_tickets)

    def place_trains(self, count):
        if count <= self.trains_left:
            self.trains_left -= count

    def move_score(self, points):
        self.score += points
        self.marker.move_by(points)

    def __str__(self):
        return f"Player {self.name} | Score: {self.score} | Buses: {self.trains_left}"
