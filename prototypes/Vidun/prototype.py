import tkinter as tk
import random

class TrainCarDeck:
    def __init__(self):
        # 12 of each of the 8 colors, plus 14 Locomotives.
        colors = ['Purple', 'Blue', 'Orange', 'White', 'Green', 'Yellow', 'Black', 'Red']
        self.cards = [color for color in colors for _ in range(12)]
        self.cards.extend(['Locomotive'] * 14)
        random.shuffle(self.cards)

    def draw(self):
        """Draws a single card from the deck."""
        return self.cards.pop() if self.cards else None

class TicketToRidePrototype:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket to Ride - Draw Train Cards")
        
        # Initialise domain data.
        self.deck = TrainCarDeck()
        self.face_up_cards = [self.deck.draw() for _ in range(5)] # 5 face-up cards.
        self.player_hand = []

        # UI Elements.
        self.lbl_hand = tk.Label(root, text="Hand: Empty", wraplength=400)
        self.lbl_hand.pack(pady=10)

        self.lbl_deck = tk.Label(root, text=f"Cards in Deck: {len(self.deck.cards)}")
        self.lbl_deck.pack()

        # Face-up pool buttons.
        self.pool_frame = tk.Frame(root)
        self.pool_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(5):
            btn = tk.Button(self.pool_frame, text=self.face_up_cards[i], width=10,
                            command=lambda idx=i: self.draw_face_up(idx))
            btn.grid(row=0, column=i, padx=5)
            self.buttons.append(btn)

        # Blind draw button.
        self.btn_blind = tk.Button(root, text="Draw Blind from Deck", command=self.draw_blind)
        self.btn_blind.pack(pady=10)

    def update_ui(self):
        """Refreshes the GUI after a card is drawn."""
        hand_text = ", ".join(self.player_hand) if self.player_hand else "Empty"
        self.lbl_hand.config(text=f"Hand: {hand_text}")
        self.lbl_deck.config(text=f"Cards in Deck: {len(self.deck.cards)}")
        
        for i in range(5):
            card = self.face_up_cards[i]
            self.buttons[i].config(text=card if card else "Empty", 
                                   state=tk.NORMAL if card else tk.DISABLED)

    def draw_face_up(self, index):
        """Logic for clicking a face-up card."""
        card = self.face_up_cards[index]
        if card:
            self.player_hand.append(card)
            # Immediately replace the drawn face-up card.
            self.face_up_cards[index] = self.deck.draw()
            self.update_ui()

    def draw_blind(self):
        """Logic for clicking the blind draw button."""
        card = self.deck.draw()
        if card:
            self.player_hand.append(card)
            self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketToRidePrototype(root)
    root.mainloop()
