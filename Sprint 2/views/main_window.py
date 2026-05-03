"""Main Tkinter window."""
import tkinter as tk
from models.core import Observer

class MainWindow(Observer):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # Configure main window.
        self.root.title("Ticket to Ride - London")
        self.root.geometry("800x600")
        
        # UI Elements.
        self.status_label = tk.Label(self.root, text="Loading game...", font=("Arial", 16))
        self.status_label.pack(pady=10)
        
        self.end_turn_btn = tk.Button(self.root, text="End Turn", command=self.handle_end_turn)
        self.end_turn_btn.pack(pady=5)
        
        # Trigger an initial update to populate the UI with starting data.
        self.update()

    def handle_end_turn(self):
        self.controller.end_turn()

    def update(self):
        # This method is called by the Subject (TurnManager) via self.notify().
        current_player = self.controller.current_player()
        
        if self.controller.game_over():
            winners = self.controller.winners()
            winner_names = ", ".join([w.name for w in winners])
            self.status_label.config(text=f"Game Over! Winners: {winner_names}")
            self.end_turn_btn.config(state=tk.DISABLED)
        elif current_player:
            self.status_label.config(
                text=f"Current Turn: {current_player.name} | "
                     f"Score: {current_player.score} | "
                     f"Buses Left: {current_player.trains_left}"
            )