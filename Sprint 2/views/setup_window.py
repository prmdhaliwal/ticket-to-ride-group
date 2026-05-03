import tkinter as tk
import sv_ttk
from tkinter import ttk, messagebox

class SetupWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Setup")
        self.geometry("300x300")
        self.players = []
        
        ttk.Label(self, text="Number of Players (2-4):").pack(pady=5)
        
        self.num_var = tk.IntVar(value=2)
        self.num_spinbox = ttk.Spinbox(self, from_=2, to=4, textvariable=self.num_var, command=self.update_player_entries)
        self.num_spinbox.pack(pady=5)
        
        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.player_entries = []
        self.update_player_entries()
        
        ttk.Button(self, text="Start Game", command=self.start_game, style="Accent.TButton").pack(pady=20)
        
        # Center the window
        self.eval('tk::PlaceWindow . center')

        sv_ttk.set_theme("light")
        
    def update_player_entries(self):
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
            
        self.player_entries.clear()
        
        try:
            num = self.num_var.get()
            if num < 2 or num > 4:
                return
        except tk.TclError:
            return
            
        for i in range(num):
            frame = ttk.Frame(self.entries_frame)
            frame.pack(fill=tk.X, padx=10, pady=2)
            ttk.Label(frame, text=f"Player {i+1} Name:").pack(side=tk.LEFT, padx=(20, 10))
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
            self.player_entries.append(entry)

    def start_game(self):
        names = []
        for entry in self.player_entries:
            name = entry.get().strip()
            if not name:
                messagebox.showerror("Error", "All player names must be filled out.", parent=self)
                return
            names.append(name)
            
        self.players = names
        self.destroy()

def get_player_names():
    dialog = SetupWindow()
    dialog.mainloop()
    return dialog.players
