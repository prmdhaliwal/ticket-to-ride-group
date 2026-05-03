"""Main Tkinter window."""
import tkinter as tk
from tkinter import ttk, messagebox
from models.core import Observer

class MainWindow(Observer):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title("Ticket to Ride - London")
        self.root.geometry("1280x720")
        
        self.setup_ui()
        self.update()

    def setup_ui(self):
        self.status_label = ttk.Label(self.root, text="Loading game...", font=("Arial", 16))
        self.status_label.pack(pady=10)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        left_frame = ttk.LabelFrame(main_frame, text="Routes", padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.route_listbox = ttk.Treeview(left_frame, show="tree", selectmode="browse")
        self.route_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.claim_btn = ttk.Button(left_frame, text="Claim Route", command=self.claim_route, style="Accent.TButton")
        self.claim_btn.pack(pady=5)
        
        mid_frame = ttk.LabelFrame(main_frame, text="Actions & Cards", padding=10)
        mid_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        
        ttk.Label(mid_frame, text="Face-Up Cards").pack(anchor=tk.W, pady=(0, 5))
        self.pool_listbox = ttk.Treeview(mid_frame, show="tree", selectmode="browse", height=5)
        self.pool_listbox.pack(pady=(0, 10), fill=tk.X)
        
        self.draw_pool_btn = ttk.Button(mid_frame, text="Draw from Pool", command=self.draw_pool)
        self.draw_pool_btn.pack(pady=5, fill=tk.X)
        
        self.draw_deck_btn = ttk.Button(mid_frame, text="Draw 1 from Deck", command=self.draw_deck)
        self.draw_deck_btn.pack(pady=5, fill=tk.X)
        
        self.draw_tickets_btn = ttk.Button(mid_frame, text="Draw Tickets", command=self.draw_tickets)
        self.draw_tickets_btn.pack(pady=5, fill=tk.X)
        
        self.end_turn_btn = ttk.Button(mid_frame, text="End Turn", command=self.handle_end_turn, style="Accent.TButton")
        self.end_turn_btn.pack(pady=(20, 5), fill=tk.X)
        
        right_frame = ttk.LabelFrame(main_frame, text="Player Status", padding=10)
        right_frame.grid(row=0, column=2, sticky="nsew")
        
        self.hand_text = tk.Text(right_frame, width=40, state=tk.DISABLED)
        self.hand_text.pack(fill=tk.BOTH, expand=True)

    def handle_end_turn(self):
        msg = self.controller.end_turn()
        if msg == "The game is over." or msg == "Game over.":
            messagebox.showinfo("Game Over", msg)
        self.update()

    def claim_route(self):
        selection = self.route_listbox.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a route.")
            return
        index = self.route_listbox.index(selection[0])
        success, msg = self.controller.claim_route(index)
        if not success:
            messagebox.showerror("Error", msg)

    def draw_pool(self):
        selection = self.pool_listbox.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a face-up card.")
            return
        index = self.pool_listbox.index(selection[0])
        success, msg = self.controller.draw_train_card(from_deck=False, pool_index=index)
        if not success:
            messagebox.showerror("Error", msg)

    def draw_deck(self):
        success, msg = self.controller.draw_train_card(from_deck=True)
        if not success:
            messagebox.showerror("Error", msg)

    def draw_tickets(self):
        result, msg = self.controller.draw_destination_tickets()
        if result is False:
            messagebox.showerror("Error", msg)
            return

        self.show_ticket_selection(result)

    def show_ticket_selection(self, tickets):
        top = tk.Toplevel(self.root)
        top.title("Select Tickets")
        top.protocol("WM_DELETE_WINDOW", lambda: None) # Disable closing window
        
        ttk.Label(top, text="Select tickets to keep:").pack(pady=(15, 10), padx=20)
        
        check_frame = ttk.Frame(top)
        check_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        ticket_vars = []
        for t in tickets:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(check_frame, text=f"{t.from_city} to {t.to_city} ({t.points})", variable=var)
            cb.pack(anchor=tk.W, pady=2)
            ticket_vars.append(var)
            
        def confirm():
            kept = []
            returned = []

            for index, var in enumerate(ticket_vars):
                if var.get():
                    kept.append(tickets[index])
                else:
                    returned.append(tickets[index])

            success, msg = self.controller.keep_destination_tickets(kept_tickets=kept, returned_tickets=returned)
            if not success:
                messagebox.showerror("Error", msg)
            else:
                top.destroy()
            
        ttk.Button(top, text="Keep Selected", command=confirm, style="Accent.TButton").pack(pady=(15, 20), padx=20)

    def update(self):
        current_player = self.controller.current_player()
        
        if self.controller.game_over():
            winners = self.controller.winners()
            winner_names = ""

            for winner in winners:
                if winner_names:
                    winner_names += ", "

                winner_names += winner.name

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
            state = tk.NORMAL

            if turn_ended:
                state = tk.DISABLED

            self.claim_btn.config(state=state)
            self.draw_pool_btn.config(state=state)
            self.draw_deck_btn.config(state=state)
            self.draw_tickets_btn.config(state=state)
            self.end_turn_btn.config(state=tk.NORMAL if turn_ended else tk.DISABLED)
            
            # Efficiently update routes instead of delete/recreate
            routes = self.controller.get_routes()
            route_items = self.route_listbox.get_children()
            
            if len(route_items) != len(routes):
                self.route_listbox.delete(*route_items)
                for r in routes:
                    owner_name = r.owner.name if r.owner else "None"
                    self.route_listbox.insert("", tk.END, text=f"{r.city_a.name} - {r.city_b.name} ({r.length} {r.colour.value}) Owner: {owner_name}")
            else:
                for i, r in enumerate(routes):
                    owner_name = r.owner.name if r.owner else "None"
                    new_text = f"{r.city_a.name} - {r.city_b.name} ({r.length} {r.colour.value}) Owner: {owner_name}"
                    if self.route_listbox.item(route_items[i], "text") != new_text:
                        self.route_listbox.item(route_items[i], text=new_text)
                
            # Efficiently update pool
            cards = self.controller.get_face_up_cards()
            pool_items = self.pool_listbox.get_children()
            
            if len(pool_items) != len(cards):
                self.pool_listbox.delete(*pool_items)
                for c in cards:
                    self.pool_listbox.insert("", tk.END, text=c.colour.value)
            else:
                for i, c in enumerate(cards):
                    new_text = c.colour.value
                    if self.pool_listbox.item(pool_items[i], "text") != new_text:
                        self.pool_listbox.item(pool_items[i], text=new_text)
                
            self.hand_text.config(state=tk.NORMAL)
            self.hand_text.delete(1.0, tk.END)
            self.hand_text.insert(tk.END, "Cards:\n")
            
            card_counts = {}
            for c in current_player.train_cards:
                color = c.colour.value

                if color not in card_counts:
                    card_counts[color] = 0

                card_counts[color] += 1
                
            for color, count in card_counts.items():
                self.hand_text.insert(tk.END, f"- {color}: {count}\n")
                
            self.hand_text.insert(tk.END, "\nTickets:\n")
            for t in current_player.destination_tickets:
                self.hand_text.insert(tk.END, f"- {t.from_city} to {t.to_city} ({t.points})\n")
                
            self.hand_text.config(state=tk.DISABLED)
