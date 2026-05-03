"""Game setup classes."""

from models.board import BoardMap
from models.player import Player
from models.decks import TrainCarCardDeck, DestinationTicketDeck, FaceUpPool
from models.cards import ColouredCarCard, LocomotiveCard
from models.tickets import DestinationTicket
from models.core import CardColor
from models.turns import TurnManager


class GameSetup:
    def set_up_game(self, map_definition, player_names):
        # 1. Create the Board
        board = self.create_board(map_definition)
        
        # 2. Create the Players
        players = self.create_players(player_names, map_definition)
        
        # 3. Build and Shuffle Decks
        train_deck = self.create_train_deck()
        ticket_deck = self.create_ticket_deck(map_definition)
        
        # 4. Deal Initial Hands
        self.deal_starting_cards(players, train_deck)
        self.deal_starting_tickets(players, ticket_deck)
        
        # 5. Flip Initial Face-Up Pool
        face_up_pool = FaceUpPool()
        face_up_pool.refresh(train_deck)
        
        # 6. Initialize Turn Manager
        turn_manager = TurnManager(players, board, train_deck, ticket_deck, face_up_pool)
        
        # Return all necessary state to the GameController
        return turn_manager, train_deck, ticket_deck, face_up_pool

    def create_board(self, map_definition):
        return BoardMap(map_definition)

    def create_players(self, names, map_definition):
        players = []
        for name in names:
            # Initialized with 17 trains for the London Map
            players.append(Player(name, trains_left=map_definition.initial_train_pieces))
        return players

    def create_train_deck(self):
        cards = []
        colors = [
            CardColor.BLUE,
            CardColor.GREEN,
            CardColor.BLACK,
            CardColor.PINK,
            CardColor.YELLOW,
            CardColor.ORANGE
        ]
        
        for color in colors:
            for _ in range(6):
                cards.append(ColouredCarCard(color))
                
        for _ in range(8):
            cards.append(LocomotiveCard())
            
        return TrainCarCardDeck(cards)

    def create_ticket_deck(self, map_definition):
        tickets = []
        # Populate from London map tickets
        for t_data in map_definition.tickets:
            tickets.append(DestinationTicket(t_data["start"], t_data["end"], t_data["points"]))
        return DestinationTicketDeck(tickets)

    def deal_starting_cards(self, players, deck):
        for player in players:
            for _ in range(2):
                card = deck.draw_blind()
                if card:
                    player.take_train_card(card)

    def deal_starting_tickets(self, players, deck):
        for player in players:
            drawn_tickets = deck.draw_two()
            player.take_tickets(drawn_tickets)
