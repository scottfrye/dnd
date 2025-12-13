"""Saving throws module for AD&D 1E.

Implements the five saving throw categories from Advanced Dungeons & Dragons
1st Edition: Paralyzation/Poison/Death Magic, Petrification/Polymorph,
Rod/Staff/Wand, Breath Weapon, and Spell.

Includes saving throw tables for all character classes, racial bonuses,
and a resolution function for making saving throws.

Public API:
    - SavingThrowCategory: Enum for the five saving throw types
    - get_saving_throw: Get base saving throw value for class/level/category
    - get_racial_saving_throw_bonus: Get racial bonus to saving throws
    - make_saving_throw: Resolve a saving throw with all modifiers

Example Usage:
    >>> from src.rules.saving_throws import (
    ...     SavingThrowCategory,
    ...     get_saving_throw,
    ...     make_saving_throw
    ... )
    >>> # Get base saving throw for a 5th level fighter vs poison
    >>> base_save = get_saving_throw(
    ...     "fighter", 5, SavingThrowCategory.PARALYZATION_POISON_DEATH
    ... )
    >>> print(f"Base save: {base_save}")
    Base save: 12
    >>> # Make a saving throw with modifiers
    >>> result = make_saving_throw(
    ...     class_name="fighter",
    ...     level=5,
    ...     category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
    ...     constitution=16,
    ...     race="dwarf",
    ...     roll=15
    ... )
    >>> print(f"Success: {result.success}")
    Success: True

References:
    - AD&D 1E Player's Handbook, Saving Throw Tables
    - AD&D 1E Player's Handbook, Racial Abilities
    - AD&D 1E Dungeon Master's Guide, Saving Throws
"""

from dataclasses import dataclass
from enum import Enum

from src.utils.dice import DiceRoller


class SavingThrowCategory(Enum):
    """Five saving throw categories from AD&D 1E.

    Each category represents different types of threats that characters
    must save against. Lower numbers are better (easier to save).

    Attributes:
        PARALYZATION_POISON_DEATH: Save vs paralysis, poison, death magic
        PETRIFICATION_POLYMORPH: Save vs petrification and polymorph
        ROD_STAFF_WAND: Save vs magical rods, staves, and wands
        BREATH_WEAPON: Save vs dragon breath and similar attacks
        SPELL: Save vs spells not covered by other categories
    """

    PARALYZATION_POISON_DEATH = "paralyzation_poison_death"
    PETRIFICATION_POLYMORPH = "petrification_polymorph"
    ROD_STAFF_WAND = "rod_staff_wand"
    BREATH_WEAPON = "breath_weapon"
    SPELL = "spell"


# Saving throw tables by class (AD&D 1E Player's Handbook)
# Format: {level: {category: target_number}}
# Target number is what must be rolled on d20 to succeed

_FIGHTER_SAVES = {
    1: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 14,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 15,
        SavingThrowCategory.ROD_STAFF_WAND: 16,
        SavingThrowCategory.BREATH_WEAPON: 17,
        SavingThrowCategory.SPELL: 17,
    },
    2: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 14,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 15,
        SavingThrowCategory.ROD_STAFF_WAND: 16,
        SavingThrowCategory.BREATH_WEAPON: 17,
        SavingThrowCategory.SPELL: 17,
    },
    3: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 14,
        SavingThrowCategory.ROD_STAFF_WAND: 15,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 16,
    },
    4: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 14,
        SavingThrowCategory.ROD_STAFF_WAND: 15,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 16,
    },
    5: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 12,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 15,
    },
    6: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 12,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 15,
    },
    7: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 13,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 14,
    },
    8: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 13,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 14,
    },
    9: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 13,
    },
    10: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 13,
    },
    11: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 12,
    },
    12: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 12,
    },
    13: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 8,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 11,
    },
    14: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 8,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 11,
    },
    15: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 7,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 10,
        SavingThrowCategory.SPELL: 10,
    },
    16: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 7,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 10,
        SavingThrowCategory.SPELL: 10,
    },
    17: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 6,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 9,
        SavingThrowCategory.SPELL: 9,
    },
    18: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 6,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 9,
        SavingThrowCategory.SPELL: 9,
    },
    19: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 5,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 6,
        SavingThrowCategory.ROD_STAFF_WAND: 7,
        SavingThrowCategory.BREATH_WEAPON: 8,
        SavingThrowCategory.SPELL: 8,
    },
    20: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 5,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 6,
        SavingThrowCategory.ROD_STAFF_WAND: 7,
        SavingThrowCategory.BREATH_WEAPON: 8,
        SavingThrowCategory.SPELL: 8,
    },
}

_CLERIC_SAVES = {
    1: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 15,
    },
    2: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 15,
    },
    3: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 15,
    },
    4: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 13,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 14,
    },
    5: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 13,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 14,
    },
    6: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 13,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 14,
    },
    7: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 8,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 13,
    },
    8: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 8,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 13,
    },
    9: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 8,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 13,
    },
    10: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 7,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 12,
    },
    11: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 7,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 12,
    },
    12: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 7,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 12,
    },
    13: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 6,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 11,
    },
    14: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 6,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 11,
    },
    15: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 6,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 11,
    },
    16: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 5,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 10,
    },
    17: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 5,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 10,
    },
    18: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 5,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 10,
    },
    19: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 4,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 10,
        SavingThrowCategory.SPELL: 9,
    },
    20: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 4,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 10,
        SavingThrowCategory.SPELL: 9,
    },
}

_MAGIC_USER_SAVES = {
    1: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 14,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 12,
    },
    2: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 14,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 12,
    },
    3: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 14,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 12,
    },
    4: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 14,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 12,
    },
    5: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 14,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 13,
        SavingThrowCategory.ROD_STAFF_WAND: 11,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 12,
    },
    6: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 10,
    },
    7: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 10,
    },
    8: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 10,
    },
    9: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 10,
    },
    10: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 9,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 10,
    },
    11: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 7,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 8,
    },
    12: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 7,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 8,
    },
    13: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 7,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 8,
    },
    14: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 7,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 8,
    },
    15: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 7,
        SavingThrowCategory.BREATH_WEAPON: 11,
        SavingThrowCategory.SPELL: 8,
    },
    16: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 5,
        SavingThrowCategory.BREATH_WEAPON: 9,
        SavingThrowCategory.SPELL: 6,
    },
    17: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 5,
        SavingThrowCategory.BREATH_WEAPON: 9,
        SavingThrowCategory.SPELL: 6,
    },
    18: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 5,
        SavingThrowCategory.BREATH_WEAPON: 9,
        SavingThrowCategory.SPELL: 6,
    },
    19: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 5,
        SavingThrowCategory.BREATH_WEAPON: 9,
        SavingThrowCategory.SPELL: 6,
    },
    20: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 7,
        SavingThrowCategory.ROD_STAFF_WAND: 5,
        SavingThrowCategory.BREATH_WEAPON: 9,
        SavingThrowCategory.SPELL: 6,
    },
}

_THIEF_SAVES = {
    1: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 15,
    },
    2: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 15,
    },
    3: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 15,
    },
    4: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 13,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 12,
        SavingThrowCategory.ROD_STAFF_WAND: 14,
        SavingThrowCategory.BREATH_WEAPON: 16,
        SavingThrowCategory.SPELL: 15,
    },
    5: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 12,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 13,
    },
    6: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 12,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 13,
    },
    7: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 12,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 13,
    },
    8: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 12,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 11,
        SavingThrowCategory.ROD_STAFF_WAND: 12,
        SavingThrowCategory.BREATH_WEAPON: 15,
        SavingThrowCategory.SPELL: 13,
    },
    9: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 11,
    },
    10: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 11,
    },
    11: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 11,
    },
    12: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 11,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 10,
        SavingThrowCategory.ROD_STAFF_WAND: 10,
        SavingThrowCategory.BREATH_WEAPON: 14,
        SavingThrowCategory.SPELL: 11,
    },
    13: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 9,
    },
    14: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 9,
    },
    15: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 9,
    },
    16: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 10,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 9,
        SavingThrowCategory.ROD_STAFF_WAND: 8,
        SavingThrowCategory.BREATH_WEAPON: 13,
        SavingThrowCategory.SPELL: 9,
    },
    17: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 6,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 7,
    },
    18: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 6,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 7,
    },
    19: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 6,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 7,
    },
    20: {
        SavingThrowCategory.PARALYZATION_POISON_DEATH: 9,
        SavingThrowCategory.PETRIFICATION_POLYMORPH: 8,
        SavingThrowCategory.ROD_STAFF_WAND: 6,
        SavingThrowCategory.BREATH_WEAPON: 12,
        SavingThrowCategory.SPELL: 7,
    },
}

# Map class names to their saving throw tables
_SAVING_THROW_TABLES = {
    "fighter": _FIGHTER_SAVES,
    "cleric": _CLERIC_SAVES,
    "magic_user": _MAGIC_USER_SAVES,
    "thief": _THIEF_SAVES,
}


@dataclass
class SavingThrowResult:
    """Result of a saving throw attempt.

    Attributes:
        success: Whether the saving throw succeeded
        roll: The d20 roll made
        target_number: The number needed to succeed
        final_modifier: Total modifier applied to the roll
        natural_20: Whether a natural 20 was rolled (automatic success)
        natural_1: Whether a natural 1 was rolled (automatic failure)
    """

    success: bool
    roll: int
    target_number: int
    final_modifier: int
    natural_20: bool = False
    natural_1: bool = False


def get_saving_throw(class_name: str, level: int, category: SavingThrowCategory) -> int:
    """Get the base saving throw value for a character class and level.

    This returns the target number that must be rolled on a d20 to succeed
    at the saving throw. Lower numbers are better (easier to save).

    Args:
        class_name: The character class (e.g., "fighter", "cleric", "magic_user", "thief")
        level: Character level (1-20)
        category: Which saving throw category to look up

    Returns:
        The target number needed on a d20 to succeed

    Raises:
        ValueError: If class_name is not recognized or level is invalid

    Example:
        >>> from src.rules.saving_throws import (
        ...     get_saving_throw,
        ...     SavingThrowCategory
        ... )
        >>> target = get_saving_throw(
        ...     "fighter", 5, SavingThrowCategory.PARALYZATION_POISON_DEATH
        ... )
        >>> print(f"Need to roll {target}+ on d20")
        Need to roll 12+ on d20
    """
    if level < 1 or level > 20:
        raise ValueError(f"Level must be between 1 and 20, got {level}")

    class_name = class_name.lower()
    if class_name not in _SAVING_THROW_TABLES:
        raise ValueError(
            f"Unknown class: {class_name}. "
            f"Valid classes: {', '.join(_SAVING_THROW_TABLES.keys())}"
        )

    return _SAVING_THROW_TABLES[class_name][level][category]


def get_racial_saving_throw_bonus(
    race: str, category: SavingThrowCategory, constitution: int
) -> int:
    """Get racial bonuses to saving throws.

    In AD&D 1E, dwarves and halflings get Constitution-based bonuses to
    certain saving throw categories. The bonus is based on Constitution:
    - Constitution 4-6: +1
    - Constitution 7-10: +2
    - Constitution 11-13: +3
    - Constitution 14-17: +4
    - Constitution 18+: +5

    Args:
        race: The character's race (case-insensitive)
        category: Which saving throw category
        constitution: Character's Constitution score

    Returns:
        Bonus to apply to the saving throw (positive numbers make it easier)

    Example:
        >>> bonus = get_racial_saving_throw_bonus(
        ...     "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 16
        ... )
        >>> print(f"Dwarf gets +{bonus} bonus vs poison")
        Dwarf gets +4 bonus vs poison
    """
    race = race.lower()

    # Calculate Constitution-based bonus for dwarves and halflings
    if constitution <= 3:
        con_bonus = 0
    elif constitution <= 6:
        con_bonus = 1
    elif constitution <= 10:
        con_bonus = 2
    elif constitution <= 13:
        con_bonus = 3
    elif constitution <= 17:
        con_bonus = 4
    else:  # 18+
        con_bonus = 5

    # Dwarves get bonuses vs poison/death magic and spells
    if race == "dwarf" or race == "hill dwarf" or race == "mountain dwarf":
        if category in (
            SavingThrowCategory.PARALYZATION_POISON_DEATH,
            SavingThrowCategory.SPELL,
        ):
            return con_bonus

    # Halflings get bonuses vs poison/death magic, rods/staves/wands, and spells
    if race == "halfling":
        if category in (
            SavingThrowCategory.PARALYZATION_POISON_DEATH,
            SavingThrowCategory.ROD_STAFF_WAND,
            SavingThrowCategory.SPELL,
        ):
            return con_bonus

    return 0


def make_saving_throw(
    class_name: str,
    level: int,
    category: SavingThrowCategory,
    constitution: int = 10,
    race: str = "human",
    modifier: int = 0,
    roll: int | None = None,
    roller: DiceRoller | None = None,
) -> SavingThrowResult:
    """Resolve a saving throw with all modifiers applied.

    This function handles the complete saving throw process:
    1. Gets base saving throw value for class/level
    2. Applies racial bonuses (if applicable)
    3. Applies any additional modifiers
    4. Rolls d20 (or uses provided roll for testing)
    5. Determines success/failure with special handling for natural 1/20

    Args:
        class_name: The character class
        level: Character level (1-20)
        category: Which saving throw category
        constitution: Character's Constitution score (default 10)
        race: Character's race (default "human")
        modifier: Additional modifier to apply (default 0)
        roll: Optional predetermined roll for testing (default None = random roll)
        roller: Optional DiceRoller for deterministic testing

    Returns:
        SavingThrowResult with all details of the saving throw attempt

    Raises:
        ValueError: If class_name is not recognized or level is invalid

    Example:
        >>> result = make_saving_throw(
        ...     class_name="fighter",
        ...     level=5,
        ...     category=SavingThrowCategory.BREATH_WEAPON,
        ...     constitution=16,
        ...     race="dwarf",
        ...     modifier=2,
        ...     roll=14
        ... )
        >>> print(f"Success: {result.success}, needed {result.target_number}")
        Success: True, needed 15
    """
    # Get base saving throw target
    target_number = get_saving_throw(class_name, level, category)

    # Get racial bonus
    racial_bonus = get_racial_saving_throw_bonus(race, category, constitution)

    # Calculate total modifier (racial + other modifiers)
    final_modifier = racial_bonus + modifier

    # Roll d20 if not provided
    if roll is None:
        if roller is None:
            roller = DiceRoller()
        roll = roller.roll_die(20)

    # Check for natural 1 or 20
    natural_1 = roll == 1
    natural_20 = roll == 20

    # Apply modifiers to roll (bonuses make it easier to save)
    modified_roll = roll + final_modifier

    # Determine success
    # Natural 20 always succeeds, natural 1 always fails (optional rule)
    if natural_20:
        success = True
    elif natural_1:
        success = False
    else:
        success = modified_roll >= target_number

    return SavingThrowResult(
        success=success,
        roll=roll,
        target_number=target_number,
        final_modifier=final_modifier,
        natural_20=natural_20,
        natural_1=natural_1,
    )
