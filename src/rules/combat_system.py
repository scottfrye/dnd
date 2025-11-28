"""Combat system module for AD&D 1E.

Provides basic attack resolution hooks using THAC0 (To Hit Armor Class 0)
mechanics. THAC0 represents the attack roll needed to hit a target with AC 0.

In AD&D 1E:
- Lower AC is better (0 is good, negative is excellent)
- To determine if an attack hits: attack roll + modifiers >= THAC0 - target_AC
- Alternatively: attack roll >= THAC0 - target_AC - modifiers

This module provides:
- THAC0 calculation based on class and level
- Attack resolution given attacker/defender stats
- Hit/miss determination with modifier support
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from src.utils.dice import DiceRoller


# Base THAC0 values by level for different class groups (AD&D 1E PHB)
# Fighter group (Fighter, Paladin, Ranger): improves every level
# Cleric group (Cleric, Druid): improves every 3 levels
# Thief group (Thief, Assassin, Monk): improves every 4 levels
# Magic-User group (Magic-User, Illusionist): improves every 5 levels
_FIGHTER_THAC0: dict[int, int] = {
    0: 21,  # Level 0 (normal man)
    1: 20,
    2: 19,
    3: 18,
    4: 17,
    5: 16,
    6: 15,
    7: 14,
    8: 13,
    9: 12,
    10: 11,
    11: 10,
    12: 9,
    13: 8,
    14: 7,
    15: 6,
    16: 5,
    17: 4,
    18: 3,
    19: 2,
    20: 1,
}

_CLERIC_THAC0: dict[int, int] = {
    1: 20,
    2: 20,
    3: 20,
    4: 18,
    5: 18,
    6: 18,
    7: 16,
    8: 16,
    9: 16,
    10: 14,
    11: 14,
    12: 14,
    13: 12,
    14: 12,
    15: 12,
    16: 10,
    17: 10,
    18: 10,
    19: 8,
    20: 8,
}

_THIEF_THAC0: dict[int, int] = {
    1: 21,
    2: 21,
    3: 21,
    4: 21,
    5: 19,
    6: 19,
    7: 19,
    8: 19,
    9: 16,
    10: 16,
    11: 16,
    12: 16,
    13: 14,
    14: 14,
    15: 14,
    16: 14,
    17: 12,
    18: 12,
    19: 12,
    20: 12,
}

_MAGIC_USER_THAC0: dict[int, int] = {
    1: 21,
    2: 21,
    3: 21,
    4: 21,
    5: 21,
    6: 19,
    7: 19,
    8: 19,
    9: 19,
    10: 19,
    11: 16,
    12: 16,
    13: 16,
    14: 16,
    15: 16,
    16: 13,
    17: 13,
    18: 13,
    19: 13,
    20: 13,
}


@dataclass
class CombatStats:
    """Combat-related statistics for an attacker or defender.

    Attributes:
        thac0: To Hit Armor Class 0 value (for attackers)
        armor_class: Armor Class value (for defenders, lower is better)
        hit_modifier: Bonus or penalty to attack rolls
        damage_modifier: Bonus or penalty to damage rolls
    """

    thac0: int = 20
    armor_class: int = 10
    hit_modifier: int = 0
    damage_modifier: int = 0




@dataclass
class AttackResult:
    """Result of an attack resolution.

    Attributes:
        hit: Whether the attack was successful
        roll: The raw d20 roll value
        total_attack: The total attack value (roll + modifiers)
        target_number: The number needed to hit
        critical_hit: Whether a natural 20 was rolled
        critical_miss: Whether a natural 1 was rolled
    """

    hit: bool
    roll: int
    total_attack: int
    target_number: int
    critical_hit: bool = False
    critical_miss: bool = False


def get_thac0(
    level: int, class_group: str = "fighter"
) -> int:
    """Get the THAC0 value for a given level and class group.

    Args:
        level: Character level (1-20, or 0 for normal men)
        class_group: One of "fighter", "cleric", "thief", "magic_user"

    Returns:
        The THAC0 value for the given level and class.

    Raises:
        ValueError: If level is invalid or class_group is unknown.
    """
    if level < 0:
        raise ValueError(f"Level must be non-negative, got {level}")

    # Cap level at 20 for lookup
    lookup_level = min(level, 20)

    # Get the appropriate THAC0 table
    thac0_tables = {
        "fighter": _FIGHTER_THAC0,
        "cleric": _CLERIC_THAC0,
        "thief": _THIEF_THAC0,
        "magic_user": _MAGIC_USER_THAC0,
    }

    if class_group not in thac0_tables:
        raise ValueError(
            f"Unknown class_group: {class_group}. "
            f"Valid options: {list(thac0_tables.keys())}"
        )

    thac0_table = thac0_tables[class_group]

    # Handle level 0 (only fighter table has it)
    if lookup_level == 0:
        if class_group == "fighter":
            return thac0_table[0]
        # Other classes don't have level 0, use level 1
        return thac0_table[1]

    return thac0_table[lookup_level]


def calculate_target_number(thac0: int, target_ac: int) -> int:
    """Calculate the attack roll needed to hit a target.

    In AD&D 1E, the formula is: need to roll >= THAC0 - AC

    Args:
        thac0: The attacker's THAC0 value
        target_ac: The defender's Armor Class

    Returns:
        The minimum d20 roll needed to hit (before modifiers).
    """
    return thac0 - target_ac


def resolve_attack(
    attacker: CombatStats,
    defender: CombatStats,
    roll: Optional[int] = None,
    roller: Optional[DiceRoller] = None,
) -> AttackResult:
    """Resolve an attack between an attacker and defender.

    Determines if an attack hits based on THAC0 mechanics.
    A natural 20 always hits, a natural 1 always misses.

    Args:
        attacker: Combat stats for the attacking entity
        defender: Combat stats for the defending entity
        roll: Optional pre-determined d20 roll (for testing).
              If not provided, a roll will be made.
        roller: Optional DiceRoller for deterministic rolling.
                If not provided, uses random rolling.

    Returns:
        An AttackResult containing hit/miss and roll details.
    """
    # Make the attack roll
    if roll is not None:
        actual_roll = roll
    elif roller is not None:
        actual_roll = roller.roll("1d20")
    else:
        # Use a default random roller
        default_roller = DiceRoller()
        actual_roll = default_roller.roll("1d20")

    # Calculate the target number needed
    target_number = calculate_target_number(attacker.thac0, defender.armor_class)

    # Calculate total attack value
    total_attack = actual_roll + attacker.hit_modifier

    # Determine hit/miss
    # Natural 20 always hits, natural 1 always misses
    critical_hit = actual_roll == 20
    critical_miss = actual_roll == 1

    if critical_miss:
        hit = False
    elif critical_hit:
        hit = True
    else:
        hit = total_attack >= target_number

    return AttackResult(
        hit=hit,
        roll=actual_roll,
        total_attack=total_attack,
        target_number=target_number,
        critical_hit=critical_hit,
        critical_miss=critical_miss,
    )


def resolve_attack_simple(
    attacker_thac0: int,
    defender_ac: int,
    hit_modifier: int = 0,
    roll: Optional[int] = None,
    roller: Optional[DiceRoller] = None,
) -> Tuple[bool, int]:
    """Simplified attack resolution with basic parameters.

    A convenience function for quick attack resolution without
    creating CombatStats objects.

    Args:
        attacker_thac0: The attacker's THAC0 value
        defender_ac: The defender's Armor Class
        hit_modifier: Bonus or penalty to the attack roll
        roll: Optional pre-determined d20 roll (for testing)
        roller: Optional DiceRoller for deterministic rolling

    Returns:
        A tuple of (hit: bool, roll: int) indicating success and the roll value.
    """
    attacker = CombatStats(thac0=attacker_thac0, hit_modifier=hit_modifier)
    defender = CombatStats(armor_class=defender_ac)

    result = resolve_attack(attacker, defender, roll=roll, roller=roller)
    return (result.hit, result.roll)
