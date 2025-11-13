import unittest

from game.card import Card
from game.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures for Player tests."""
        self.deck = [
            Card(id=1, name="Goblin", card_type="monster", atk=3, defense=1, hp=2),
            Card(id=2, name="Ogre", card_type="monster", atk=5, defense=2, hp=5),
            Card(id=3, name="Knight", card_type="monster", atk=4, defense=4, hp=6),
        ]
        self.player = Player(self.deck.copy())

    def test_player_initialization(self):
        """Test Player initializes with correct default values."""
        self.assertEqual(self.player.hp, 30)
        self.assertEqual(self.player.max_hp, 30)
        self.assertEqual(self.player.defense, 10)
        self.assertEqual(self.player.mana, 3)
        self.assertEqual(len(self.player.deck), 3)
        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(len(self.player.bench), 0)
        self.assertIsNone(self.player.playing_card)

    def test_get_alive_monsters_with_no_playing_card(self):
        """Test get_alive_monsters when no card is playing."""
        alive = self.player.get_alive_monsters()
        self.assertEqual(alive, [])

    def test_get_alive_monsters_with_alive_playing_card(self):
        """Test get_alive_monsters returns playing card when alive."""
        card = Card(id=1, name="Goblin", card_type="monster", atk=3, defense=1, hp=2)
        self.player.playing_card = card
        alive = self.player.get_alive_monsters()
        self.assertEqual(len(alive), 1)
        self.assertEqual(alive[0], card)

    def test_get_alive_monsters_with_dead_playing_card(self):
        """Test get_alive_monsters excludes dead playing card."""
        card = Card(id=1, name="Goblin", card_type="monster", atk=3, defense=1, hp=1)
        card.take_damage(5)  # Kill the card
        self.player.playing_card = card
        alive = self.player.get_alive_monsters()
        self.assertEqual(alive, [])

    def test_get_alive_monsters_with_bench(self):
        """Test get_alive_monsters includes alive bench cards."""
        card1 = Card(id=1, name="Goblin", card_type="monster", atk=3, defense=1, hp=2)
        card2 = Card(id=2, name="Ogre", card_type="monster", atk=5, defense=2, hp=5)
        self.player.playing_card = card1
        self.player.bench = [card2]
        alive = self.player.get_alive_monsters()
        self.assertEqual(len(alive), 2)
        self.assertIn(card1, alive)
        self.assertIn(card2, alive)

    def test_get_alive_monsters_mixed_alive_and_dead(self):
        """Test get_alive_monsters returns only alive cards from playing and bench."""
        card1 = Card(id=1, name="Goblin", card_type="monster", atk=3, defense=1, hp=2)  # alive
        card2 = Card(id=2, name="Ogre", card_type="monster", atk=5, defense=2, hp=5)  # alive
        card3 = Card(id=3, name="Knight", card_type="monster", atk=4, defense=4, hp=1)  # will be dead
        card3.take_damage(10)  # Kill card3
        self.player.playing_card = card1
        self.player.bench = [card2, card3]
        alive = self.player.get_alive_monsters()
        self.assertEqual(len(alive), 2)
        self.assertIn(card1, alive)
        self.assertIn(card2, alive)
        self.assertNotIn(card3, alive)

    def test_player_take_damage_more_than_defense(self):
        """Test Player take_damage when damage exceeds defense."""
        dmg = self.player.take_damage(15)  # 15 > defense(10)
        self.assertEqual(dmg, 5)  # actual = min(30, 15-10)
        self.assertEqual(self.player.hp, 25)

    def test_player_take_damage_less_than_defense(self):
        """Test Player take_damage when damage is less than defense."""
        dmg = self.player.take_damage(5)  # 5 < defense(10)
        self.assertEqual(dmg, 0)
        self.assertEqual(self.player.hp, 30)


if __name__ == '__main__':
    unittest.main()
