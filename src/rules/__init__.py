"""AD&D 1E rules engine package.

This package contains modules implementing core AD&D 1E game mechanics
including abilities, character classes, races, combat, spells, and more.
"""

from src.rules.abilities import (
    AbilityScores,
    get_constitution_hp_modifier,
    get_dexterity_ac_modifier,
    get_dexterity_initiative_modifier,
    get_dexterity_modifiers,
    get_strength_damage_modifier,
    get_strength_hit_modifier,
    get_strength_modifiers,
)

__all__ = [
    "AbilityScores",
    "get_strength_hit_modifier",
    "get_strength_damage_modifier",
    "get_strength_modifiers",
    "get_dexterity_ac_modifier",
    "get_dexterity_initiative_modifier",
    "get_dexterity_modifiers",
    "get_constitution_hp_modifier",
]
