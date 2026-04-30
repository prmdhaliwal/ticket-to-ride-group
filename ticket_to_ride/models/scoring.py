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

