import unittest

from game.card import Card


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


if __name__ == '__main__':
    unittest.main()
