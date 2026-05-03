"""Application entrypoint."""

import tkinter as tk
from controllers.game_setup import GameSetup
from controllers.game_controller import GameController
from models.map_definition import MapDefinition
from views.main_window import MainWindow

def main():
    # Bootstrap the backend.
    london_map = MapDefinition.create_london_map()
    setup = GameSetup()
    players = ["Bob", "Alice"] # Hardcoded for now.
    
    turn_manager = setup.set_up_game(london_map, players)
    
    controller = GameController(turn_manager)
    
    root = tk.Tk()
    main_window = MainWindow(root, controller)
    
    turn_manager.attach(main_window)
    
    root.mainloop()

if __name__ == "__main__":
    main()