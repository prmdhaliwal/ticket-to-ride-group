from models.core import Subject

class EndGameTracker:
    """Tracks the final round trigger (when a player hits 2 or fewer buses)."""
    def __init__(self):
        self._finalRound = False
        self._triggeringPlayer = None
        self._finalTurnsRemaining = 0

    def checkFinalRound(self, player, total_players: int) -> None:
        if not self._finalRound and player.trainsLeft <= 2:
            self._finalRound = True
            self._triggeringPlayer = player
            # Everyone gets one last turn, including the player who triggered it
            self._finalTurnsRemaining = total_players  

    def decrementTurn(self) -> None:
        if self._finalRound:
            self._finalTurnsRemaining -= 1

    def finalRoundStarted(self) -> bool:
        return self._finalRound

    def gameOver(self) -> bool:
        return self._finalRound and self._finalTurnsRemaining <= 0


class TurnManager(Subject):
    """Manages the active player and validates actions."""
    def __init__(self, players, board, transport_deck, ticket_deck, face_up_pool):
        super().__init__()
        self._players = players
        self._board = board
        self._transport_deck = transport_deck
        self._ticket_deck = ticket_deck
        self._face_up_pool = face_up_pool
        self._currentPlayerIndex = 0
        self._actionTaken = False
        self._endGameTracker = EndGameTracker()

    def getCurrentPlayer(self):
        return self._players[self._currentPlayerIndex]

    def nextTurn(self) -> None:
        """Ends the current turn and passes play to the next person."""
        # Check for the end game trigger before passing the turn
        current_player = self.getCurrentPlayer()
        self._endGameTracker.checkFinalRound(current_player, len(self._players))
        self._endGameTracker.decrementTurn()

        # Move to the next player
        self._currentPlayerIndex = (self._currentPlayerIndex + 1) % len(self._players)
        self._actionTaken = False
        
        # Notify the UI that the turn has changed!
        self.notify()

    def isGameOver(self) -> bool:
        return self._endGameTracker.gameOver()