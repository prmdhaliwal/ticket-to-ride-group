"""Scoring classes."""


class ScoringStrategy:
    pass


class StandardScoring:
    def final_scores(self, players, board):
        # total score after tickets and longest path bonus
        scores = {}
        longest_players = self.longest_path_players(players, board)

        for player in players:
            total = player.score

            for ticket in player.destination_tickets:
                if ticket.is_complete(board, player):
                    total += ticket.value()
                else:
                    total -= ticket.value()

            if player in longest_players:
                if self.longest_path_length(player, board) > 0:
                    total += 10

            scores[player] = total

        return scores

    def winners(self, players, board):
        # start by finding players with the highest score
        scores = self.final_scores(players, board)
        winners = []
        best_score = None

        for player in players:
            player_score = scores[player]

            if best_score is None or player_score > best_score:
                best_score = player_score
                winners = []
                winners.append(player)
            elif player_score == best_score:
                winners.append(player)

        winners = self.tie_by_completed_tickets(winners, board)
        winners = self.tie_by_longest_path(winners, board)
        return winners

    def tie_by_completed_tickets(self, players, board):
        # first tie breaker is completed tickets
        tied = []
        best_count = None

        for player in players:
            completed = self.completed_ticket_count(player, board)

            if best_count is None or completed > best_count:
                best_count = completed
                tied = []
                tied.append(player)
            elif completed == best_count:
                tied.append(player)

        return tied

    def tie_by_longest_path(self, players, board):
        # second tie breaker is longest path
        tied = []
        best_length = None

        for player in players:
            path_length = self.longest_path_length(player, board)

            if best_length is None or path_length > best_length:
                best_length = path_length
                tied = []
                tied.append(player)
            elif path_length == best_length:
                tied.append(player)

        return tied  
    
    def completed_ticket_count(self, player, board):
        # count tickets where both cities are connected
        completed = 0

        for ticket in player.destination_tickets:
            if ticket.is_complete(board, player):
                completed += 1

        return completed

    def walk_route(self, city, unused_routes, current_length):
        # helper to keep walking through unused routes from the current city
        best_length = current_length

        for route in unused_routes:
            next_city = None

            if route.city_a == city:
                next_city = route.city_b

            if route.city_b == city:
                next_city = route.city_a

            if next_city is not None:
                remaining_routes = unused_routes.copy()
                remaining_routes.remove(route)
                path_length = self.walk_route(next_city, remaining_routes, current_length + route.length)

                if path_length > best_length:
                    best_length = path_length

        return best_length

    def longest_path_players(self, players, board):
        # players tied for the longest path bonus
        tied = []
        best_length = 0

        for player in players:
            path_length = self.longest_path_length(player, board)

            if path_length > best_length:
                best_length = path_length
                tied = []
                tied.append(player)
            elif path_length == best_length:
                tied.append(player)

        return tied

    def longest_path_length(self, player, board):
        # try each claimed route as the start of a path
        claimed_routes = board.claimed_routes(player)
        best_length = 0

        for route in claimed_routes:
            remaining_routes = claimed_routes.copy()
            remaining_routes.remove(route)

            length_from_a = self.walk_route(route.city_a, remaining_routes, route.length)
            length_from_b = self.walk_route(route.city_b, remaining_routes, route.length)

            if length_from_a > best_length:
                best_length = length_from_a

            if length_from_b > best_length:
                best_length = length_from_b

        return best_length

    