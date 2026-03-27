import tkinter as tk

class TicketToRidePrototype:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket to Ride")
        self.root.geometry("430x260")

        self.colour_var = tk.StringVar(value="blue")
        self.status_var = tk.StringVar(value="Pick a colour and try the route.")

        self.setup_data()

        # main parts
        self.title_label = tk.Label(
            root,
            text="Ticket to Ride Prototype",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=12)

        self.route_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            justify="left"
        )
        self.route_label.pack(pady=4)

        self.player_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            justify="left"
        )
        self.player_label.pack(pady=4)

        self.hand_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            justify="left"
        )
        self.hand_label.pack(pady=4)

        # controls
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=10)

        self.colour_text = tk.Label(self.controls_frame, text="Colour", font=("Arial", 11))
        self.colour_text.grid(row=0, column=0, padx=4)

        self.colour_menu = tk.OptionMenu(self.controls_frame, self.colour_var, "blue", "red", "black", "white", "yellow")
        self.colour_menu.grid(row=0, column=1, padx=4)

        self.claim_button = tk.Button(
            self.controls_frame,
            text="Claim Route",
            command=self.handle_claim,
            font=("Arial", 11)
        )
        self.claim_button.grid(row=0, column=2, padx=6)

        self.reset_button = tk.Button(
            self.controls_frame,
            text="Reset",
            command=self.handle_reset,
            font=("Arial", 11)
        )
        self.reset_button.grid(row=0, column=3, padx=6)

        # result
        self.status_label = tk.Label(
            root,
            textvariable=self.status_var,
            font=("Arial", 11),
            justify="center",
            wraplength=380
        )
        self.status_label.pack(pady=10)

        self.update_labels()

    def setup_data(self):
        self.route_name = "Montreal - New York"
        self.route_colour = "blue"
        self.route_length = 3
        self.route_points = 4
        self.route_claimed = False

        self.player_name = "Player 1"
        self.trains = 45
        self.score = 0
        self.hand = {
            "blue": 3,
            "red": 2,
            "black": 1,
            "white": 1,
            "yellow": 1,
            "locomotive": 1
        }

    def update_labels(self):
        # route info
        if self.route_claimed:
            route_status = "Claimed"
        else:
            route_status = "Open"

        self.route_label.config(
            text=f"Route: {self.route_name} | Colour: {self.route_colour} | Length: {self.route_length} | {route_status}"
        )

        # player info
        self.player_label.config(
            text=f"Player: {self.player_name} | Trains: {self.trains} | Score: {self.score}"
        )

        self.hand_label.config(
            text="Hand: "
            + "blue "
            + str(self.hand["blue"])
            + ", red "
            + str(self.hand["red"])
            + ", black "
            + str(self.hand["black"])
            + ", white "
            + str(self.hand["white"])
            + ", yellow "
            + str(self.hand["yellow"])
            + ", locomotive "
            + str(self.hand["locomotive"])
        )

    def handle_claim(self):
        chosen_colour = self.colour_var.get()

        # checks
        if self.route_claimed:
            self.status_var.set("Route already claimed.")
            return

        if chosen_colour != self.route_colour:
            self.status_var.set("Wrong colour for this route.")
            return

        total_cards = self.hand[chosen_colour] + self.hand["locomotive"]

        if total_cards < self.route_length:
            self.status_var.set("Not enough cards.")
            return

        if self.trains < self.route_length:
            self.status_var.set("Not enough trains.")
            return

        # spend cards
        cards_left = self.route_length

        while cards_left > 0 and self.hand[chosen_colour] > 0:
            self.hand[chosen_colour] = self.hand[chosen_colour] - 1
            cards_left = cards_left - 1

        while cards_left > 0 and self.hand["locomotive"] > 0:
            self.hand["locomotive"] = self.hand["locomotive"] - 1
            cards_left = cards_left - 1

        # update values
        self.trains = self.trains - self.route_length
        self.score = self.score + self.route_points
        self.route_claimed = True

        self.status_var.set("Route claimed.")
        self.update_labels()

    def handle_reset(self):
        self.setup_data()
        self.colour_var.set("blue")
        self.status_var.set("Back to start.")
        self.update_labels()


def main():
    root = tk.Tk()
    app = TicketToRidePrototype(root)
    root.mainloop()


if __name__ == "__main__":
    main()
