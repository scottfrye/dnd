"""Unit tests for the dice rolling module.

These tests verify that the dice module correctly:
- Parses standard dice notation (e.g., 1d6, 3d8+2)
- Supports seeding for deterministic results
- Handles edge cases (0 dice, negative modifiers)
"""

import pytest

from src.utils.dice import DiceRoller, roll, seed


class TestDiceRoller:
    """Tests for the DiceRoller class."""

    def test_roll_single_die(self):
        """Test rolling a single die with seeded roller."""
        roller = DiceRoller(seed=42)
        result = roller.roll("1d6")
        assert 1 <= result <= 6

    def test_seeded_rolls_are_deterministic(self):
        """Test that seeded rollers produce deterministic results."""
        roller1 = DiceRoller(seed=42)
        roller2 = DiceRoller(seed=42)

        results1 = [roller1.roll("1d20") for _ in range(10)]
        results2 = [roller2.roll("1d20") for _ in range(10)]

        assert results1 == results2

    def test_different_seeds_produce_different_results(self):
        """Test that different seeds produce different results."""
        roller1 = DiceRoller(seed=42)
        roller2 = DiceRoller(seed=123)

        results1 = [roller1.roll("1d20") for _ in range(10)]
        results2 = [roller2.roll("1d20") for _ in range(10)]

        # Very unlikely to be equal with different seeds
        assert results1 != results2

    def test_reseed_roller(self):
        """Test that reseeding the roller produces deterministic results."""
        roller = DiceRoller(seed=42)
        first_roll = roller.roll("1d20")

        roller.seed(42)
        second_roll = roller.roll("1d20")

        assert first_roll == second_roll

    def test_roll_multiple_dice(self):
        """Test rolling multiple dice."""
        roller = DiceRoller(seed=42)
        result = roller.roll("3d6")
        # 3d6 should be between 3 and 18
        assert 3 <= result <= 18

    def test_roll_with_positive_modifier(self):
        """Test rolling dice with positive modifier."""
        roller = DiceRoller(seed=42)
        result = roller.roll("1d6+5")
        # 1d6+5 should be between 6 and 11
        assert 6 <= result <= 11

    def test_roll_with_negative_modifier(self):
        """Test rolling dice with negative modifier."""
        roller = DiceRoller(seed=42)
        result = roller.roll("1d6-2")
        # 1d6-2 should be between -1 and 4
        assert -1 <= result <= 4

    def test_roll_zero_dice(self):
        """Test rolling zero dice returns just the modifier."""
        roller = DiceRoller(seed=42)

        # 0d6 with no modifier should be 0
        result = roller.roll("0d6")
        assert result == 0

        # 0d6+5 should be 5
        result_with_modifier = roller.roll("0d6+5")
        assert result_with_modifier == 5

        # 0d6-3 should be -3
        result_with_negative = roller.roll("0d6-3")
        assert result_with_negative == -3

    def test_roll_without_count(self):
        """Test rolling dice without explicit count (d6 = 1d6)."""
        roller = DiceRoller(seed=42)
        result = roller.roll("d6")
        assert 1 <= result <= 6

    def test_roll_case_insensitive(self):
        """Test that dice notation is case-insensitive."""
        roller = DiceRoller(seed=42)
        lower_result = roller.roll("1d6")

        roller.seed(42)
        upper_result = roller.roll("1D6")

        assert lower_result == upper_result

    def test_roll_with_whitespace(self):
        """Test that whitespace is handled correctly."""
        roller = DiceRoller(seed=42)
        result = roller.roll("  1d6  ")
        assert 1 <= result <= 6

    def test_invalid_notation_raises_error(self):
        """Test that invalid notation raises ValueError."""
        roller = DiceRoller(seed=42)

        with pytest.raises(ValueError):
            roller.roll("invalid")

        with pytest.raises(ValueError):
            roller.roll("d")

        with pytest.raises(ValueError):
            roller.roll("1d")

        with pytest.raises(ValueError):
            roller.roll("abc1d6")

    def test_zero_sides_raises_error(self):
        """Test that zero-sided dice raise ValueError."""
        roller = DiceRoller(seed=42)

        with pytest.raises(ValueError):
            roller.roll("1d0")

    def test_roll_die_with_invalid_sides_raises_error(self):
        """Test that roll_die with invalid sides raises ValueError."""
        roller = DiceRoller(seed=42)

        with pytest.raises(ValueError):
            roller.roll_die(0)

        with pytest.raises(ValueError):
            roller.roll_die(-1)

    def test_common_dice_types(self):
        """Test common AD&D dice types."""
        roller = DiceRoller(seed=42)

        # d4
        result = roller.roll("1d4")
        assert 1 <= result <= 4

        # d6
        result = roller.roll("1d6")
        assert 1 <= result <= 6

        # d8
        result = roller.roll("1d8")
        assert 1 <= result <= 8

        # d10
        result = roller.roll("1d10")
        assert 1 <= result <= 10

        # d12
        result = roller.roll("1d12")
        assert 1 <= result <= 12

        # d20
        result = roller.roll("1d20")
        assert 1 <= result <= 20

        # d100
        result = roller.roll("1d100")
        assert 1 <= result <= 100


class TestGlobalDiceFunctions:
    """Tests for the global dice functions."""

    def test_global_roll_function(self):
        """Test the global roll function."""
        seed(42)
        result = roll("1d20")
        assert 1 <= result <= 20

    def test_global_seed_function(self):
        """Test the global seed function produces deterministic results."""
        seed(42)
        first_result = roll("1d20")

        seed(42)
        second_result = roll("1d20")

        assert first_result == second_result

    def test_global_roll_with_modifier(self):
        """Test the global roll function with modifiers."""
        seed(42)
        result = roll("2d6+3")
        # 2d6+3 should be between 5 and 15
        assert 5 <= result <= 15
