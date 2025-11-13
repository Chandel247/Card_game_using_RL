import unittest

from game.card import Card, make_monster_pool, make_effect_pool


class TestCard(unittest.TestCase):

    def test_monster_card_attributes(self):
        c = Card(id=1, name="Goblin", card_type="monster", atk=3, defense=1, hp=2)
        self.assertEqual(c.name, "Goblin")
        self.assertEqual(c.card_type, "monster")
        self.assertEqual(c.atk, 3)
        self.assertEqual(c.defense, 1)
        self.assertEqual(c.hp, 2)
        self.assertEqual(c.max_hp, 2)

    def test_take_damage_more_than_defense(self):
        c = Card(id=2, name="Ogre", card_type="monster", atk=5, defense=2, hp=5)
        actual = c.take_damage(4)  # 4 >= defense(2) -> actual = 2
        self.assertEqual(actual, 2)
        self.assertEqual(c.hp, 3)

    def test_take_damage_less_than_defense(self):
        c = Card(id=3, name="Turtle", card_type="monster", atk=1, defense=3, hp=4)
        actual = c.take_damage(2)  # 2 < defense(3) -> 0
        self.assertEqual(actual, 0)
        self.assertEqual(c.hp, 4)

    def test_take_damage_equal_to_defense(self):
        # When damage equals defense, actual damage should be 0 and hp unchanged
        c = Card(id=4, name="Shell", card_type="monster", atk=1, defense=3, hp=4)
        actual = c.take_damage(3)  # 3 == defense(3) -> actual = 0
        self.assertEqual(actual, 0)
        self.assertEqual(c.hp, 4)

    def test_is_alive_false_when_hp_zero(self):
        c = Card(id=5, name="Worm", card_type="monster", atk=1, defense=0, hp=1)
        dmg = c.take_damage(5)
        # take_damage returns actual damage applied (min(hp, amount-defense)) -> 1
        self.assertEqual(dmg, 1)
        self.assertFalse(c.is_alive())
        self.assertEqual(c.hp, 0)

    def test_non_monster_card_fields(self):
        c = Card(id=6, name="Heal", card_type="spell", effect_type='heal', duration=1, cost=0)
        # Non-monster should have effect-related fields
        self.assertEqual(c.card_type, 'spell')
        self.assertEqual(getattr(c, 'effect_type'), 'heal')
        self.assertEqual(getattr(c, 'duration'), 1)
        self.assertEqual(getattr(c, 'cost'), 0)
        # Non-monster should not have monster-only attributes like 'atk'
        self.assertFalse(hasattr(c, 'atk'))
        # Non-monster cards do not define 'hp' or 'defense' attributes
        self.assertFalse(hasattr(c, 'hp'))
        self.assertFalse(hasattr(c, 'defense'))


class TestMonsterPool(unittest.TestCase):

    def test_make_monster_pool_loads_cards(self):
        """Test that make_monster_pool returns a non-empty list of Card objects."""
        monsters = make_monster_pool()
        self.assertIsInstance(monsters, list)
        self.assertGreater(len(monsters), 0)

    def test_make_monster_pool_cards_are_monsters(self):
        """Test that all loaded monsters have card_type 'monster'."""
        monsters = make_monster_pool()
        for monster in monsters:
            self.assertIsInstance(monster, Card)
            self.assertEqual(monster.card_type, "monster")

    def test_make_monster_pool_has_required_fields(self):
        """Test that loaded monsters have required attributes."""
        monsters = make_monster_pool()
        for monster in monsters:
            self.assertTrue(hasattr(monster, 'id'))
            self.assertTrue(hasattr(monster, 'name'))
            self.assertTrue(hasattr(monster, 'hp'))
            self.assertTrue(hasattr(monster, 'atk'))
            self.assertTrue(hasattr(monster, 'defense'))
            self.assertIsInstance(monster.id, int)
            self.assertIsInstance(monster.name, str)
            self.assertGreaterEqual(monster.hp, 0)
            self.assertGreaterEqual(monster.atk, 0)
            self.assertGreaterEqual(monster.defense, 0)

    def test_make_monster_pool_first_monster(self):
        """Test the first monster card (Goblin Scout) is loaded correctly."""
        monsters = make_monster_pool()
        first = monsters[0]
        self.assertEqual(first.id, 1)
        self.assertEqual(first.name, "Goblin Scout")
        self.assertEqual(first.atk, 4)
        self.assertEqual(first.defense, 1)
        self.assertEqual(first.hp, 8)


class TestEffectPool(unittest.TestCase):

    def test_make_effect_pool_loads_cards(self):
        """Test that make_effect_pool returns a non-empty list of Card objects."""
        effects = make_effect_pool()
        self.assertIsInstance(effects, list)
        self.assertGreater(len(effects), 0)

    def test_make_effect_pool_cards_are_spells(self):
        """Test that all loaded effects have card_type 'spell'."""
        effects = make_effect_pool()
        for effect in effects:
            self.assertIsInstance(effect, Card)
            self.assertEqual(effect.card_type, "spell")

    def test_make_effect_pool_has_required_fields(self):
        """Test that loaded effects have required attributes."""
        effects = make_effect_pool()
        for effect in effects:
            self.assertTrue(hasattr(effect, 'id'))
            self.assertTrue(hasattr(effect, 'name'))
            self.assertTrue(hasattr(effect, 'effect_type'))
            self.assertTrue(hasattr(effect, 'cost'))
            self.assertTrue(hasattr(effect, 'duration'))
            self.assertIsInstance(effect.id, int)
            self.assertIsInstance(effect.name, str)
            self.assertIsInstance(effect.effect_type, str)
            self.assertGreaterEqual(effect.cost, 0)
            self.assertGreaterEqual(effect.duration, -1)

    def test_make_effect_pool_first_effect(self):
        """Test the first effect card (Minor Heal) is loaded correctly."""
        effects = make_effect_pool()
        first = effects[0]
        self.assertEqual(first.id, 21)
        self.assertEqual(first.name, "Minor Heal")
        self.assertEqual(first.effect_type, "heal")
        self.assertEqual(first.cost, 0)
        self.assertEqual(first.duration, 1)

    def test_make_effect_pool_effects_do_not_have_monster_fields(self):
        """Test that effect cards do not have monster-specific fields."""
        effects = make_effect_pool()
        for effect in effects:
            self.assertFalse(hasattr(effect, 'atk'))
            self.assertFalse(hasattr(effect, 'defense'))
            self.assertFalse(hasattr(effect, 'hp'))


if __name__ == '__main__':
    unittest.main()
