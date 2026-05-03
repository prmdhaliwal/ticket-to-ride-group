# Ticket to Ride Sprint 2 Class Diagram Rationale

## Rationale Method

The Week 7 guidance states that a good design rationale should make the reasoning behind a design decision visible. Each major design choice below is therefore written around four parts: the issue or decision point, the alternatives considered, the advantages and disadvantages of those alternatives, and the final decision with justification. This avoids merely describing the class diagram and instead explains why the selected design is preferable for the Sprint 2 Ticket to Ride implementation.

The Sprint 2 brief requires the class diagram to cover setup, drawing Train Car cards, claiming routes, drawing Destination Tickets, final-round detection, final scoring, and winner determination. The design rationale also needs to justify key classes, relationships, inheritance, cardinalities, and design-pattern usage. Our design is intentionally focused on core game logic; full Tkinter component classes are not expanded in the diagram, although a small `GameObserver` interface is included so the Observer pattern can be shown without cluttering the model with UI widgets.

## Decision 1: Separating Game Setup From Turn Flow

**Issue:** Should setup and turn execution be handled by one central class, or should they be separated into focused classes?

**Alternative A: One central game/session class.**  
This option is initially simple because one class can create the board, create players, deal cards, process turns, check final-round conditions, score the game, and update the UI. However, this quickly becomes a God Class. It would have many unrelated reasons to change: map setup, turn rules, card drawing, route claiming, final scoring, and UI events. This would reduce cohesion and make future Sprint 3 changes risky.

**Alternative B: Separate `GameSetup`, `TurnManager`, and `EndGameTracker`.**  
This option introduces more classes, so there is slightly more structure to understand. However, each class has a focused responsibility. `GameSetup` creates the initial game state, `TurnManager` coordinates legal turn actions and player order, and `EndGameTracker` handles only the final-round trigger and game-over state.

**Decision with rationale:** We chose Alternative B. The extra classes are justified because setup, turn flow, and final-round tracking change for different reasons. This design avoids the God Class anti-pattern while keeping the diagram simple enough for Sprint 2. It also improves testability because setup, turn progression, and end-game conditions can be tested separately.

## Decision 2: Data-Driven Map Extensibility

**Issue:** How should the design support future maps without editing core game logic for every new city or board layout?

**Alternative A: Formal Factory Method with map-specific subclasses.**  
This would use classes such as `LondonMapFactory`, `NewYorkMapFactory`, or `MelbourneMapFactory`. It is extensible in the sense that a new map can be added by creating another factory subclass. It is also a recognisable GoF design pattern. However, it creates class-driven extensibility: every new map needs new code even when the differences are only city data, route data, ticket data, player limits, and score values. This risks Speculative Generality because it introduces a factory hierarchy before the design needs map-specific creation behaviour.

**Alternative B: Adapter for maps.**  
An Adapter would be useful if the project had to import an incompatible external map format, such as a third-party JSON, XML, or legacy map class. Its advantage is that it can protect the domain model from external interfaces. However, the current design does not have an incompatible external interface. We already control the map structure, so using Adapter now would mostly convert our own data into our own data.

**Alternative C: Data-driven `MapDefinition`.**  
This option stores map-specific variation as data: cities, routes, destination tickets, district definitions, route score values, player limits, and initial train pieces. The disadvantage is that map data must be validated carefully in implementation. However, it avoids subclass explosion and supports adding future maps by adding new map definitions rather than new class hierarchies.

**Decision with rationale:** We chose Alternative C. `MapDefinition` is the best fit because the map variations are primarily data variations, not different object-creation algorithms. This satisfies the Open/Closed Principle in a practical way: future maps can be added through new map data while core classes such as `TurnManager`, `BoardMap`, `Player`, and `StandardScoring` remain stable. Factory Method and Adapter were considered but rejected because they solve problems the current design does not have.

## Decision 3: Scoring Strategy

**Issue:** Where should final scoring logic live, and how should the design support possible future scoring variations?

**Alternative A: Put all scoring in `TurnManager` or `EndGameTracker`.**  
This keeps the number of classes lower, but it gives turn-flow classes responsibility for final scoring. It also makes those classes harder to maintain because turn sequencing, final-round detection, ticket evaluation, district completion, and winner resolution become mixed together.

**Alternative B: Put scoring directly on `Player`.**  
This works for simple score updates, such as moving a score marker after claiming a route. However, final scoring depends on multiple players, the board, claimed routes, Destination Tickets, district data, and tie-break rules. A single player does not naturally own all of that information.

**Alternative C: Use the Strategy pattern with `ScoringStrategy` and `StandardScoring`.**  
This introduces an interface and a concrete scoring implementation. The small cost is another abstraction. The benefit is that scoring is treated as an interchangeable algorithm. Future scoring variants can be introduced without changing the board, player, route, or turn-management classes.

**Decision with rationale:** We chose Alternative C. `ScoringStrategy` is a suitable Strategy pattern because final scoring is an algorithm that may vary across future rule versions or maps. `StandardScoring` handles the Ticket to Ride: London final-scoring behaviour: claimed route points already recorded during play, completed Destination Tickets added, incomplete Destination Tickets subtracted, completed Districts added, and tied winners resolved by completed Destination Ticket count. This keeps scoring cohesive and avoids switch-style scoring logic inside unrelated classes.

## Decision 4: Observer For UI Updates

**Issue:** How should the game update the Tkinter UI when the model changes without coupling domain classes directly to Tkinter widgets?

**Alternative A: Direct UI references in domain classes.**  
`TurnManager` or `BoardMap` could directly call methods on Tkinter view classes after a route is claimed, a card is drawn, or the turn changes. This is easy at first, but it creates tight coupling between game logic and the UI library. It also creates Inappropriate Intimacy because domain classes would know too much about presentation details.

**Alternative B: Observer pattern using `GameObserver`.**  
The domain layer keeps a list of observers and notifies them through an abstract `update(event: String)` method. The concrete Tkinter view can implement this interface in the implementation, but the UML does not need to show every Tkinter component. The disadvantage is that event flow can be slightly less direct to trace. The advantage is that `TurnManager` depends only on an abstraction, not on Tkinter.

**Decision with rationale:** We chose Alternative B. The diagram includes `GameObserver` as the minimal Observer interface required to show the pattern. `TurnManager` acts as the subject/publisher and notifies observers when game state changes. This supports MVC-style separation while keeping the class diagram focused on core game logic. It also improves testability because tests can attach a fake observer without constructing Tkinter windows.

## Decision 5: Card Polymorphism

**Issue:** How should the design handle normal coloured Train Car cards and Locomotive cards without scattering type checks across the system?

**Alternative A: One `TrainCarCard` class with type fields and conditionals.**  
This would be simple initially, but it would push checks such as `if card.colour == LOCOMOTIVE` into route-claiming or draw logic. As more card-specific rules are added, the design risks switch statements and repeated conditionals.

**Alternative B: Use polymorphism with `TrainCarCard`, `ColouredCarCard`, and `LocomotiveCard`.**  
This option uses inheritance only where there is real behavioural variation. Both concrete card types respond to `matches(colour)`, but they can implement the answer differently. The disadvantage is that it adds two small subclasses. The advantage is that card-specific behaviour stays with the card object itself. This is especially useful for route claiming because Bus cards can act as wild cards without forcing `TurnManager` to inspect every card type manually.

**Decision with rationale:** We chose Alternative B. This is not a GoF pattern in the same sense as Strategy or Observer, but it is a core object-oriented design mechanism taught in the unit. It avoids switch statements and Feature Envy because route-claiming logic can ask cards whether they match a route instead of inspecting their internal type.

## Decision 6: Turn Actions And Command Pattern

**Issue:** Should drawing cards, claiming routes, and drawing destination tickets be represented as separate command objects?

**Alternative A: Use Command with action classes.**  
This would create classes such as `DrawTrainCardsAction`, `ClaimRouteAction`, and `DrawDestinationTicketsAction`. The advantage is that actions could later support undo, replay, logging, or action queues. The disadvantage is that the Sprint 2 prototype does not currently require those features, so the action classes would mostly be short-lived delegators.

**Alternative B: Keep legal turn choices as methods on `TurnManager`.**  
This keeps the diagram shorter and easier to read. The disadvantage is that `TurnManager` must be monitored so it does not grow into a God Class. The design controls this by limiting `TurnManager` to turn flow and delegating resource/route behaviour to `Player`, `Route`, decks, and `BoardMap`.

**Decision with rationale:** We chose Alternative B and rejected Command. In this context, Command would risk the Poltergeists anti-pattern because the action objects would exist mainly to pass data briefly and then disappear. If Sprint 3 introduces undo, replay, AI turns, or queued network actions, Command can be reconsidered with stronger justification.

## Key Classes

`GameSetup` is included because initialising a Ticket to Ride game coordinates many objects: map data, players, board, train-card deck, destination-ticket deck, starting cards, tickets, train pieces, and score markers. This is not naturally owned by `Player`, `BoardMap`, or a deck. Keeping setup in one focused class prevents setup logic from leaking into unrelated domain classes.

`TurnManager` is included because turn order is system-level game flow, not a responsibility of any individual player or route. It tracks the current player, enforces one action per turn, exposes the legal turn choices, advances turns, and delegates final-round checks. It coordinates route claiming, but the actual rule data remains on `Route`, `Player`, `TrainCarCard`, and `BoardMap`. It is deliberately not responsible for setup, final scoring, map definition, or UI rendering.

`EndGameTracker` is included because final-round state is distinct from normal turn order. It tracks whether the final round has started, which player triggered it, how many final turns remain, and whether the game is over. Keeping this separate stops `TurnManager` from growing back into an all-purpose manager.

## Key Relationships

`BoardMap` contains `City` and `Route` objects because those objects form the playable board structure. The relationship is shown as whole-part ownership because cities and routes belong to a specific board instance during a game.

`Player` owns one `ScoringMarker` because the score marker represents that player's current score-track position. We considered storing score directly as an integer on `Player`, but kept `ScoringMarker` because it reflects an actual Ticket to Ride component and separates player resources from score-track position.

`BoardMap` stores district definitions and route score values copied from `MapDefinition`. This keeps London-specific board data out of `TurnManager` and `StandardScoring`, while still allowing scoring and route claiming to read the current map's data.

`TurnManager` aggregates `GameObserver` objects because observers are attached to receive updates but are not owned permanently by the manager. A Tkinter view or a test observer can be added or removed without changing `TurnManager`'s core turn-flow responsibility.

## Inheritance Decisions

Inheritance is used for `TrainCarCard` because coloured cards and locomotive cards share a common role but may answer matching rules differently. This is justified because it supports polymorphic behaviour and avoids type-checking conditionals.

Inheritance is also used through the `ScoringStrategy` interface because scoring is an interchangeable algorithm. `StandardScoring` is the current concrete strategy, but future scoring variants can be added without modifying the classes that use the strategy.

Inheritance is deliberately not used for maps. A subclass tree such as `LondonMap`, `NewYorkMap`, or `MelbourneMap` would make future maps class-driven rather than data-driven. Since map variation is mostly data, `MapDefinition` is a better fit.

## Cardinality Decisions

`TurnManager` manages `2..4` players because Ticket to Ride London supports two to four players. Sprint 2 may implement two players first, but keeping the cardinality at `2..4` shows that the turn model is compatible with future three- and four-player functionality.

`Route` has `0..1` owner because a route starts unclaimed and can later be claimed by exactly one player. It cannot have multiple owners, and it should not require an owner before the game begins.

`FaceUpPool` contains `0..5` face-up Train Car cards. It normally displays five cards, but the lower bound allows temporary states during setup, refresh, or deck exhaustion.

## Anti-Pattern Rationale

The design avoids the God Class or Blob anti-pattern by distributing responsibility. `GameSetup` handles setup, `TurnManager` handles turn flow, `EndGameTracker` handles final-round state, `StandardScoring` handles scoring, and the domain classes own their own state and behaviour.

The design avoids an Anemic Domain Model by keeping behaviour near the data it uses. `Player` manages cards, tickets, train pieces, and score movement. `Route` manages availability, ownership, route length, double-route restrictions, and card acceptance. `DestinationTicket` can check completion. `TrainCarCard` subclasses answer whether they match route colours.

The design avoids Speculative Generality by not adding map-specific factory subclasses, command action classes, repositories, validators, or adapters before they are needed. These may become useful later, but the Sprint 2 design should not introduce abstractions only for imagined future requirements.

The design avoids Poltergeists by rejecting short-lived command/action objects for simple turn actions. Since undo, replay, and action queues are not current requirements, direct turn methods are clearer and easier to trace.

The design avoids switch statements by using Strategy for scoring and polymorphism for cards. Instead of a large conditional block deciding how final scoring or card matching works, those behaviours are encapsulated in dedicated objects.

The design avoids Inappropriate Intimacy between the model and Tkinter UI by using the Observer pattern. `TurnManager` notifies `GameObserver` rather than calling Tkinter-specific view methods directly.

The design avoids Singleton/global game state because global access would make testing and future map/player extensions harder. Game state is passed through collaborating objects rather than retrieved through a global `GameManager.getInstance()` style dependency.

## Overall Justification

The final design balances Sprint 2 readability with enough architectural depth to show object-oriented design quality. Strategy is used where the algorithm genuinely varies: final scoring. Observer is used where decoupling is needed: notifying the UI without depending on Tkinter. Polymorphism is used where object behaviour naturally differs: coloured cards and locomotive cards. Command, Factory Method, Adapter, and Template Method were considered but rejected because they would add extra classes or inheritance structures that the current requirements do not justify.

This gives the project a design that is cohesive, extensible, and testable without becoming over-engineered for Sprint 2.
