"""Turn flow classes."""

from ticket_to_ride.models.cards import TrainCar


class EndGameTracker:
    pass


class TurnManager:
    def __init__(self, players, board):
        self.players = players
        self.board = board
        self.current_player_index = 0
        self.action_taken = False

    def get_current_player(self):
        return self.players[self.current_player_index]

    def claim_route(self, route):
        player = self.get_current_player()

        if self.action_taken:
            return False, "Only one route may be claimed per turn."

        if route not in self.board.routes:
            return False, "That route is not on the board."

        if not route.is_available():
            return False, "That route has already been claimed."

        if player.trains_left < route.length:
            return False, "Not enough train pieces."

        # use the first matching cards in players hand
        matching_cards = player.matching_cards(route.colour)
        cards_to_use = []

        for card in matching_cards:
            if len(cards_to_use) < route.length:
                cards_to_use.append(card)

        if len(cards_to_use) < route.length:
            return False, "Not enough matching train cards."

        player.remove_cards(cards_to_use)
        player.trains_left -= route.length
        player.score += self.route_points(route.length)

        route.owner = player
        route.placed_trains = []

        # train pieces now on the claimed route
        for _ in range(route.length):
            train = TrainCar(player, route)
            route.placed_trains.append(train)

        self.action_taken = True
        return True, "Route claimed."

    def route_points(self, length):
        score_table = {
            1: 1,
            2: 2,
            3: 4,
            4: 7,
            5: 10,
            6: 15,
        }

        if length in score_table:
            return score_table[length]

        return 0
