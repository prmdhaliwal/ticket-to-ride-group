from models.board import BoardMap
from models.player import Player
from models.cards import TrainCarCardDeck, DestinationTicketDeck, ColouredCarCard, LocomotiveCard, DestinationTicket, FaceUpPool
from models.core import CardColor
from controllers.turn_manager import TurnManager

class GameSetup:
    """Responsible for bootstrapping the game state from a MapDefinition."""
    
    def setUpGame(self, map_def, player_names) -> TurnManager:
        board = self.createBoard(map_def)
        players = self.createPlayers(player_names, map_def)
        
        # Build Decks
        transport_deck = self._build_transport_deck()
        ticket_deck = self._build_ticket_deck(map_def)
        
        self.dealStartingCards(players, transport_deck)
        self.dealStartingTickets(players, ticket_deck)
        
        # Initialize the 5 face-up cards
        face_up_pool = FaceUpPool()
        face_up_pool.refresh(transport_deck)
        
        return TurnManager(players, board, transport_deck, ticket_deck, face_up_pool)

    def createPlayers(self, names, map_def):
        return [Player(name, map_def.initial_pieces) for name in names]

    def createBoard(self, map_def):
        return BoardMap(map_def)

    def dealStartingCards(self, players, deck):
        for player in players:
            for _ in range(4):
                player.takeTrainCard(deck.drawBlind())

    def dealStartingTickets(self, players, deck):
        for player in players:
            # Draw 3 tickets. (The UI will later handle discarding unwanted ones).
            dealt = deck.drawThree()
            player.takeTickets(dealt)

    def _build_transport_deck(self):
        """Creates the 68 cards for the London edition."""
        cards = []
        colors = [CardColor.BLUE, CardColor.BLACK, CardColor.PINK, 
                  CardColor.YELLOW, CardColor.ORANGE, CardColor.WHITE]
        for color in colors:
            for _ in range(10):
                cards.append(ColouredCarCard(color))
        for _ in range(8):
            cards.append(LocomotiveCard())
        return TrainCarCardDeck(cards)

    def _build_ticket_deck(self, map_def):
        """Creates the tickets based on the map definition."""
        tickets = []
        for t_data in map_def.tickets:
            tickets.append(DestinationTicket(t_data["start"], t_data["end"], t_data["points"]))
        return DestinationTicketDeck(tickets)