from models.map_definition import MapDefinition
from controllers.game_setup import GameSetup

def main():
    print("--- Ticket to Ride: London Setup ---\n")

    # 1. Load the London Map Configuration
    london_map = MapDefinition.create_london_map()

    # 2. Boot up the setup controller
    setup = GameSetup()
    
    # 3. Create the TurnManager (which holds the entire game state)
    game_manager = setup.setUpGame(london_map, ["Prabhjot", "Param"])

    print("--- Setup Complete ---")
    
    # Verify player data
    for player in game_manager._players:
        print(player)
        print(f"  Transport Hand: {len(player._trainCards)} cards")
        print(f"  Destination Tickets: {len(player._tickets)} tickets\n")

    # Verify the board state
    print("--- Board State ---")
    print(f"Face-up pool: {[str(card) for card in game_manager._face_up_pool._faceUpCards]}")
    
    # Prove the TurnManager works
    print(f"\nCurrent Player: {game_manager.getCurrentPlayer().name}")

if __name__ == "__main__":
    main()