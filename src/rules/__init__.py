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
from src.rules.character_classes import (
    ArmorType,
    Character,
    Cleric,
    DualClassCharacter,
    Fighter,
    MagicUser,
    MultiClassCharacter,
    Thief,
    WeaponType,
    calculate_hp,
)
from src.rules.combat_system import (
    AttackResult,
    CombatStats,
    calculate_target_number,
    get_thac0,
    resolve_attack,
    resolve_attack_simple,
)

__all__ = [
    # Abilities
    "AbilityScores",
    "get_strength_hit_modifier",
    "get_strength_damage_modifier",
    "get_strength_modifiers",
    "get_dexterity_ac_modifier",
    "get_dexterity_initiative_modifier",
    "get_dexterity_modifiers",
    "get_constitution_hp_modifier",
    # Character Classes
    "Character",
    "Fighter",
    "Cleric",
    "MagicUser",
    "Thief",
    "MultiClassCharacter",
    "DualClassCharacter",
    "ArmorType",
    "WeaponType",
    "calculate_hp",
    # Combat System
    "CombatStats",
    "AttackResult",
    "get_thac0",
    "calculate_target_number",
    "resolve_attack",
    "resolve_attack_simple",
]
