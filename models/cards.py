from abc import ABC, abstractmethod
import random
from typing import List
from models.core import CardColor

# --- CARD MODELS ---

class TrainCarCard(ABC):
    @abstractmethod
    def matches(self, colour: CardColor) -> bool:
        pass

class ColouredCarCard(TrainCarCard):
    def __init__(self, colour: CardColor):
        self._colour = colour

    def matches(self, colour: CardColor) -> bool:
        # Match if it's the exact colour, or if the route requires GRAY (any colour)
        return self._colour == colour or colour == CardColor.GRAY

    def __str__(self):
        return f"{self._colour.value} Bus"

class LocomotiveCard(TrainCarCard):
    def matches(self, colour: CardColor) -> bool:
        # Locomotives match everything
        return True

    def __str__(self):
        return "Wild Bus"

class DestinationTicket:
    def __init__(self, from_city, to_city, points: int):
        self._from_city = from_city
        self._to_city = to_city
        self._points = points

    def value(self) -> int:
        return self._points

    def isComplete(self, board, player) -> bool:
        # Graph traversal to be implemented later
        return False

    def __str__(self):
        return f"{self._from_city} to {self._to_city} ({self._points} pts)"


# --- DECK AND POOL MANAGERS ---

class TrainCarCardDeck:
    def __init__(self, initial_cards: List[TrainCarCard]):
        self._deck = initial_cards
        self._discard = []
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self._deck)

    def drawBlind(self) -> TrainCarCard:
        if not self._deck:
            if not self._discard:
                return None  # No cards left anywhere
            # Reshuffle discards into deck
            self._deck = self._discard
            self._discard = []
            self.shuffle()
        return self._deck.pop()

    def discardCards(self, cards: List[TrainCarCard]) -> None:
        self._discard.extend(cards)

class FaceUpPool:
    def __init__(self):
        self._faceUpCards = []

    def refresh(self, deck: TrainCarCardDeck) -> None:
        """Refills the face-up pool to 5 cards."""
        while len(self._faceUpCards) < 5:
            card = deck.drawBlind()
            if card:
                self._faceUpCards.append(card)
            else:
                break  # Deck is completely empty

    def drawFaceUp(self, index: int) -> TrainCarCard:
        """Draws a specific card from the pool."""
        if 0 <= index < len(self._faceUpCards):
            return self._faceUpCards.pop(index)
        return None

class DestinationTicketDeck:
    def __init__(self, initial_tickets: List[DestinationTicket]):
        self._tickets = initial_tickets
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self._tickets)

    def drawThree(self) -> List[DestinationTicket]:
        drawn = []
        for _ in range(min(3, len(self._tickets))):
            drawn.append(self._tickets.pop())
        return drawn

    def returnTickets(self, rejected: List[DestinationTicket]) -> None:
        # Returned tickets go to the bottom of the deck (index 0)
        for ticket in rejected:
            self._tickets.insert(0, ticket)