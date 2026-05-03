import sys
import unittest
from collections import Counter
from pathlib import Path


SPRINT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SPRINT_DIR))

from controllers.game_controller import GameController
from controllers.game_setup import GameSetup as ControllerGameSetup
from models.cards import ColouredCarCard, LocomotiveCard
from models.core import CardColor
from models.decks import DestinationTicketDeck, FaceUpPool, TrainCarCardDeck
from models.map_definition import MapDefinition
from models.player import Player
from models.setup import GameSetup
from models.tickets import DestinationTicket
from models.turns import TurnManager


class LondonRulesTest(unittest.TestCase):
    def make_small_map(self):
        map_definition = MapDefinition("Test London", 2, 4, 17)

        for city in ["A", "B", "C", "D"]:
            map_definition.add_city(city)

        map_definition.add_ticket("A", "B", 1)
        map_definition.add_ticket("B", "C", 2)
        map_definition.add_ticket("C", "D", 3)
        map_definition.add_ticket("D", "A", 4)

        return map_definition

    def test_transport_deck_uses_london_card_counts(self):
        deck = GameSetup().create_train_deck()
        cards = deck.deck + deck.discard
        counts = Counter()

        for card in cards:
            counts[card.colour] += 1

        self.assertEqual(44, len(cards))
        self.assertEqual(8, counts[CardColor.LOCOMOTIVE])
        self.assertEqual(6, counts[CardColor.BLUE])
        self.assertEqual(6, counts[CardColor.GREEN])
        self.assertEqual(6, counts[CardColor.BLACK])
        self.assertEqual(6, counts[CardColor.PINK])
        self.assertEqual(6, counts[CardColor.YELLOW])
        self.assertEqual(6, counts[CardColor.ORANGE])
        self.assertEqual(0, counts[CardColor.RED])
        self.assertEqual(0, counts[CardColor.WHITE])

    def test_setup_deals_two_transport_cards_and_two_tickets(self):
        turn_manager, train_deck, ticket_deck, face_up_pool = GameSetup().set_up_game(
            self.make_small_map(),
            ["Alice", "Bob"]
        )

        for player in turn_manager.players:
            self.assertEqual(2, len(player.train_cards))
            self.assertEqual(2, len(player.destination_tickets))

    def test_controller_setup_uses_london_setup_rules(self):
        turn_manager = ControllerGameSetup().set_up_game(
            self.make_small_map(),
            ["Alice", "Bob"]
        )

        for player in turn_manager.players:
            self.assertEqual(2, len(player.train_cards))
            self.assertEqual(2, len(player.destination_tickets))

    def test_london_map_contains_district_data(self):
        london = MapDefinition.create_london_map()

        self.assertIn("Buckingham Palace", london.cities)

        district_found = False

        for district in london.districts:
            if district["name"] == "District 2":
                if "Buckingham Palace" in district["locations"]:
                    if district["points"] == 2:
                        district_found = True

        self.assertTrue(district_found)

    def test_face_up_pool_discards_and_replaces_three_buses(self):
        pool = FaceUpPool()
        pool.face_up_cards = [
            LocomotiveCard(),
            LocomotiveCard(),
            LocomotiveCard(),
            ColouredCarCard(CardColor.BLUE),
            ColouredCarCard(CardColor.GREEN),
        ]

        deck = TrainCarCardDeck([])
        deck.deck = [
            ColouredCarCard(CardColor.BLACK),
            ColouredCarCard(CardColor.PINK),
            ColouredCarCard(CardColor.YELLOW),
            ColouredCarCard(CardColor.ORANGE),
            ColouredCarCard(CardColor.BLUE),
        ]

        pool.replace_if_three_buses(deck)

        bus_count = 0

        for card in pool.face_up_cards:
            if card.colour == CardColor.LOCOMOTIVE:
                bus_count += 1

        self.assertEqual(5, len(pool.face_up_cards))
        self.assertEqual(5, len(deck.discard))
        self.assertLess(bus_count, 3)

    def test_face_up_bus_as_first_transport_card_ends_turn(self):
        player = Player("Alice")
        pool = FaceUpPool()
        pool.face_up_cards = [
            LocomotiveCard(),
            ColouredCarCard(CardColor.BLUE),
            ColouredCarCard(CardColor.GREEN),
            ColouredCarCard(CardColor.BLACK),
            ColouredCarCard(CardColor.YELLOW),
        ]

        deck = TrainCarCardDeck([])
        deck.deck = [ColouredCarCard(CardColor.ORANGE)]

        turn_manager = TurnManager(
            [player, Player("Bob")],
            object(),
            deck,
            DestinationTicketDeck([]),
            pool
        )

        ok, message = turn_manager.draw_train_card(False, 0)

        self.assertTrue(ok)
        self.assertTrue(turn_manager.turn_ended())
        self.assertEqual(1, len(player.train_cards))
        self.assertEqual(CardColor.LOCOMOTIVE, player.train_cards[0].colour)
        self.assertEqual(5, len(pool.face_up_cards))

    def test_face_up_bus_cannot_be_second_transport_card(self):
        player = Player("Alice")
        pool = FaceUpPool()
        pool.face_up_cards = [
            LocomotiveCard(),
            ColouredCarCard(CardColor.BLUE),
            ColouredCarCard(CardColor.GREEN),
            ColouredCarCard(CardColor.BLACK),
            ColouredCarCard(CardColor.YELLOW),
        ]

        deck = TrainCarCardDeck([])
        deck.deck = [ColouredCarCard(CardColor.ORANGE)]

        turn_manager = TurnManager(
            [player, Player("Bob")],
            object(),
            deck,
            DestinationTicketDeck([]),
            pool
        )

        ok, message = turn_manager.draw_train_card(True)
        self.assertTrue(ok)

        ok, message = turn_manager.draw_train_card(False, 0)

        self.assertFalse(ok)
        self.assertEqual(1, len(player.train_cards))

    def test_draw_destination_tickets_draws_two_and_keeps_one(self):
        player = Player("Alice")
        tickets = [
            DestinationTicket("A", "B", 1),
            DestinationTicket("B", "C", 2),
            DestinationTicket("C", "D", 3),
        ]

        ticket_deck = DestinationTicketDeck(tickets)
        turn_manager = TurnManager(
            [player, Player("Bob")],
            object(),
            TrainCarCardDeck([]),
            ticket_deck,
            FaceUpPool()
        )

        drawn, message = turn_manager.draw_destination_tickets()
        self.assertEqual(2, len(drawn))

        ok, message = turn_manager.keep_destination_tickets([drawn[0]], [drawn[1]])

        self.assertTrue(ok)
        self.assertTrue(turn_manager.turn_ended())
        self.assertEqual(1, len(player.destination_tickets))
        self.assertEqual(drawn[0], player.destination_tickets[0])
        self.assertIn(drawn[1], ticket_deck.tickets)

    def test_game_controller_draw_train_card_delegates_to_turn_manager(self):
        player = Player("Alice")
        pool = FaceUpPool()
        pool.face_up_cards = [
            ColouredCarCard(CardColor.BLUE),
            ColouredCarCard(CardColor.GREEN),
            ColouredCarCard(CardColor.BLACK),
            ColouredCarCard(CardColor.YELLOW),
            ColouredCarCard(CardColor.ORANGE),
        ]

        deck = TrainCarCardDeck([])
        deck.deck = [ColouredCarCard(CardColor.PINK)]

        turn_manager = TurnManager(
            [player, Player("Bob")],
            object(),
            deck,
            DestinationTicketDeck([]),
            pool
        )
        controller = GameController(turn_manager)

        ok, message = controller.draw_train_card(False, 0)

        self.assertTrue(ok)
        self.assertEqual(1, len(player.train_cards))


if __name__ == "__main__":
    unittest.main()
