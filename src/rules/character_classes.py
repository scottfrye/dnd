"""Character classes module for AD&D 1E.

Implements the four base character classes from Advanced Dungeons & Dragons
1st Edition: Fighter, Cleric, Magic-User, and Thief. Includes level progression,
hit points, THAC0 calculation, class restrictions, and multi/dual-class support.

Public API:
    - Character: Base character class with common attributes
    - Fighter: Fighter class implementation
    - Cleric: Cleric class implementation
    - MagicUser: Magic-User class implementation
    - Thief: Thief class implementation
    - MultiClassCharacter: Multi-class character support
    - DualClassCharacter: Dual-class character support
    - calculate_hp: Calculate HP for a character level

Example Usage:
    >>> from src.rules.character_classes import Fighter
    >>> from src.rules.abilities import AbilityScores
    >>> scores = AbilityScores(strength=18, dexterity=14, constitution=16,
    ...                         intelligence=10, wisdom=12, charisma=8)
    >>> fighter = Fighter(name="Conan", ability_scores=scores, level=5)
    >>> print(f"THAC0: {fighter.thac0}, HP: {fighter.hit_points}")

References:
    - AD&D 1E Player's Handbook, Character Classes section
    - AD&D 1E Player's Handbook, Experience Tables
    - AD&D 1E Player's Handbook, Multi-Class and Dual-Class rules
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from src.rules.abilities import AbilityScores, get_constitution_hp_modifier
from src.rules.combat_system import get_thac0
from src.utils.dice import DiceRoller


class ArmorType(Enum):
    """Armor types for class restrictions."""

    NONE = "none"
    LEATHER = "leather"
    STUDDED_LEATHER = "studded_leather"
    RING_MAIL = "ring_mail"
    SCALE_MAIL = "scale_mail"
    CHAIN_MAIL = "chain_mail"
    SPLINT_MAIL = "splint_mail"
    PLATE_MAIL = "plate_mail"
    SHIELD = "shield"


class WeaponType(Enum):
    """Weapon types for class restrictions."""

    DAGGER = "dagger"
    SHORT_SWORD = "short_sword"
    LONG_SWORD = "long_sword"
    TWO_HANDED_SWORD = "two_handed_sword"
    SWORD = "sword"  # Generic sword
    STAFF = "staff"
    CLUB = "club"
    MACE = "mace"
    FLAIL = "flail"
    MORNING_STAR = "morning_star"
    WAR_HAMMER = "war_hammer"
    SHORT_BOW = "short_bow"
    LONG_BOW = "long_bow"
    LIGHT_CROSSBOW = "light_crossbow"
    HEAVY_CROSSBOW = "heavy_crossbow"
    SLING = "sling"
    SPEAR = "spear"
    POLEARM = "polearm"
    AXE = "axe"
    BATTLE_AXE = "battle_axe"
    HAND_AXE = "hand_axe"


# Experience point requirements by level (AD&D 1E PHB)
# Index 0 is unused, index 1 = level 1, index 2 = level 2, etc.
_FIGHTER_XP_TABLE: list[int] = [
    0,  # Level 0 (unused)
    0,  # Level 1
    2000,  # Level 2
    4000,  # Level 3
    8000,  # Level 4
    16000,  # Level 5
    32000,  # Level 6
    64000,  # Level 7
    125000,  # Level 8
    250000,  # Level 9
    500000,  # Level 10
    750000,  # Level 11
    1000000,  # Level 12
    1250000,  # Level 13
    1500000,  # Level 14
    1750000,  # Level 15
    2000000,  # Level 16
    2250000,  # Level 17
    2500000,  # Level 18
    2750000,  # Level 19
    3000000,  # Level 20
]

_CLERIC_XP_TABLE: list[int] = [
    0,  # Level 0 (unused)
    0,  # Level 1
    1500,  # Level 2
    3000,  # Level 3
    6000,  # Level 4
    13000,  # Level 5
    27500,  # Level 6
    55000,  # Level 7
    110000,  # Level 8
    225000,  # Level 9
    450000,  # Level 10
    675000,  # Level 11
    900000,  # Level 12
    1125000,  # Level 13
    1350000,  # Level 14
    1575000,  # Level 15
    1800000,  # Level 16
    2025000,  # Level 17
    2250000,  # Level 18
    2475000,  # Level 19
    2700000,  # Level 20
]

_MAGIC_USER_XP_TABLE: list[int] = [
    0,  # Level 0 (unused)
    0,  # Level 1
    2500,  # Level 2
    5000,  # Level 3
    10000,  # Level 4
    22500,  # Level 5
    40000,  # Level 6
    60000,  # Level 7
    90000,  # Level 8
    135000,  # Level 9
    250000,  # Level 10
    375000,  # Level 11
    750000,  # Level 12
    1125000,  # Level 13
    1500000,  # Level 14
    1875000,  # Level 15
    2250000,  # Level 16
    2625000,  # Level 17
    3000000,  # Level 18
    3375000,  # Level 19
    3750000,  # Level 20
]

_THIEF_XP_TABLE: list[int] = [
    0,  # Level 0 (unused)
    0,  # Level 1
    1250,  # Level 2
    2500,  # Level 3
    5000,  # Level 4
    10000,  # Level 5
    20000,  # Level 6
    40000,  # Level 7
    70000,  # Level 8
    110000,  # Level 9
    160000,  # Level 10
    220000,  # Level 11
    440000,  # Level 12
    660000,  # Level 13
    880000,  # Level 14
    1100000,  # Level 15
    1320000,  # Level 16
    1540000,  # Level 17
    1760000,  # Level 18
    1980000,  # Level 19
    2200000,  # Level 20
]


def calculate_hp(
    hit_die_sides: int,
    level: int,
    constitution_modifier: int,
    roller: DiceRoller | None = None,
    fixed_rolls: list[int] | None = None,
) -> int:
    """Calculate hit points for a character.

    Rolls hit dice for each level and applies constitution modifiers.
    Uses 1 HP minimum per level (even with penalties).

    Args:
        hit_die_sides: Number of sides on the hit die (e.g., 10 for d10)
        level: Character level (1-20)
        constitution_modifier: HP bonus/penalty per level from Constitution
        roller: Optional DiceRoller for deterministic testing
        fixed_rolls: Optional list of predetermined rolls for testing

    Returns:
        Total hit points for the character

    Raises:
        ValueError: If level is less than 1 or hit_die_sides is less than 1
    """
    if level < 1:
        raise ValueError(f"Level must be at least 1, got {level}")
    if hit_die_sides < 1:
        raise ValueError(f"Hit die must have at least 1 side, got {hit_die_sides}")

    if roller is None:
        roller = DiceRoller()

    total_hp = 0

    for i in range(level):
        if fixed_rolls is not None and i < len(fixed_rolls):
            roll = fixed_rolls[i]
        else:
            roll = roller.roll_die(hit_die_sides)

        # Apply constitution modifier, minimum 1 HP per level
        hp_this_level = max(1, roll + constitution_modifier)
        total_hp += hp_this_level

    return total_hp


@dataclass
class Character(ABC):
    """Base character class for AD&D 1E.

    This abstract base class defines common attributes and methods for all
    character classes. Subclasses must implement class-specific details like
    hit dice, allowed armor/weapons, and THAC0 progression.

    Attributes:
        name: Character's name
        ability_scores: Six primary ability scores
        level: Character level (1-20)
        experience_points: Total XP earned
        hit_points: Current/maximum hit points
        class_name: Name of the character class (e.g., "Fighter")
        hit_die_sides: Number of sides on the hit die
        thac0: To Hit Armor Class 0 value
        allowed_armor: Set of armor types the class can use
        allowed_weapons: Set of weapon types the class can use
    """

    name: str
    ability_scores: AbilityScores
    level: int = 1
    experience_points: int = 0
    hit_points: int = 0

    # Class-specific attributes (set by subclasses)
    class_name: str = field(init=False)
    hit_die_sides: int = field(init=False)
    thac0: int = field(init=False)
    allowed_armor: set[ArmorType] = field(default_factory=set, init=False)
    allowed_weapons: set[WeaponType] = field(default_factory=set, init=False)

    def __post_init__(self):
        """Initialize derived attributes after dataclass initialization."""
        if self.level < 1 or self.level > 20:
            raise ValueError(f"Level must be between 1 and 20, got {self.level}")

        # Calculate THAC0 based on class
        self.thac0 = self._calculate_thac0()

        # Calculate initial HP if not set
        if self.hit_points == 0:
            constitution_modifier = get_constitution_hp_modifier(
                self.ability_scores.constitution
            )
            self.hit_points = calculate_hp(
                self.hit_die_sides, self.level, constitution_modifier
            )

    @abstractmethod
    def _calculate_thac0(self) -> int:
        """Calculate THAC0 for this character's class and level.

        Returns:
            THAC0 value for the character
        """
        pass

    @abstractmethod
    def get_xp_for_next_level(self) -> int:
        """Get experience points required for next level.

        Returns:
            XP required to reach the next level, or 0 if at max level
        """
        pass

    def can_use_armor(self, armor: ArmorType) -> bool:
        """Check if character can use specified armor type.

        Args:
            armor: Armor type to check

        Returns:
            True if character can use this armor type
        """
        return armor in self.allowed_armor

    def can_use_weapon(self, weapon: WeaponType) -> bool:
        """Check if character can use specified weapon type.

        Args:
            weapon: Weapon type to check

        Returns:
            True if character can use this weapon type
        """
        return weapon in self.allowed_weapons

    def gain_experience(self, xp: int) -> bool:
        """Add experience points and check for level up.

        Args:
            xp: Experience points to add

        Returns:
            True if character leveled up, False otherwise
        """
        if xp < 0:
            raise ValueError(f"Cannot gain negative experience: {xp}")

        self.experience_points += xp
        xp_needed = self.get_xp_for_next_level()

        if xp_needed > 0 and self.experience_points >= xp_needed:
            return True

        return False


@dataclass
class Fighter(Character):
    """Fighter character class for AD&D 1E.

    Fighters are warriors skilled in combat. They have the best THAC0
    progression, the highest hit dice (d10), and can use all armor and weapons.

    Hit Die: d10
    THAC0 Progression: Improves every level (fighter group)
    Armor: All types including shields
    Weapons: All types

    References:
        - AD&D 1E PHB, Fighter class description
        - AD&D 1E PHB, Table I: Fighter Experience Levels
    """

    def __post_init__(self):
        """Initialize Fighter-specific attributes."""
        self.class_name = "Fighter"
        self.hit_die_sides = 10

        # Fighters can use all armor
        self.allowed_armor = {
            ArmorType.NONE,
            ArmorType.LEATHER,
            ArmorType.STUDDED_LEATHER,
            ArmorType.RING_MAIL,
            ArmorType.SCALE_MAIL,
            ArmorType.CHAIN_MAIL,
            ArmorType.SPLINT_MAIL,
            ArmorType.PLATE_MAIL,
            ArmorType.SHIELD,
        }

        # Fighters can use all weapons
        self.allowed_weapons = set(WeaponType)

        super().__post_init__()

    def _calculate_thac0(self) -> int:
        """Calculate THAC0 using fighter progression."""
        return get_thac0(self.level, "fighter")

    def get_xp_for_next_level(self) -> int:
        """Get XP required for next level."""
        if self.level >= 20:
            return 0
        return _FIGHTER_XP_TABLE[self.level + 1]


@dataclass
class Cleric(Character):
    """Cleric character class for AD&D 1E.

    Clerics are divine spellcasters who serve their deity. They have moderate
    combat ability, good hit dice (d8), and access to clerical spells.

    Hit Die: d8
    THAC0 Progression: Improves every 3 levels (cleric group)
    Armor: All types including shields
    Weapons: Blunt weapons only (no edged weapons)

    References:
        - AD&D 1E PHB, Cleric class description
        - AD&D 1E PHB, Table II: Cleric Experience Levels
    """

    def __post_init__(self):
        """Initialize Cleric-specific attributes."""
        self.class_name = "Cleric"
        self.hit_die_sides = 8

        # Clerics can use all armor
        self.allowed_armor = {
            ArmorType.NONE,
            ArmorType.LEATHER,
            ArmorType.STUDDED_LEATHER,
            ArmorType.RING_MAIL,
            ArmorType.SCALE_MAIL,
            ArmorType.CHAIN_MAIL,
            ArmorType.SPLINT_MAIL,
            ArmorType.PLATE_MAIL,
            ArmorType.SHIELD,
        }

        # Clerics can only use blunt weapons (no edged weapons)
        self.allowed_weapons = {
            WeaponType.CLUB,
            WeaponType.MACE,
            WeaponType.FLAIL,
            WeaponType.MORNING_STAR,
            WeaponType.WAR_HAMMER,
            WeaponType.STAFF,
            WeaponType.SLING,
        }

        super().__post_init__()

    def _calculate_thac0(self) -> int:
        """Calculate THAC0 using cleric progression."""
        return get_thac0(self.level, "cleric")

    def get_xp_for_next_level(self) -> int:
        """Get XP required for next level."""
        if self.level >= 20:
            return 0
        return _CLERIC_XP_TABLE[self.level + 1]


@dataclass
class MagicUser(Character):
    """Magic-User character class for AD&D 1E.

    Magic-Users are arcane spellcasters with powerful magic but weak combat
    ability. They have the lowest hit dice (d4) and limited weapon/armor options.

    Hit Die: d4
    THAC0 Progression: Improves every 5 levels (magic-user group)
    Armor: None (armor interferes with spellcasting)
    Weapons: Dagger, staff, dart (very limited)

    References:
        - AD&D 1E PHB, Magic-User class description
        - AD&D 1E PHB, Table IV: Magic-User Experience Levels
    """

    def __post_init__(self):
        """Initialize Magic-User-specific attributes."""
        self.class_name = "Magic-User"
        self.hit_die_sides = 4

        # Magic-Users cannot wear armor
        self.allowed_armor = {ArmorType.NONE}

        # Magic-Users have very limited weapon selection
        self.allowed_weapons = {
            WeaponType.DAGGER,
            WeaponType.STAFF,
        }

        super().__post_init__()

    def _calculate_thac0(self) -> int:
        """Calculate THAC0 using magic-user progression."""
        return get_thac0(self.level, "magic_user")

    def get_xp_for_next_level(self) -> int:
        """Get XP required for next level."""
        if self.level >= 20:
            return 0
        return _MAGIC_USER_XP_TABLE[self.level + 1]


@dataclass
class Thief(Character):
    """Thief character class for AD&D 1E.

    Thieves are skilled in stealth, locks, and traps. They have moderate hit
    dice (d6) and limited combat ability, but unique thieving skills.

    Hit Die: d6
    THAC0 Progression: Improves every 4 levels (thief group)
    Armor: Leather only (heavier armor reduces thieving skills)
    Weapons: Limited selection (small/concealable weapons)

    References:
        - AD&D 1E PHB, Thief class description
        - AD&D 1E PHB, Table III: Thief Experience Levels
    """

    def __post_init__(self):
        """Initialize Thief-specific attributes."""
        self.class_name = "Thief"
        self.hit_die_sides = 6

        # Thieves can only use leather armor
        self.allowed_armor = {
            ArmorType.NONE,
            ArmorType.LEATHER,
        }

        # Thieves have limited weapon selection
        self.allowed_weapons = {
            WeaponType.DAGGER,
            WeaponType.SHORT_SWORD,
            WeaponType.CLUB,
            WeaponType.SHORT_BOW,
            WeaponType.LIGHT_CROSSBOW,
            WeaponType.SLING,
            WeaponType.STAFF,
        }

        super().__post_init__()

    def _calculate_thac0(self) -> int:
        """Calculate THAC0 using thief progression."""
        return get_thac0(self.level, "thief")

    def get_xp_for_next_level(self) -> int:
        """Get XP required for next level."""
        if self.level >= 20:
            return 0
        return _THIEF_XP_TABLE[self.level + 1]


@dataclass
class MultiClassCharacter:
    """Multi-class character support for AD&D 1E.

    Multi-classing allows non-human characters to advance in multiple classes
    simultaneously. Experience points are divided evenly among all classes.

    This is a scaffolding implementation for future expansion.

    Attributes:
        name: Character's name
        ability_scores: Six primary ability scores
        classes: List of Character instances representing each class
        experience_points: Total XP (divided among classes)

    References:
        - AD&D 1E PHB, Multi-Class Characters section
    """

    name: str
    ability_scores: AbilityScores
    classes: list[Character]
    experience_points: int = 0

    def __post_init__(self):
        """Validate multi-class character."""
        if len(self.classes) < 2:
            raise ValueError("Multi-class character must have at least 2 classes")
        if len(self.classes) > 3:
            raise ValueError("Multi-class character cannot have more than 3 classes")

    def gain_experience(self, xp: int) -> None:
        """Add experience points, divided among all classes.

        Args:
            xp: Total experience points to add
        """
        if xp < 0:
            raise ValueError(f"Cannot gain negative experience: {xp}")

        self.experience_points += xp
        xp_per_class = xp // len(self.classes)

        for char_class in self.classes:
            char_class.gain_experience(xp_per_class)


@dataclass
class DualClassCharacter:
    """Dual-class character support for AD&D 1E.

    Dual-classing allows human characters to switch from one class to another.
    The character stops advancing in the original class and begins a new class.

    This is a scaffolding implementation for future expansion.

    Attributes:
        name: Character's name
        ability_scores: Six primary ability scores
        original_class: The first class the character advanced in
        new_class: The class the character is currently advancing in
        experience_points: Total XP in the new class

    References:
        - AD&D 1E PHB, Dual-Class Characters section
    """

    name: str
    ability_scores: AbilityScores
    original_class: Character
    new_class: Character
    experience_points: int = 0

    def __post_init__(self):
        """Validate dual-class character."""
        # In AD&D 1E, the original class must be at least level 2
        if self.original_class.level < 2:
            raise ValueError("Original class must be at least level 2 to dual-class")

        # New class typically starts at level 1
        if self.new_class.level != 1:
            raise ValueError("New class must start at level 1")

    def gain_experience(self, xp: int) -> None:
        """Add experience points to the new class only.

        Args:
            xp: Experience points to add
        """
        if xp < 0:
            raise ValueError(f"Cannot gain negative experience: {xp}")

        self.experience_points += xp
        self.new_class.gain_experience(xp)
