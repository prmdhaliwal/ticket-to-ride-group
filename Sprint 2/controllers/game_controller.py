"""Controller layer for the game."""

from models.scoring import StandardScoring


class GameController:
    def __init__(self, turn_manager=None, scoring=None):
        self.turn_manager = turn_manager

        if scoring is None:
            self.scoring = StandardScoring()
        else:
            self.scoring = scoring

    def set_turn_manager(self, turn_manager):
        self.turn_manager = turn_manager

    def get_routes(self):
        # routes shown
        if self.turn_manager is None:
            return []

        return self.turn_manager.board.routes

    def players(self):
        if self.turn_manager is None:
            return []

        return self.turn_manager.players

    def claim_route(self, route_index):
        # ui sends the selected route
        if self.turn_manager is None:
            return False, "Game has not been set up."

        routes = self.get_routes()

        if route_index is None or route_index < 0 or route_index >= len(routes):
            return False, "Select a valid route first."

        route = routes[route_index]
        return self.turn_manager.claim_route(route)

    def end_turn(self):
        if self.turn_manager is None:
            return "Game has not been set up."

        return self.turn_manager.next_turn()

    def current_player(self):
        if self.turn_manager is None:
            return None

        return self.turn_manager.get_current_player()

    def game_over(self):
        # stop actions after the game ends
        if self.turn_manager is None:
            return False

        return self.turn_manager.is_game_over()

    def final_scores(self):
        # scores shown once game is over
        if self.turn_manager is None:
            return {}

        players = self.turn_manager.players
        board = self.turn_manager.board
        return self.scoring.final_scores(players, board)

    def winners(self):
        # winner text shown by the ui
        if self.turn_manager is None:
            return []

        players = self.turn_manager.players
        board = self.turn_manager.board
        return self.scoring.winners(players, board)
    
    def draw_train_cards(self, from_deck = False, pool_index = None):
        if self.turn_manager is None:
            return False, "Game has not been set up."

        if pool_index < 0 or pool_index >= len(self.transport_deck()):
            return False, "Select a valid face up card first."

        return self.turn_manager.draw_train_cards(from_deck, pool_index)
        
