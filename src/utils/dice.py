"""Dice rolling module for AD&D 1E.

Provides deterministic and random dice roll helpers supporting standard
dice notation (e.g., 1d6, 3d8+2, 2d10-1).
"""

import random
import re
from typing import Optional

# Pattern to match dice notation: [count]d<sides>[+/-modifier]
# Examples: d6, 1d6, 3d8+2, 2d10-1, d20+5
DICE_PATTERN = re.compile(r"^(\d*)d(\d+)([+-]\d+)?$", re.IGNORECASE)


class DiceRoller:
    """A dice roller with optional seeding for deterministic results."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize the dice roller.

        Args:
            seed: Optional seed for the random number generator.
                  If provided, rolls will be deterministic.
        """
        self._rng = random.Random(seed)

    def seed(self, seed: int) -> None:
        """Set the seed for the random number generator.

        Args:
            seed: The seed value to use.
        """
        self._rng.seed(seed)

    def roll_die(self, sides: int) -> int:
        """Roll a single die with the given number of sides.

        Args:
            sides: The number of sides on the die (must be >= 1).

        Returns:
            A random integer from 1 to sides (inclusive).

        Raises:
            ValueError: If sides is less than 1.
        """
        if sides < 1:
            raise ValueError(f"Die must have at least 1 side, got {sides}")
        return self._rng.randint(1, sides)

    def roll(self, notation: str) -> int:
        """Roll dice using standard dice notation.

        Supports notation like:
        - "d6" or "1d6": Roll one 6-sided die
        - "3d8": Roll three 8-sided dice and sum
        - "2d10+5": Roll two 10-sided dice and add 5
        - "1d20-2": Roll one 20-sided die and subtract 2
        - "0d6": Returns just the modifier (0 if none)

        Args:
            notation: Dice notation string (e.g., "3d6+2").

        Returns:
            The total result of the roll.

        Raises:
            ValueError: If the notation is invalid or sides < 1.
        """
        match = DICE_PATTERN.match(notation.strip())
        if not match:
            raise ValueError(f"Invalid dice notation: {notation}")

        count_str, sides_str, modifier_str = match.groups()

        # Parse count (default to 1 if empty)
        count = int(count_str) if count_str else 1

        # Parse sides
        sides = int(sides_str)
        if sides < 1:
            raise ValueError(f"Die must have at least 1 side, got {sides}")

        # Parse modifier (default to 0 if not present)
        modifier = int(modifier_str) if modifier_str else 0

        # Roll the dice
        total = sum(self.roll_die(sides) for _ in range(count))

        return total + modifier


# Default global roller for convenience
_default_roller = DiceRoller()


def roll(notation: str) -> int:
    """Roll dice using standard dice notation with the global roller.

    Supports notation like:
    - "d6" or "1d6": Roll one 6-sided die
    - "3d8": Roll three 8-sided dice and sum
    - "2d10+5": Roll two 10-sided dice and add 5
    - "1d20-2": Roll one 20-sided die and subtract 2
    - "0d6": Returns just the modifier (0 if none)

    Args:
        notation: Dice notation string (e.g., "3d6+2").

    Returns:
        The total result of the roll.

    Raises:
        ValueError: If the notation is invalid.
    """
    return _default_roller.roll(notation)


def seed(seed_value: int) -> None:
    """Set the seed for the global dice roller.

    Args:
        seed_value: The seed value to use for deterministic rolls.
    """
    _default_roller.seed(seed_value)
