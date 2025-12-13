"""Character entity module for AD&D 1E.

This module provides the Character class that integrates the game's rules systems
(abilities, races, classes) into a complete, playable character entity. Characters
have stats (HP, AC, THAC0), inventory, and can be serialized for persistence.

Public API:
    - Character: Main character entity class
    - create_character: Factory function for creating characters

Example Usage:
    >>> from src.entities.character import Character
    >>> from src.rules.abilities import AbilityScores
    >>> from src.rules.races import Human
    >>> from src.rules.character_classes import Fighter
    >>> 
    >>> scores = AbilityScores(strength=16, dexterity=14, constitution=15,
    ...                         intelligence=10, wisdom=12, charisma=8)
    >>> race = Human()
    >>> char_class = Fighter(name="Conan", ability_scores=scores, level=1)
    >>> 
    >>> character = Character(
    ...     name="Conan",
    ...     race=race,
    ...     character_class=char_class,
    ...     ability_scores=scores
    ... )
    >>> print(f"HP: {character.hit_points}, AC: {character.armor_class}, THAC0: {character.thac0}")

References:
    - AD&D 1E Player's Handbook, Character Creation
    - AD&D 1E Player's Handbook, Combat section
"""

from dataclasses import dataclass, field
from typing import Any

from src.rules.abilities import (
    AbilityScores,
    get_constitution_hp_modifier,
    get_dexterity_ac_modifier,
)
from src.rules.character_classes import Character as CharacterClass
from src.rules.races import Race


@dataclass
class Character:
    """Complete character entity for AD&D 1E gameplay.

    Integrates ability scores, race, character class, and combat statistics
    into a single playable character. Handles stat calculations based on
    AD&D 1E rules and provides serialization for persistence.

    Attributes:
        name: Character's name
        race: Character's race (Human, Elf, Dwarf, Halfling, etc.)
        character_class: Character's class (Fighter, Cleric, Magic-User, Thief)
        ability_scores: Six primary ability scores
        inventory: List of items in character's inventory (scaffolding)
        hit_points: Current hit points (calculated from class + CON)
        max_hit_points: Maximum hit points
        armor_class: Armor Class (base 10 + DEX modifier + armor)
        thac0: To Hit Armor Class 0 (from character class)
        experience_points: Total experience points earned
        level: Character level (from character class)

    Notes:
        - HP is calculated from character class hit dice + constitution modifier
        - AC starts at 10 (no armor) and is modified by DEX and worn armor
        - THAC0 comes directly from the character class
        - Inventory is currently a scaffolding (list of item names/dicts)
    """

    name: str
    race: Race
    character_class: CharacterClass
    ability_scores: AbilityScores
    inventory: list[dict[str, Any]] = field(default_factory=list)
    _max_hit_points: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        """Initialize derived character statistics.

        Calculates HP, AC, THAC0, and other stats based on ability scores,
        race, and character class. This is called automatically after the
        dataclass __init__.
        """
        # Ensure ability scores have racial adjustments applied
        self._adjusted_scores = self.race.apply_ability_adjustments(self.ability_scores)

        # Update character class ability scores with adjusted values
        self.character_class.ability_scores = self._adjusted_scores

        # Store max HP from character class
        self._max_hit_points = self.character_class.hit_points

    @property
    def hit_points(self) -> int:
        """Get current hit points from character class.

        Returns:
            Current HP value
        """
        return self.character_class.hit_points

    @hit_points.setter
    def hit_points(self, value: int) -> None:
        """Set current hit points.

        Args:
            value: New HP value
        """
        self.character_class.hit_points = max(0, value)

    @property
    def max_hit_points(self) -> int:
        """Get maximum hit points.

        Returns:
            Maximum HP value
        """
        return self._max_hit_points

    @property
    def armor_class(self) -> int:
        """Calculate armor class.

        Base AC is 10 (no armor). Dexterity modifier adjusts AC (negative is
        better in AD&D 1E). Worn armor would further modify AC, but armor
        implementation is scaffolding for now.

        Returns:
            Current AC value (lower is better)
        """
        base_ac = 10
        dex_modifier = get_dexterity_ac_modifier(self._adjusted_scores.dexterity)
        # TODO: Add armor bonuses when armor system is implemented
        return base_ac + dex_modifier

    @property
    def thac0(self) -> int:
        """Get THAC0 (To Hit Armor Class 0) from character class.

        Returns:
            THAC0 value (lower is better)
        """
        return self.character_class.thac0

    @property
    def experience_points(self) -> int:
        """Get total experience points from character class.

        Returns:
            Current XP value
        """
        return self.character_class.experience_points

    @experience_points.setter
    def experience_points(self, value: int) -> None:
        """Set experience points.

        Args:
            value: New XP value
        """
        self.character_class.experience_points = value

    @property
    def level(self) -> int:
        """Get character level from character class.

        Returns:
            Current level (1-20)
        """
        return self.character_class.level

    def gain_experience(self, xp: int) -> bool:
        """Add experience points and check for level up.

        Args:
            xp: Experience points to add

        Returns:
            True if character leveled up, False otherwise

        Raises:
            ValueError: If xp is negative
        """
        return self.character_class.gain_experience(xp)

    def take_damage(self, damage: int) -> int:
        """Apply damage to character.

        Args:
            damage: Amount of damage to take

        Returns:
            Actual damage taken (non-negative)
        """
        if damage < 0:
            damage = 0

        old_hp = self.hit_points
        self.hit_points = max(0, self.hit_points - damage)
        actual_damage = old_hp - self.hit_points
        return actual_damage

    def heal(self, amount: int) -> int:
        """Heal character hit points.

        Args:
            amount: Amount to heal

        Returns:
            Actual healing applied (cannot exceed max HP)
        """
        if amount < 0:
            amount = 0

        old_hp = self.hit_points
        self.hit_points = min(self.max_hit_points, self.hit_points + amount)
        actual_healing = self.hit_points - old_hp
        return actual_healing

    def is_alive(self) -> bool:
        """Check if character is alive.

        Returns:
            True if HP > 0, False otherwise
        """
        return self.hit_points > 0

    def add_item(self, item: dict[str, Any]) -> None:
        """Add an item to inventory.

        Args:
            item: Item dictionary with properties like name, type, etc.
        """
        self.inventory.append(item.copy())

    def remove_item(self, item_name: str) -> bool:
        """Remove an item from inventory by name.

        Args:
            item_name: Name of the item to remove

        Returns:
            True if item was found and removed, False otherwise
        """
        for i, item in enumerate(self.inventory):
            if item.get("name") == item_name:
                self.inventory.pop(i)
                return True
        return False

    def to_dict(self) -> dict[str, Any]:
        """Serialize character to dictionary for persistence.

        Returns:
            Dictionary representation suitable for JSON/YAML serialization
        """
        # Get race class name for deserialization
        race_name = self.race.__class__.__name__

        # Get character class data
        char_class_data = {
            "class_name": self.character_class.class_name,
            "level": self.character_class.level,
            "experience_points": self.character_class.experience_points,
            "hit_points": self.character_class.hit_points,
            "max_hit_points": self._max_hit_points,
        }

        # Get ability scores (original, unadjusted)
        abilities_data = {
            "strength": self.ability_scores.strength,
            "dexterity": self.ability_scores.dexterity,
            "constitution": self.ability_scores.constitution,
            "intelligence": self.ability_scores.intelligence,
            "wisdom": self.ability_scores.wisdom,
            "charisma": self.ability_scores.charisma,
        }

        return {
            "name": self.name,
            "race": race_name,
            "character_class": char_class_data,
            "ability_scores": abilities_data,
            "inventory": [item.copy() for item in self.inventory],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Character":
        """Deserialize character from dictionary.

        Args:
            data: Dictionary representation of character

        Returns:
            New Character instance

        Raises:
            ValueError: If data is invalid or contains unknown race/class
        """
        # Import here to avoid circular dependencies
        from src.rules.character_classes import Cleric, Fighter, MagicUser, Thief
        from src.rules.races import (
            Halfling,
            HighElf,
            HillDwarf,
            Human,
            MountainDwarf,
            WoodElf,
        )

        # Map race names to classes
        race_map = {
            "Human": Human,
            "HighElf": HighElf,
            "WoodElf": WoodElf,
            "HillDwarf": HillDwarf,
            "MountainDwarf": MountainDwarf,
            "Halfling": Halfling,
        }

        # Map class names to classes
        class_map = {
            "Fighter": Fighter,
            "Cleric": Cleric,
            "Magic-User": MagicUser,
            "Thief": Thief,
        }

        # Reconstruct ability scores
        abilities_data = data["ability_scores"]
        ability_scores = AbilityScores(
            strength=abilities_data["strength"],
            dexterity=abilities_data["dexterity"],
            constitution=abilities_data["constitution"],
            intelligence=abilities_data["intelligence"],
            wisdom=abilities_data["wisdom"],
            charisma=abilities_data["charisma"],
        )

        # Reconstruct race
        race_name = data["race"]
        if race_name not in race_map:
            raise ValueError(f"Unknown race: {race_name}")
        race = race_map[race_name]()

        # Reconstruct character class
        char_class_data = data["character_class"]
        class_name = char_class_data["class_name"]
        if class_name not in class_map:
            raise ValueError(f"Unknown character class: {class_name}")

        char_class = class_map[class_name](
            name=data["name"],
            ability_scores=ability_scores,
            level=char_class_data["level"],
            experience_points=char_class_data["experience_points"],
            hit_points=char_class_data["hit_points"],
        )

        # Create character
        character = cls(
            name=data["name"],
            race=race,
            character_class=char_class,
            ability_scores=ability_scores,
            inventory=[item.copy() for item in data.get("inventory", [])],
        )

        # Restore max HP if present (for backward compatibility, default to current HP)
        character._max_hit_points = char_class_data.get(
            "max_hit_points", char_class_data["hit_points"]
        )

        return character


def create_character(
    name: str,
    race: Race,
    character_class_type: type[CharacterClass],
    ability_scores: AbilityScores,
    level: int = 1,
) -> Character:
    """Factory function to create a character.

    This is a convenience function that handles the proper initialization
    order for creating a character with a race and class.

    Args:
        name: Character's name
        race: Character's race instance
        character_class_type: Character class type (Fighter, Cleric, etc.)
        ability_scores: Ability scores (will be adjusted by race)
        level: Starting level (default 1)

    Returns:
        New Character instance

    Example:
        >>> from src.entities.character import create_character
        >>> from src.rules.abilities import AbilityScores
        >>> from src.rules.races import Human
        >>> from src.rules.character_classes import Fighter
        >>> 
        >>> scores = AbilityScores(16, 14, 15, 10, 12, 8)
        >>> char = create_character("Conan", Human(), Fighter, scores, level=1)
    """
    # Apply racial adjustments to ability scores
    adjusted_scores = race.apply_ability_adjustments(ability_scores)

    # Create character class instance
    char_class = character_class_type(
        name=name, ability_scores=adjusted_scores, level=level
    )

    # Create and return character
    return Character(
        name=name,
        race=race,
        character_class=char_class,
        ability_scores=ability_scores,  # Store original scores
    )
