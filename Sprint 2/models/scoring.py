"""Scoring classes."""


class ScoringStrategy:
    def final_scores(self, players, board):
        raise NotImplementedError

    def winners(self, players, board):
        raise NotImplementedError


class StandardScoring(ScoringStrategy):
    def final_scores(self, players, board):
        scores = {}

        for player in players:
            total = player.score

            for ticket in player.destination_tickets:
                if ticket.is_complete(board, player):
                    total += ticket.value()
                else:
                    total -= ticket.value()

            total += self.district_score(player, board)

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
    
    def completed_ticket_count(self, player, board):
        # count tickets where both cities are connected
        completed = 0

        for ticket in player.destination_tickets:
            if ticket.is_complete(board, player):
                completed += 1

        return completed

    def district_score(self, player, board):
        total = 0

        for district in board.districts:
            if self.district_complete(player, board, district):
                total += district["points"]

        return total

    def completed_districts(self, player, board):
        completed = []

        for district in board.districts:
            if self.district_complete(player, board, district):
                completed.append(district["name"])

        return completed

    def district_complete(self, player, board, district):
        locations = district["locations"]

        if not locations:
            return False

        for start in locations:
            for end in locations:
                if start != end and not self.cities_connected(start, end, player, board):
                    return False

        return True

    def cities_connected(self, start_city, target_city, player, board):
        start = self.city_name(start_city)
        target = self.city_name(target_city)
        connected = [start]
        changed = True

        while changed:
            changed = False

            for route in board.claimed_routes(player):
                city_a = self.city_name(route.city_a)
                city_b = self.city_name(route.city_b)

                if city_a in connected and city_b not in connected:
                    connected.append(city_b)
                    changed = True

                if city_b in connected and city_a not in connected:
                    connected.append(city_a)
                    changed = True

        return target in connected

    def city_name(self, city):
        return getattr(city, "name", city)
