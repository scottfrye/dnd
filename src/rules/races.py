"""Character races module for AD&D 1E.

Implements the core character races from Advanced Dungeons & Dragons
1st Edition: Human, Elf (with sub-races), Dwarf (with sub-races), and Halfling.
Includes racial ability adjustments, level limits, special abilities, and languages.

Public API:
    - Race: Base race class with common attributes
    - Human: Human race implementation
    - Elf: Elf race base class
    - HighElf: High Elf sub-race
    - WoodElf: Wood Elf sub-race
    - Dwarf: Dwarf race base class
    - HillDwarf: Hill Dwarf sub-race
    - MountainDwarf: Mountain Dwarf sub-race
    - Halfling: Halfling race implementation

Example Usage:
    >>> from src.rules.races import HighElf
    >>> from src.rules.abilities import AbilityScores
    >>> scores = AbilityScores(strength=12, dexterity=16, constitution=14,
    ...                         intelligence=14, wisdom=10, charisma=12)
    >>> high_elf = HighElf()
    >>> adjusted = high_elf.apply_ability_adjustments(scores)
    >>> print(f"DEX: {adjusted.dexterity}, CON: {adjusted.constitution}")
    DEX: 17, CON: 13

References:
    - AD&D 1E Player's Handbook, Character Races section
    - AD&D 1E Player's Handbook, Racial Ability Adjustments
    - AD&D 1E Player's Handbook, Racial Level Limits
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.rules.abilities import AbilityScores


@dataclass
class RaceInfo:
    """Information about a character race.

    Attributes:
        name: Name of the race (e.g., "Human", "High Elf", "Hill Dwarf")
        ability_adjustments: Dict of ability score adjustments {ability: modifier}
        level_limits: Dict of class level limits {class_name: max_level}
        special_abilities: List of special ability names
        languages: List of languages the race can speak
        infravision_range: Range of infravision in feet (0 if none)
    """

    name: str
    ability_adjustments: dict[str, int]
    level_limits: dict[str, int]
    special_abilities: list[str]
    languages: list[str]
    infravision_range: int = 0


class Race(ABC):
    """Abstract base class for character races in AD&D 1E.

    All races implement methods for:
    - Applying ability score adjustments
    - Getting level limits for character classes
    - Listing special abilities
    - Listing racial languages
    """

    @abstractmethod
    def get_race_info(self) -> RaceInfo:
        """Get information about this race.

        Returns:
            RaceInfo object with race details
        """
        pass

    def apply_ability_adjustments(self, scores: AbilityScores) -> AbilityScores:
        """Apply racial ability score adjustments.

        Args:
            scores: Original ability scores

        Returns:
            New AbilityScores with racial adjustments applied

        Note:
            Ability scores are capped at 3 minimum and 18 maximum
            (except for exceptional strength which is not affected by this cap)
        """
        info = self.get_race_info()
        adjustments = info.ability_adjustments

        # Apply adjustments with min/max bounds (3-18)
        new_strength = max(3, min(18, scores.strength + adjustments.get("strength", 0)))
        new_dexterity = max(
            3, min(18, scores.dexterity + adjustments.get("dexterity", 0))
        )
        new_constitution = max(
            3, min(18, scores.constitution + adjustments.get("constitution", 0))
        )
        new_intelligence = max(
            3, min(18, scores.intelligence + adjustments.get("intelligence", 0))
        )
        new_wisdom = max(3, min(18, scores.wisdom + adjustments.get("wisdom", 0)))
        new_charisma = max(3, min(18, scores.charisma + adjustments.get("charisma", 0)))

        return AbilityScores(
            strength=new_strength,
            dexterity=new_dexterity,
            constitution=new_constitution,
            intelligence=new_intelligence,
            wisdom=new_wisdom,
            charisma=new_charisma,
        )

    def get_level_limit(self, class_name: str) -> int | None:
        """Get the maximum level for a given character class.

        Args:
            class_name: Name of the character class (e.g., "fighter", "cleric")

        Returns:
            Maximum level for the class, or None if unlimited
        """
        info = self.get_race_info()
        return info.level_limits.get(class_name)

    def get_special_abilities(self) -> list[str]:
        """Get list of special racial abilities.

        Returns:
            List of special ability descriptions
        """
        info = self.get_race_info()
        return info.special_abilities.copy()

    def get_languages(self) -> list[str]:
        """Get list of languages the race can speak.

        Returns:
            List of language names
        """
        info = self.get_race_info()
        return info.languages.copy()

    def get_infravision_range(self) -> int:
        """Get the infravision range in feet.

        Returns:
            Range in feet, or 0 if the race has no infravision
        """
        info = self.get_race_info()
        return info.infravision_range


class Human(Race):
    """Human race - no adjustments or limits.

    Humans are the most versatile race in AD&D 1E, with no ability
    score adjustments, no level limits, and no special abilities.
    They can advance to any level in any class.

    References:
        - AD&D 1E Player's Handbook, page 14-15
    """

    def get_race_info(self) -> RaceInfo:
        """Get human race information."""
        return RaceInfo(
            name="Human",
            ability_adjustments={},
            level_limits={},  # No level limits
            special_abilities=[],  # No special abilities
            languages=["Common"],
            infravision_range=0,
        )


class Elf(Race):
    """Base class for Elf sub-races.

    Elves in AD&D 1E have +1 DEX, -1 CON, 90% resistance to sleep and charm,
    infravision, and bonuses to detect secret doors. Sub-races may have
    additional adjustments.

    References:
        - AD&D 1E Player's Handbook, page 15-16
    """

    @abstractmethod
    def get_race_info(self) -> RaceInfo:
        """Get elf race information - implemented by sub-races."""
        pass


class HighElf(Elf):
    """High Elf sub-race.

    High elves have standard elf abilities with +1 DEX, -1 CON.
    They have level limits in most classes and various special abilities.

    References:
        - AD&D 1E Player's Handbook, page 15-16
    """

    def get_race_info(self) -> RaceInfo:
        """Get high elf race information."""
        return RaceInfo(
            name="High Elf",
            ability_adjustments={"dexterity": 1, "constitution": -1},
            level_limits={
                "cleric": 7,
                "fighter": 7,
                "magic_user": 11,
                "thief": 10,
                "ranger": 8,
                "fighter_magic_user": 7,  # Multi-class
                "fighter_thief": 7,
                "magic_user_thief": 10,
            },
            special_abilities=[
                "90% resistance to sleep and charm spells",
                "Surprise opponents 4 in 6 when alone or with other elves/halflings",
                "Detect secret doors (1 in 6 within 10 feet, 2 in 6 when searching)",
                "Detect concealed doors (3 in 6 when searching)",
                "+1 to hit with bow, short sword, or long sword",
            ],
            languages=[
                "Common",
                "Elvish",
                "Gnome",
                "Halfling",
                "Goblin",
                "Hobgoblin",
                "Orcish",
                "Gnoll",
            ],
            infravision_range=60,
        )


class WoodElf(Elf):
    """Wood Elf sub-race.

    Wood elves have standard elf abilities with +1 DEX, -1 CON.
    They are similar to high elves but with slightly different level limits
    and stronger connection to nature.

    References:
        - AD&D 1E Player's Handbook, page 15-16
    """

    def get_race_info(self) -> RaceInfo:
        """Get wood elf race information."""
        return RaceInfo(
            name="Wood Elf",
            ability_adjustments={"dexterity": 1, "constitution": -1},
            level_limits={
                "cleric": 7,
                "fighter": 7,
                "magic_user": 9,  # Lower than high elf
                "thief": 11,  # Higher than high elf
                "ranger": 8,
                "fighter_magic_user": 7,
                "fighter_thief": 7,
                "magic_user_thief": 9,
            },
            special_abilities=[
                "90% resistance to sleep and charm spells",
                "Surprise opponents 4 in 6 when alone or with other elves/halflings",
                "Detect secret doors (1 in 6 within 10 feet, 2 in 6 when searching)",
                "Detect concealed doors (3 in 6 when searching)",
                "+1 to hit with bow, short sword, or long sword",
            ],
            languages=[
                "Common",
                "Elvish",
                "Gnome",
                "Halfling",
                "Goblin",
                "Hobgoblin",
                "Orcish",
                "Gnoll",
            ],
            infravision_range=60,
        )


class Dwarf(Race):
    """Base class for Dwarf sub-races.

    Dwarves in AD&D 1E have +1 CON, -1 CHA, infravision, bonuses against
    magic and poison, and ability to detect slopes and new construction.
    Sub-races may have slight variations.

    References:
        - AD&D 1E Player's Handbook, page 16-17
    """

    @abstractmethod
    def get_race_info(self) -> RaceInfo:
        """Get dwarf race information - implemented by sub-races."""
        pass


class HillDwarf(Dwarf):
    """Hill Dwarf sub-race.

    Hill dwarves are the most common type of dwarf. They have +1 CON, -1 CHA
    and various special abilities related to stonework and combat.

    References:
        - AD&D 1E Player's Handbook, page 16-17
    """

    def get_race_info(self) -> RaceInfo:
        """Get hill dwarf race information."""
        return RaceInfo(
            name="Hill Dwarf",
            ability_adjustments={"constitution": 1, "charisma": -1},
            level_limits={
                "cleric": 8,
                "fighter": 9,
                "thief": 9,
                "assassin": 9,
                "fighter_thief": 9,
            },
            special_abilities=[
                "Saving throw bonus vs. magic based on constitution",
                "Saving throw bonus vs. poison based on constitution",
                "Detect grade or slope in passage (75%)",
                "Detect new tunnel/passage construction (75%)",
                "Detect sliding/shifting walls or rooms (66%)",
                "Detect stonework traps, pits, and deadfalls (50%)",
                "Determine approximate depth underground (50%)",
                "+1 to hit orcs, half-orcs, goblins, and hobgoblins",
                "AC bonus against giants, ogres, and titans based on size",
            ],
            languages=["Common", "Dwarvish", "Gnome", "Goblin", "Kobold", "Orcish"],
            infravision_range=60,
        )


class MountainDwarf(Dwarf):
    """Mountain Dwarf sub-race.

    Mountain dwarves are similar to hill dwarves but slightly hardier.
    They have +1 CON, -1 CHA and the same special abilities as hill dwarves.

    References:
        - AD&D 1E Player's Handbook, page 16-17
    """

    def get_race_info(self) -> RaceInfo:
        """Get mountain dwarf race information."""
        return RaceInfo(
            name="Mountain Dwarf",
            ability_adjustments={"constitution": 1, "charisma": -1},
            level_limits={
                "cleric": 8,
                "fighter": 10,  # Slightly higher than hill dwarf
                "thief": 9,
                "assassin": 9,
                "fighter_thief": 9,
            },
            special_abilities=[
                "Saving throw bonus vs. magic based on constitution",
                "Saving throw bonus vs. poison based on constitution",
                "Detect grade or slope in passage (75%)",
                "Detect new tunnel/passage construction (75%)",
                "Detect sliding/shifting walls or rooms (66%)",
                "Detect stonework traps, pits, and deadfalls (50%)",
                "Determine approximate depth underground (50%)",
                "+1 to hit orcs, half-orcs, goblins, and hobgoblins",
                "AC bonus against giants, ogres, and titans based on size",
            ],
            languages=["Common", "Dwarvish", "Gnome", "Goblin", "Kobold", "Orcish"],
            infravision_range=60,
        )


class Halfling(Race):
    """Halfling race.

    Halflings have +1 DEX, -1 STR, and various special abilities including
    bonuses to saving throws, hiding, and using slings. They are similar
    to hobbits in other fantasy settings.

    References:
        - AD&D 1E Player's Handbook, page 17-18
    """

    def get_race_info(self) -> RaceInfo:
        """Get halfling race information."""
        return RaceInfo(
            name="Halfling",
            ability_adjustments={"dexterity": 1, "strength": -1},
            level_limits={"cleric": 6, "fighter": 6, "thief": 10, "fighter_thief": 6},
            special_abilities=[
                "Saving throw bonus vs. magic based on constitution",
                "Saving throw bonus vs. poison based on constitution",
                "+3 to hit with slings and thrown weapons",
                "Surprise opponents 4 in 6 in woods or underbrush",
                "Hide in shadows/move silently (outdoor: 4 in 6, dungeons: 2 in 6)",
                "AC bonus against large creatures based on size",
            ],
            languages=["Common", "Halfling", "Dwarvish", "Gnome", "Goblin", "Orcish"],
            infravision_range=0,  # Halflings do not have infravision
        )
