# Ticket to Ride: London

I built this desktop adaptation of Ticket to Ride: London with my team during FIT3077 at Monash University in 2026. We took the project from UML designs and individual prototypes to a shared Python application, using object-oriented models, controllers and a Tkinter interface.

## What We Built

- A local, turn-based game for two to four players.
- A London board drawn from JSON map data, with routes, destination tickets and player scores.
- Transport-card drawing, route claiming, starting-ticket selection and end-game scoring.
- A themed Tkinter interface using `sv-ttk`.

## My Contribution

I contributed under `prmdhaliwal` and `pdha0007`.

- I developed route-claiming and scoring logic, including card payment, route availability, ticket completion, final scoring and tie-breaking.
- I connected London map data to the board display and refined player-count validation and starting-ticket selection.
- I added automated rule tests and worked on integration across the shared models and controllers.
- I created a route-claiming prototype and contributed the turn-structure sequence diagram.

We kept each teammate's early prototype in `prototypes/`. The repository retains our individual contributions and shared development history.

## Design

We separated the application into game models, controllers and Tkinter views. The board layout and route geometry live in JSON, while the game objects hold the state and rules.

- [`Sprint 2/models/`](Sprint%202/models): players, cards, routes, tickets, turns and scoring.
- [`Sprint 2/controllers/`](Sprint%202/controllers): setup and game-action coordination.
- [`Sprint 2/views/`](Sprint%202/views): setup window, board and player controls.
- [`Sprint 2/assets/maps/`](Sprint%202/assets/maps): London map configuration.

Our early design artifacts include the [domain model](Sprint%201/Domain_Model.png), [setup sequence](Sprint%201/Game_Setup_Sequence_diagram.jpeg) and [turn-structure sequence](Sprint%201/final_turn_sequence_diagram.png). These show our initial design, before later implementation changes.

## Run Locally

I use Python with Tkinter and `sv-ttk`. From PowerShell on Windows:

```powershell
git clone https://github.com/prmdhaliwal/ticket-to-ride-group.git
cd ticket-to-ride-group
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe "Sprint 2/main.py"
```

Enter the player names in the setup window to start a game. The source does not require an account, database or external service.

## Tests

```powershell
./.venv/Scripts/python.exe -B -m unittest discover -s "Sprint 2/tests" -v
```

The current suite runs 14 tests: 12 pass and two error because they still reference the removed `MapDefinition.districts` and `add_district` API. They need to be brought into line with the final scoring model. The passing checks cover setup, card drawing, starting-ticket choices and controller delegation.

## Individual Continuation

I continued this shared codebase in a separate [individual final sprint](https://github.com/prmdhaliwal/ticket-to-ride-individual), refactoring the design and adding ferry routes, a visible ticket market and configurable maps.
