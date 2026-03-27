import tkinter as tk

import random

class DestinationTicketDeck:

    def __init__(self):

        self.tickets = [
            "Montreal - New York",
            "Toronto - Chicago",
            "Vancouver - Montreal",
            "Los Angeles - Miami",
            "Portland - Nashville",
            "Seattle - Los Angeles",
            "Calgary - Phoenix"
        ]

        random.shuffle(self.tickets)

    def draw_tickets(self, count=3):

        drawn = []
        for _ in range(count):
            if self.tickets:
                drawn.append(self.tickets.pop())
        return drawn

class TicketToRidePrototype:

    def __init__(self, root):
        self.root = root
        self.root.title("Ticket to Ride")
        self.root.geometry("350x250")
        self.deck = DestinationTicketDeck()
        self.title_label = tk.Label(

            root,
            text="Ticket to Ride Prototype",
            font=("Arial", 16, "bold")
        )

        self.title_label.pack(pady=15)
        self.draw_button = tk.Button(
            root,
            text="Draw Destination Tickets",
            command=self.handle_draw,
            font=("Arial", 12)
        )

        self.draw_button.pack(pady=10)
        self.result_label = tk.Label(

            root,
            text="",
            font=("Arial", 12),
            justify="center"
        )

        self.result_label.pack(pady=15)

    def handle_draw(self):
        """Handles the button click event."""
        new_tickets = self.deck.draw_tickets(3)

        if not new_tickets:
            self.result_label.config(text="The deck is empty!")
            return

        display_text = "\n".join(new_tickets)
        self.result_label.config(text=display_text)

if __name__ == "__main__":

    root = tk.Tk()
    app = TicketToRidePrototype(root)
    root.mainloop()