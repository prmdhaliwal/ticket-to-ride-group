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

   
