"""Ability scores module for AD&D 1E.

Provides storage and modifier calculations for the six primary ability scores:
Strength (STR), Dexterity (DEX), Constitution (CON),
Intelligence (INT), Wisdom (WIS), and Charisma (CHA).

Modifiers are based on AD&D 1E rules from the Player's Handbook.
"""

from dataclasses import dataclass


@dataclass
class AbilityScores:
    """Storage for the six primary ability scores in AD&D 1E.

    Each ability score typically ranges from 3-18, with exceptional
    strength (for fighters) potentially reaching 18/00.

    Attributes:
        strength: Physical power, affects hit and damage bonuses
        dexterity: Agility, affects AC and initiative
        constitution: Health, affects HP bonus
        intelligence: Mental acuity
        wisdom: Perception and willpower
        charisma: Leadership and personality
    """

    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    def __post_init__(self) -> None:
        """Validate that all ability scores are within valid range."""
        for attr_name in [
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ]:
            value = getattr(self, attr_name)
            if not isinstance(value, int) or value < 1:
                raise ValueError(f"{attr_name} must be a positive integer, got {value}")


# AD&D 1E Strength modifiers (to-hit and damage)
# Based on Player's Handbook Table I
_STRENGTH_MODIFIERS: dict[int, tuple[int, int]] = {
    1: (-5, -4),
    2: (-3, -2),
    3: (-3, -1),
    4: (-2, -1),
    5: (-2, -1),
    6: (-1, 0),
    7: (-1, 0),
    8: (0, 0),
    9: (0, 0),
    10: (0, 0),
    11: (0, 0),
    12: (0, 0),
    13: (0, 0),
    14: (0, 0),
    15: (0, 0),
    16: (0, +1),
    17: (+1, +1),
    18: (+1, +2),
    # Exceptional strength for fighters (18/01-18/00) would be handled separately
    # 19+ for monsters or magic-enhanced characters
    19: (+3, +7),
    20: (+3, +8),
    21: (+4, +9),
    22: (+4, +10),
    23: (+5, +11),
    24: (+6, +12),
    25: (+7, +14),
}


# AD&D 1E Dexterity modifiers (reaction/initiative and defensive/AC)
# Based on Player's Handbook Table II
_DEXTERITY_MODIFIERS: dict[int, tuple[int, int]] = {
    1: (-6, +5),  # (reaction adj, AC adj) - positive AC adj is worse in AD&D
    2: (-4, +5),
    3: (-3, +4),
    4: (-2, +3),
    5: (-1, +2),
    6: (0, +1),
    7: (0, 0),
    8: (0, 0),
    9: (0, 0),
    10: (0, 0),
    11: (0, 0),
    12: (0, 0),
    13: (0, 0),
    14: (0, 0),
    15: (0, -1),
    16: (+1, -2),
    17: (+2, -3),
    18: (+2, -4),
    19: (+3, -4),
    20: (+3, -4),
    21: (+4, -5),
    22: (+4, -5),
    23: (+4, -5),
    24: (+5, -6),
    25: (+5, -6),
}


# AD&D 1E Constitution HP modifiers
# Based on Player's Handbook Table III
_CONSTITUTION_HP_MODIFIERS: dict[int, int] = {
    1: -3,
    2: -2,
    3: -2,
    4: -1,
    5: -1,
    6: -1,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: +1,
    16: +2,
    17: +2,  # +3 for fighters (handled by class-specific logic if needed)
    18: +2,  # +4 for fighters
    19: +2,  # +5 for fighters
    20: +2,  # +5 for fighters
    21: +2,  # +6 for fighters
    22: +2,  # +6 for fighters
    23: +2,  # +6 for fighters
    24: +2,  # +7 for fighters
    25: +2,  # +7 for fighters
}


def get_strength_hit_modifier(strength: int) -> int:
    """Get the to-hit modifier based on Strength score.

    Args:
        strength: The character's Strength score.

    Returns:
        The to-hit modifier (positive is better).

    Raises:
        ValueError: If strength is not a valid score.
    """
    if strength < 1:
        raise ValueError(f"Strength must be at least 1, got {strength}")
    if strength > 25:
        # For very high strength, use the highest defined value
        strength = 25
    if strength in _STRENGTH_MODIFIERS:
        return _STRENGTH_MODIFIERS[strength][0]
    # Should not reach here with valid input
    raise ValueError(f"Invalid strength score: {strength}")


def get_strength_damage_modifier(strength: int) -> int:
    """Get the damage modifier based on Strength score.

    Args:
        strength: The character's Strength score.

    Returns:
        The damage modifier (positive is better).

    Raises:
        ValueError: If strength is not a valid score.
    """
    if strength < 1:
        raise ValueError(f"Strength must be at least 1, got {strength}")
    if strength > 25:
        strength = 25
    if strength in _STRENGTH_MODIFIERS:
        return _STRENGTH_MODIFIERS[strength][1]
    raise ValueError(f"Invalid strength score: {strength}")


def get_strength_modifiers(strength: int) -> tuple[int, int]:
    """Get both hit and damage modifiers based on Strength score.

    Args:
        strength: The character's Strength score.

    Returns:
        A tuple of (hit_modifier, damage_modifier).

    Raises:
        ValueError: If strength is not a valid score.
    """
    return (
        get_strength_hit_modifier(strength),
        get_strength_damage_modifier(strength),
    )


def get_dexterity_ac_modifier(dexterity: int) -> int:
    """Get the AC modifier based on Dexterity score.

    In AD&D 1E, lower AC is better. A negative modifier improves AC.

    Args:
        dexterity: The character's Dexterity score.

    Returns:
        The AC modifier (negative is better in AD&D 1E).

    Raises:
        ValueError: If dexterity is not a valid score.
    """
    if dexterity < 1:
        raise ValueError(f"Dexterity must be at least 1, got {dexterity}")
    if dexterity > 25:
        dexterity = 25
    if dexterity in _DEXTERITY_MODIFIERS:
        return _DEXTERITY_MODIFIERS[dexterity][1]
    raise ValueError(f"Invalid dexterity score: {dexterity}")


def get_dexterity_initiative_modifier(dexterity: int) -> int:
    """Get the initiative/reaction modifier based on Dexterity score.

    Args:
        dexterity: The character's Dexterity score.

    Returns:
        The initiative modifier (positive is better, acts sooner).

    Raises:
        ValueError: If dexterity is not a valid score.
    """
    if dexterity < 1:
        raise ValueError(f"Dexterity must be at least 1, got {dexterity}")
    if dexterity > 25:
        dexterity = 25
    if dexterity in _DEXTERITY_MODIFIERS:
        return _DEXTERITY_MODIFIERS[dexterity][0]
    raise ValueError(f"Invalid dexterity score: {dexterity}")


def get_dexterity_modifiers(dexterity: int) -> tuple[int, int]:
    """Get both initiative and AC modifiers based on Dexterity score.

    Args:
        dexterity: The character's Dexterity score.

    Returns:
        A tuple of (initiative_modifier, ac_modifier).

    Raises:
        ValueError: If dexterity is not a valid score.
    """
    return (
        get_dexterity_initiative_modifier(dexterity),
        get_dexterity_ac_modifier(dexterity),
    )


def get_constitution_hp_modifier(constitution: int) -> int:
    """Get the HP per level modifier based on Constitution score.

    Note: In AD&D 1E, fighters and related classes can get higher bonuses
    for Constitution 17+. This function returns the base modifier for
    non-fighter classes.

    Args:
        constitution: The character's Constitution score.

    Returns:
        The HP modifier per level (positive is better).

    Raises:
        ValueError: If constitution is not a valid score.
    """
    if constitution < 1:
        raise ValueError(f"Constitution must be at least 1, got {constitution}")
    if constitution > 25:
        constitution = 25
    if constitution in _CONSTITUTION_HP_MODIFIERS:
        return _CONSTITUTION_HP_MODIFIERS[constitution]
    raise ValueError(f"Invalid constitution score: {constitution}")
