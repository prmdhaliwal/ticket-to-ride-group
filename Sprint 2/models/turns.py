"""Turn flow classes."""

from models.cards import TrainCar
from models.core import Subject


class EndGameTracker:
    """Tracks the final round trigger (when a player hits 2 or fewer buses)."""
    def __init__(self):
        self.final_round = False
        self.triggering_player = None
        self.final_turns_remaining = 0
        self.game_finished = False

    def check_final_round(self, player, player_count):
        if self.final_round:
            return False

        if player.trains_left <= 2:
            self.final_round = True
            self.triggering_player = player
            self.final_turns_remaining = player_count
            return True

        return False

    def use_final_turn(self):
        if self.final_round and self.final_turns_remaining > 0:
            self.final_turns_remaining -= 1

        if self.final_round and self.final_turns_remaining == 0:
            self.game_finished = True

    def game_over(self):
        return self.game_finished


class TurnManager(Subject):
    """Manages the active player and validates actions."""
    def __init__(self, players, board, transport_deck, ticket_deck, face_up_pool):
        super().__init__()
        self.players = players
        self.board = board
        self.transport_deck = transport_deck
        self.ticket_deck = ticket_deck
        self.face_up_pool = face_up_pool
        self.current_player_index = 0
        self.action_taken = False
        self.end_game_tracker = EndGameTracker()

    def get_current_player(self):
        return self.players[self.current_player_index]

    def claim_route(self, route):
        if self.end_game_tracker.game_over():
            return False, "The game is over."

        player = self.get_current_player()

        if self.action_taken:
            return False, "Only one route may be claimed per turn."

        if route not in self.board.routes:
            return False, "That route is not on the board."

        # Pass total players to is_available for double-route logic
        if not route.is_available(len(self.players)):
            return False, "That route has already been claimed."

        if player.trains_left < route.length:
            return False, "Not enough bus pieces."

        # use the first matching cards in players hand
        matching_cards = player.matching_cards(route.colour)
        cards_to_use = []

        for card in matching_cards:
            if len(cards_to_use) < route.length:
                cards_to_use.append(card)

        if len(cards_to_use) < route.length:
            return False, "Not enough matching transportation cards."

        player.remove_cards(cards_to_use)
        player.trains_left -= route.length
        player.score += self.route_points(route.length)

        route.owner = player
        route.placed_trains = []

        # bus pieces now on the claimed route
        for _ in range(route.length):
            train = TrainCar(player, route)
            route.placed_trains.append(train)

        self.action_taken = True
        self.notify()  # Notify observers that the board state changed
        return True, "Route claimed."

    def next_turn(self):
        if self.end_game_tracker.game_over():
            return "The game is over."

        player = self.get_current_player()

        # check final round when players end their turn
        final_round_started = self.end_game_tracker.check_final_round(player, len(self.players))

        if self.end_game_tracker.final_round and not final_round_started:
            self.end_game_tracker.use_final_turn()

        if self.end_game_tracker.game_over():
            self.notify() # Notify observers of game end
            return "Game over."

        self.current_player_index += 1

        if self.current_player_index >= len(self.players):
            self.current_player_index = 0

        self.action_taken = False
        self.notify()  # Notify observers that turn has changed
        return "Next turn."

    def is_game_over(self):
        return self.end_game_tracker.game_over()

    def route_points(self, length):
        score_table = {
            1: 1,
            2: 2,
            3: 4,
            4: 7,
        }

        if length in score_table:
            return score_table[length]

        return 0