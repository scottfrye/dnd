import unittest
from unittest.mock import MagicMock
from src.dice import Dice


class TestDice(unittest.TestCase):
    def test_die_6(self):
        d = Dice()
        value = d.roll(1, 6)
        print(value)
        self.assertLessEqual(value, 6)

    def test_mock_dice(self):
        d = Dice()
        d.roll = MagicMock(return_value=1)
        value = d.roll()
        print(value)
        self.assertEqual(value, 1)