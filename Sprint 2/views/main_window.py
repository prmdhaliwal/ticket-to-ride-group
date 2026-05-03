"""Main Tkinter window."""
import tkinter as tk
from tkinter import messagebox
from models.core import Observer

class MainWindow(Observer):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title("Ticket to Ride - London")
        self.root.geometry("1000x600")
        
        self.setup_ui()
        self.update()

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="Loading game...", font=("Arial", 16))
        self.status_label.pack(pady=10)
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(left_frame, text="Routes").pack()
        
        self.route_listbox = tk.Listbox(left_frame, width=50)
        self.route_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.claim_btn = tk.Button(left_frame, text="Claim Route", command=self.claim_route)
        self.claim_btn.pack(pady=5)
        
        mid_frame = tk.Frame(main_frame)
        mid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(mid_frame, text="Face-Up Cards").pack()
        
        self.pool_listbox = tk.Listbox(mid_frame, width=30, height=5)
        self.pool_listbox.pack()
        
        self.draw_pool_btn = tk.Button(mid_frame, text="Draw from Pool", command=self.draw_pool)
        self.draw_pool_btn.pack(pady=5)
        
        self.draw_deck_btn = tk.Button(mid_frame, text="Draw 1 from Deck", command=self.draw_deck)
        self.draw_deck_btn.pack(pady=5)
        
        self.draw_tickets_btn = tk.Button(mid_frame, text="Draw Tickets", command=self.draw_tickets)
        self.draw_tickets_btn.pack(pady=5)
        
        self.end_turn_btn = tk.Button(mid_frame, text="End Turn", command=self.handle_end_turn)
        self.end_turn_btn.pack(pady=20)
        
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(right_frame, text="Player Status").pack()
        
        self.hand_text = tk.Text(right_frame, width=40, state=tk.DISABLED)
        self.hand_text.pack(fill=tk.BOTH, expand=True)

    def handle_end_turn(self):
        msg = self.controller.end_turn()
        if msg == "The game is over." or msg == "Game over.":
            messagebox.showinfo("Game Over", msg)
        self.update()

    def claim_route(self):
        selection = self.route_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a route.")
            return
        success, msg = self.controller.claim_route(selection[0])
        if not success:
            messagebox.showerror("Error", msg)

    def draw_pool(self):
        selection = self.pool_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a face-up card.")
            return
        success, msg = self.controller.draw_train_card(from_deck=False, pool_index=selection[0])
        if not success:
            messagebox.showerror("Error", msg)

    def draw_deck(self):
        success, msg = self.controller.draw_train_card(from_deck=True)
        if not success:
            messagebox.showerror("Error", msg)

    def draw_tickets(self):
        result, msg = self.controller.draw_destination_tickets()
        if not isinstance(result, list):
            messagebox.showerror("Error", msg)
            return
        self.show_ticket_selection(result)

    def show_ticket_selection(self, tickets):
        top = tk.Toplevel(self.root)
        top.title("Select Tickets")
        top.geometry("300x200")
        
        tk.Label(top, text="Select tickets to keep:").pack()
        listbox = tk.Listbox(top, selectmode=tk.MULTIPLE, width=40)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        for t in tickets:
            listbox.insert(tk.END, f"{t.from_city} to {t.to_city} ({t.points})")
            
        def confirm():
            selection = listbox.curselection()
            kept = [tickets[i] for i in selection]
            returned = [tickets[i] for i in range(len(tickets)) if i not in selection]
            success, msg = self.controller.keep_destination_tickets(kept_tickets=kept, returned_tickets=returned)
            if not success:
                messagebox.showerror("Error", msg)
            else:
                top.destroy()
            
        tk.Button(top, text="Keep Selected", command=confirm).pack(pady=5)

    def update(self):
        current_player = self.controller.current_player()
        
        if self.controller.game_over():
            winners = self.controller.winners()
            if isinstance(winners, list):
                winner_names = ", ".join([w.name for w in winners])
            else:
                winner_names = winners.name
            self.status_label.config(text=f"Game Over! Winners: {winner_names}")
            self.end_turn_btn.config(state=tk.DISABLED)
            
            scores = self.controller.final_scores()
            score_text = "Final Scores:\n"
            for p, s in scores.items():
                score_text += f"{p.name}: {s}\n"
            messagebox.showinfo("Game Over", score_text)
            return
            
        if current_player:
            self.status_label.config(
                text=f"Current Turn: {current_player.name} | "
                     f"Score: {current_player.score} | "
                     f"Buses: {current_player.trains_left}"
            )
            
            turn_ended = self.controller.turn_ended()
            state = tk.DISABLED if turn_ended else tk.NORMAL
            self.claim_btn.config(state=state)
            self.draw_pool_btn.config(state=state)
            self.draw_deck_btn.config(state=state)
            self.draw_tickets_btn.config(state=state)
            self.end_turn_btn.config(state=tk.NORMAL)
            
            self.route_listbox.delete(0, tk.END)
            for r in self.controller.get_routes():
                owner_name = r.owner.name if r.owner else "None"
                self.route_listbox.insert(tk.END, f"{r.city_a.name} - {r.city_b.name} ({r.length} {r.colour.value}) Owner: {owner_name}")
                
            self.pool_listbox.delete(0, tk.END)
            for c in self.controller.get_face_up_cards():
                self.pool_listbox.insert(tk.END, c.colour.value)
                
            self.hand_text.config(state=tk.NORMAL)
            self.hand_text.delete(1.0, tk.END)
            self.hand_text.insert(tk.END, "Cards:\n")
            
            card_counts = {}
            for c in current_player.train_cards:
                color = c.colour.value
                card_counts[color] = card_counts.get(color, 0) + 1
                
            for color, count in card_counts.items():
                self.hand_text.insert(tk.END, f"- {color}: {count}\n")
                
            self.hand_text.insert(tk.END, "\nTickets:\n")
            for t in current_player.destination_tickets:
                self.hand_text.insert(tk.END, f"- {t.from_city} to {t.to_city} ({t.points})\n")
                
            self.hand_text.config(state=tk.DISABLED)