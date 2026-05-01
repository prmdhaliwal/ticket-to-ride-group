from typing import List
from models.cards import TrainCarCard, DestinationTicket

class ScoringMarker:
    def __init__(self):
        self._position = 0

    def moveBy(self, points: int) -> None:
        self._position += points

    @property
    def position(self) -> int:
        return self._position

class TrainCar:
    """Represents the physical plastic piece (e.g., London Bus)."""
    def __init__(self):
        self._route = None

    def placeOn(self, route) -> None:
        self._route = route

class Player:
    def __init__(self, name: str, initial_trains: int):
        self._name = name
        self._trainCards = []
        self._tickets = []
        self._trainsLeft = initial_trains
        self._marker = ScoringMarker()
        
        # Instantiate the physical plastic pieces
        self._trainPieces = [TrainCar() for _ in range(initial_trains)]

    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self) -> int:
        return self._marker.position

    @property
    def trainsLeft(self) -> int:
        return self._trainsLeft

    def takeTrainCard(self, card: TrainCarCard) -> None:
        if card:
            self._trainCards.append(card)

    def useTrainCards(self, cards: List[TrainCarCard]) -> None:
        for card in cards:
            if card in self._trainCards:
                self._trainCards.remove(card)

    def canPayFor(self, route, cards: List[TrainCarCard]) -> bool:
        """Validates if the provided cards match the route's cost and color."""
        if len(cards) != route.length:
            return False
        for card in cards:
            if not card.matches(route.color):
                return False
        return True

    def takeTickets(self, tickets: List[DestinationTicket]) -> None:
        self._tickets.extend(tickets)

    def placeTrains(self, count: int) -> None:
        if count <= self._trainsLeft:
            self._trainsLeft -= count

    def moveScore(self, points: int) -> None:
        self._marker.moveBy(points)
        
    def __str__(self):
        return f"Player {self._name} | Score: {self.score} | Buses: {self.trainsLeft}"