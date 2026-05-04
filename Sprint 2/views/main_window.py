"""Main Tkinter window."""
import math
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from models.core import Observer
from models.core import CardColor

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

        self.route_canvas = tk.Canvas(
            left_frame,
            height=430,
            background="#f7f3e8",
            highlightthickness=0
        )
        self.route_canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.route_canvas.tag_bind("route", "<Button-1>", self.handle_canvas_route_click)
        self.route_canvas.bind("<Configure>", self.handle_map_resize)
        
        self.route_listbox = ttk.Treeview(left_frame, show="tree", selectmode="browse", height=6)
        self.route_listbox.pack(fill=tk.X, pady=(0, 10))
        self.route_listbox.bind("<<TreeviewSelect>>", self.handle_route_list_selection)
        
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

    def handle_map_resize(self, event):
        self.draw_map()

    def handle_route_list_selection(self, event):
        self.draw_map()

    def handle_canvas_route_click(self, event):
        selected = self.route_canvas.find_withtag("current")

        if not selected:
            return

        tags = self.route_canvas.gettags(selected[0])
        route_index = None

        for tag in tags:
            if tag.startswith("route_index_"):
                route_index = int(tag.replace("route_index_", ""))

        if route_index is not None:
            self.select_route(route_index)

    def select_route(self, route_index):
        route_items = self.route_listbox.get_children()

        if route_index < 0:
            return

        if route_index >= len(route_items):
            return

        selected_item = route_items[route_index]
        self.route_listbox.selection_set(selected_item)
        self.route_listbox.focus(selected_item)
        self.route_listbox.see(selected_item)
        self.draw_map()

    def selected_route_index(self):
        selection = self.route_listbox.selection()

        if not selection:
            return None

        return self.route_listbox.index(selection[0])

    def draw_map(self):
        if not hasattr(self, "route_canvas"):
            return

        routes = self.controller.get_routes()
        self.route_canvas.delete("all")

        if not routes:
            return

        bounds = self.map_bounds(routes)

        if bounds is None:
            self.route_canvas.create_text(
                20,
                20,
                anchor=tk.NW,
                text="No map coordinates found."
            )
            return

        self.draw_map_background()

        selected_index = self.selected_route_index()

        for index, route in enumerate(routes):
            self.draw_route(route, index, selected_index, bounds)

        drawn_cities = []

        for route in routes:
            for city in route.cities:
                if city.name not in drawn_cities:
                    self.draw_city(city, bounds)
                    drawn_cities.append(city.name)

    def map_bounds(self, routes):
        x_values = []
        y_values = []

        for route in routes:
            for point in route.visual_points:
                if point.get("x") is not None and point.get("y") is not None:
                    x_values.append(point.get("x"))
                    y_values.append(point.get("y"))

            for city in route.cities:
                if city.x is not None and city.y is not None:
                    x_values.append(city.x)
                    y_values.append(city.y)

        if not x_values or not y_values:
            return None

        return {
            "min_x": min(x_values),
            "max_x": max(x_values),
            "min_y": min(y_values),
            "max_y": max(y_values)
        }

    def draw_map_background(self):
        if not self.map_background_loaded:
            self.load_map_background()

        if self.map_background_image is None:
            return

        width = self.route_canvas.winfo_width()
        height = self.route_canvas.winfo_height()
        image_width = self.map_background_image.width()
        image_height = self.map_background_image.height()
        x = (width - image_width) / 2
        y = (height - image_height) / 2

        self.route_canvas.create_image(
            x,
            y,
            anchor=tk.NW,
            image=self.map_background_image
        )

    def load_map_background(self):
        self.map_background_loaded = True
        image_path = self.map_background_path()

        if not os.path.exists(image_path):
            return

        try:
            self.map_background_image = tk.PhotoImage(file=image_path)
        except tk.TclError:
            self.map_background_image = None

    def map_background_path(self):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        return os.path.join(base_path, "assets", "maps", "london_map.png")

    def to_canvas_point(self, x, y, bounds):
        width = self.route_canvas.winfo_width()
        height = self.route_canvas.winfo_height()

        if width < 100:
            width = 700

        if height < 100:
            height = 430

        padding = 40
        span_x = bounds["max_x"] - bounds["min_x"]
        span_y = bounds["max_y"] - bounds["min_y"]

        if span_x == 0:
            span_x = 1

        if span_y == 0:
            span_y = 1

        scale_x = (width - padding * 2) / span_x
        scale_y = (height - padding * 2) / span_y
        scale = min(scale_x, scale_y)

        used_width = span_x * scale
        used_height = span_y * scale
        offset_x = (width - used_width) / 2
        offset_y = (height - used_height) / 2

        canvas_x = offset_x + (x - bounds["min_x"]) * scale
        canvas_y = offset_y + (y - bounds["min_y"]) * scale

        return canvas_x, canvas_y

    def draw_route(self, route, index, selected_index, bounds):
        canvas_points = []

        if route.visual_points:
            for point in route.visual_points:
                x = point.get("x")
                y = point.get("y")

                if x is not None and y is not None:
                    canvas_x, canvas_y = self.to_canvas_point(x, y, bounds)
                    canvas_points.append(canvas_x)
                    canvas_points.append(canvas_y)
        else:
            for city in route.cities:
                if city.x is not None and city.y is not None:
                    canvas_x, canvas_y = self.to_canvas_point(city.x, city.y, bounds)
                    canvas_points.append(canvas_x)
                    canvas_points.append(canvas_y)

        if len(canvas_points) < 4:
            return

        colour = self.route_display_colour(route)
        tag = "route_index_" + str(index)

        self.route_canvas.create_line(
            canvas_points,
            fill="#d8d0c0",
            width=5,
            smooth=True,
            capstyle=tk.ROUND,
            tags=("route", tag)
        )

        if route.segment_points:
            self.draw_route_segments(route, index, selected_index, bounds)
        else:
            self.draw_route_fallback_segments(route, index, selected_index, canvas_points)

    def draw_route_segments(self, route, index, selected_index, bounds):
        colour = self.route_display_colour(route)
        outline = "#4a4037"
        segment_width = 26
        segment_height = 11

        if index == selected_index:
            segment_width = 30
            segment_height = 13
            outline = "#111111"

        tag = "route_index_" + str(index)

        for point in route.segment_points:
            x = point.get("x")
            y = point.get("y")
            rotation = point.get("rotation")

            if rotation is None:
                rotation = 0

            if x is not None and y is not None:
                canvas_x, canvas_y = self.to_canvas_point(x, y, bounds)
                self.draw_segment_shape(
                    canvas_x,
                    canvas_y,
                    rotation,
                    segment_width,
                    segment_height,
                    colour,
                    outline,
                    tag
                )

    def draw_route_fallback_segments(self, route, index, selected_index, canvas_points):
        colour = self.route_display_colour(route)
        outline = "#4a4037"
        segment_width = 26
        segment_height = 11

        if index == selected_index:
            segment_width = 30
            segment_height = 13
            outline = "#111111"

        tag = "route_index_" + str(index)
        start_x = canvas_points[0]
        start_y = canvas_points[1]
        end_x = canvas_points[-2]
        end_y = canvas_points[-1]
        rotation = math.atan2(end_y - start_y, end_x - start_x)

        for segment_index in range(route.length):
            fraction = (segment_index + 1) / (route.length + 1)
            x = start_x + (end_x - start_x) * fraction
            y = start_y + (end_y - start_y) * fraction
            self.draw_segment_shape(
                x,
                y,
                rotation,
                segment_width,
                segment_height,
                colour,
                outline,
                tag
            )

    def draw_segment_shape(self, x, y, rotation, width, height, colour, outline, tag):
        half_width = width / 2
        half_height = height / 2
        corners = [
            (-half_width, -half_height),
            (half_width, -half_height),
            (half_width, half_height),
            (-half_width, half_height)
        ]
        rotated_points = []

        for corner_x, corner_y in corners:
            rotated_x = x + corner_x * math.cos(rotation) - corner_y * math.sin(rotation)
            rotated_y = y + corner_x * math.sin(rotation) + corner_y * math.cos(rotation)
            rotated_points.append(rotated_x)
            rotated_points.append(rotated_y)

        self.route_canvas.create_polygon(
            rotated_points,
            fill=colour,
            outline=outline,
            width=2,
            tags=("route", tag)
        )

    def draw_city(self, city, bounds):
        if city.x is None or city.y is None:
            return

        x, y = self.to_canvas_point(city.x, city.y, bounds)
        radius = 7

        self.route_canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="#ffffff",
            outline="#222222",
            width=2
        )
        self.route_canvas.create_text(
            x,
            y - 15,
            text=city.name,
            font=("Arial", 8),
            fill="#1f1f1f"
        )

    def route_display_colour(self, route):
        if route.owner is not None:
            players = self.controller.players()
            player_colours = ["#1f66d1", "#c0392b", "#138a43", "#8e44ad"]

            for index, player in enumerate(players):
                if player == route.owner:
                    return player_colours[index % len(player_colours)]

            return "#2f2f2f"

        colours = {
            CardColor.BLUE: "#2f6fd6",
            CardColor.GREEN: "#228b45",
            CardColor.YELLOW: "#d9a521",
            CardColor.BLACK: "#333333",
            CardColor.ORANGE: "#d66b2f",
            CardColor.PINK: "#d85aa6",
            CardColor.RED: "#c94b4b",
            CardColor.WHITE: "#e8e8e8",
            CardColor.PURPLE: "#8056c9",
            CardColor.GRAY: "#8c9299",
            CardColor.LOCOMOTIVE: "#5d5d5d"
        }

        if route.colour in colours:
            return colours[route.colour]

        return "#8c9299"

    def handle_end_turn(self):
        msg = self.controller.end_turn()
        if msg not in ["Next turn.", "The game is over.", "Game over."]:
            messagebox.showwarning("Warning", msg)
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

            self.draw_map()
                
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
