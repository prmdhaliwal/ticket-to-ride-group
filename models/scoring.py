from abc import ABC, abstractmethod

class ScoringStrategy(ABC):
    """Strategy interface for calculating final scores."""
    
    @abstractmethod
    def calculate_final_scores(self, players, board_map):
        pass

class StandardScoring(ScoringStrategy):
    """The standard scoring rules for Ticket to Ride."""
    
    def calculate_final_scores(self, players, board_map):
        scores = {}
        for player in players:
            # 1. Base score from routes (already tracked during the game)
            final_score = player.score 
            
            # 2. Add/Subtract Destination Tickets
            for ticket in player.destination_tickets:
                if ticket.is_complete(board_map, player):
                    final_score += ticket.point_value
                else:
                    final_score -= ticket.point_value
                    
            scores[player] = final_score
            
        # Note: We can add the 'Longest Path' bonus logic here later!
        return scores