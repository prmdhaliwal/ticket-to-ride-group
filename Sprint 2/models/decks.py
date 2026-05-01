"""Deck classes."""

import random


class TrainCarCardDeck:
    def __init__(self, initial_cards):
        self.deck = initial_cards
        self.discard = []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def draw_blind(self):
        if not self.deck:
            if not self.discard:
                return None
            self.deck = self.discard
            self.discard = []
            self.shuffle()
        return self.deck.pop()

    def discard_cards(self, cards):
        self.discard.extend(cards)


class FaceUpPool:
    def __init__(self):
        self.face_up_cards = []

    def refresh(self, deck):
        while len(self.face_up_cards) < 5:
            card = deck.draw_blind()
            if card:
                self.face_up_cards.append(card)
            else:
                break

    def draw_face_up(self, index):
        if 0 <= index < len(self.face_up_cards):
            return self.face_up_cards.pop(index)
        return None


class DestinationTicketDeck:
    def __init__(self, initial_tickets):
        self.tickets = initial_tickets
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.tickets)

    def draw_three(self):
        drawn = []
        for _ in range(min(3, len(self.tickets))):
            drawn.append(self.tickets.pop())
        return drawn

    def return_tickets(self, rejected):
        for ticket in rejected:
            self.tickets.insert(0, ticket)