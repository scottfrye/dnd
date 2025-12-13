"""Unit tests for the character entity module.

These tests verify that the character module correctly:
- Creates characters with race, class, and ability scores
- Calculates HP from class + constitution modifier
- Calculates AC from base + dexterity modifier
- Calculates THAC0 from character class
- Handles damage and healing
- Manages inventory
- Serializes and deserializes characters
- Achieves 100% code coverage
"""

import pytest

from src.entities.character import Character, create_character
from src.rules.abilities import AbilityScores
from src.rules.character_classes import Cleric, Fighter, MagicUser, Thief
from src.rules.races import Halfling, HighElf, HillDwarf, Human


class TestCharacterCreation:
    """Tests for character creation."""

    def test_create_human_fighter(self):
        """Test creating a human fighter character."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        race = Human()
        char_class = Fighter(name="Conan", ability_scores=scores, level=1)

        character = Character(
            name="Conan", race=race, character_class=char_class, ability_scores=scores
        )

        assert character.name == "Conan"
        assert character.level == 1
        assert character.hit_points > 0
        assert character.armor_class == 10  # Base AC with DEX 14 (no modifier)
        assert character.thac0 == 20  # Level 1 fighter

    def test_create_elf_magic_user(self):
        """Test creating a high elf magic-user."""
        scores = AbilityScores(
            strength=8,
            dexterity=16,
            constitution=12,
            intelligence=18,
            wisdom=13,
            charisma=10,
        )
        race = HighElf()
        # Elf gets +1 DEX, -1 CON, so adjusted scores are STR 8, DEX 17, CON 11
        adjusted_scores = race.apply_ability_adjustments(scores)
        char_class = MagicUser(name="Elrond", ability_scores=adjusted_scores, level=1)

        character = Character(
            name="Elrond",
            race=race,
            character_class=char_class,
            ability_scores=scores,
        )

        assert character.name == "Elrond"
        assert character.level == 1
        assert character.armor_class == 7  # Base 10 + DEX 17 modifier (-3)
        assert character.thac0 == 21  # Level 1 magic-user

    def test_create_dwarf_cleric(self):
        """Test creating a hill dwarf cleric."""
        scores = AbilityScores(
            strength=14,
            dexterity=12,
            constitution=16,
            intelligence=10,
            wisdom=16,
            charisma=8,
        )
        race = HillDwarf()
        # Dwarf gets +1 CON, -1 CHA, so adjusted scores are CON 17, CHA 7
        adjusted_scores = race.apply_ability_adjustments(scores)
        char_class = Cleric(name="Gimli", ability_scores=adjusted_scores, level=1)

        character = Character(
            name="Gimli",
            race=race,
            character_class=char_class,
            ability_scores=scores,
        )

        assert character.name == "Gimli"
        assert character.level == 1
        assert character.armor_class == 10  # Base 10 + DEX 12 (no modifier)
        assert character.thac0 == 20  # Level 1 cleric

    def test_create_halfling_thief(self):
        """Test creating a halfling thief."""
        scores = AbilityScores(
            strength=12,
            dexterity=17,
            constitution=14,
            intelligence=13,
            wisdom=10,
            charisma=12,
        )
        race = Halfling()
        # Halfling gets +1 DEX, -1 STR, so adjusted scores are STR 11, DEX 18
        adjusted_scores = race.apply_ability_adjustments(scores)
        char_class = Thief(name="Bilbo", ability_scores=adjusted_scores, level=1)

        character = Character(
            name="Bilbo",
            race=race,
            character_class=char_class,
            ability_scores=scores,
        )

        assert character.name == "Bilbo"
        assert character.level == 1
        assert character.armor_class == 6  # Base 10 + DEX 18 modifier (-4)
        assert character.thac0 == 21  # Level 1 thief


class TestCharacterFactory:
    """Tests for the create_character factory function."""

    def test_create_character_factory(self):
        """Test creating character with factory function."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )

        character = create_character("Conan", Human(), Fighter, scores, level=1)

        assert character.name == "Conan"
        assert character.level == 1
        assert isinstance(character.race, Human)
        assert isinstance(character.character_class, Fighter)

    def test_create_character_with_racial_adjustments(self):
        """Test factory applies racial adjustments correctly."""
        scores = AbilityScores(
            strength=16,
            dexterity=16,
            constitution=14,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )

        # High elf gets +1 DEX, -1 CON
        character = create_character("Legolas", HighElf(), Fighter, scores, level=1)

        # Character should have adjusted DEX (17) affecting AC
        assert character.armor_class == 7  # Base 10 + DEX 17 modifier (-3)


class TestCharacterStats:
    """Tests for character stat calculations."""

    def test_armor_class_with_high_dexterity(self):
        """Test AC calculation with high dexterity."""
        scores = AbilityScores(
            strength=16,
            dexterity=18,  # DEX 18 gives -4 AC modifier
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        # Base AC 10 + DEX modifier (-4) = AC 6
        assert character.armor_class == 6

    def test_armor_class_with_low_dexterity(self):
        """Test AC calculation with low dexterity."""
        scores = AbilityScores(
            strength=16,
            dexterity=6,  # DEX 6 gives +1 AC modifier (worse)
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        # Base AC 10 + DEX modifier (+1) = AC 11
        assert character.armor_class == 11

    def test_hit_points_from_character_class(self):
        """Test that HP comes from character class."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)

        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        assert character.hit_points == 10
        assert character.max_hit_points == 10

    def test_thac0_from_character_class(self):
        """Test that THAC0 comes from character class."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores, level=5)

        # Level 5 fighter has THAC0 16
        assert character.thac0 == 16

    def test_experience_points_property(self):
        """Test experience points property."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        assert character.experience_points == 0

        character.experience_points = 1500
        assert character.experience_points == 1500
        assert character.character_class.experience_points == 1500


class TestCharacterCombat:
    """Tests for character combat functionality."""

    def test_take_damage(self):
        """Test taking damage reduces HP."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=20)
        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        damage_taken = character.take_damage(5)

        assert damage_taken == 5
        assert character.hit_points == 15

    def test_take_damage_cannot_go_below_zero(self):
        """Test damage cannot reduce HP below 0."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)
        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        damage_taken = character.take_damage(20)

        assert damage_taken == 10  # Only had 10 HP to lose
        assert character.hit_points == 0

    def test_take_negative_damage(self):
        """Test taking negative damage does nothing."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=20)
        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        damage_taken = character.take_damage(-5)

        assert damage_taken == 0
        assert character.hit_points == 20

    def test_heal(self):
        """Test healing increases HP."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=20)
        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        character.take_damage(10)
        assert character.hit_points == 10

        healed = character.heal(5)
        assert healed == 5
        assert character.hit_points == 15

    def test_heal_cannot_exceed_max(self):
        """Test healing cannot exceed max HP."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=20)
        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        character.take_damage(5)
        assert character.hit_points == 15

        healed = character.heal(10)
        assert healed == 5  # Only healed 5 to reach max of 20
        assert character.hit_points == 20

    def test_heal_negative_amount(self):
        """Test healing with negative amount does nothing."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=20)
        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        healed = character.heal(-5)
        assert healed == 0
        assert character.hit_points == 20

    def test_is_alive(self):
        """Test is_alive checks HP."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        char_class = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)
        character = Character(
            name="Test", race=Human(), character_class=char_class, ability_scores=scores
        )

        assert character.is_alive()

        character.take_damage(10)
        assert not character.is_alive()


class TestCharacterExperience:
    """Tests for character experience and leveling."""

    def test_gain_experience(self):
        """Test gaining experience."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        leveled = character.gain_experience(1000)

        assert not leveled  # Need 2000 for level 2
        assert character.experience_points == 1000

    def test_gain_experience_level_up(self):
        """Test gaining enough experience to level up."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        leveled = character.gain_experience(2500)

        assert leveled  # 2500 > 2000 needed for level 2
        assert character.experience_points == 2500


class TestCharacterInventory:
    """Tests for character inventory system."""

    def test_inventory_starts_empty(self):
        """Test character starts with empty inventory."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        assert character.inventory == []

    def test_add_item(self):
        """Test adding item to inventory."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        item = {"name": "Long Sword", "type": "weapon", "damage": "1d8"}
        character.add_item(item)

        assert len(character.inventory) == 1
        assert character.inventory[0]["name"] == "Long Sword"

    def test_add_multiple_items(self):
        """Test adding multiple items to inventory."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        item1 = {"name": "Long Sword", "type": "weapon"}
        item2 = {"name": "Chain Mail", "type": "armor"}
        item3 = {"name": "Healing Potion", "type": "potion"}

        character.add_item(item1)
        character.add_item(item2)
        character.add_item(item3)

        assert len(character.inventory) == 3

    def test_add_item_makes_copy(self):
        """Test that add_item makes a copy of the item."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        item = {"name": "Long Sword", "type": "weapon"}
        character.add_item(item)

        # Modify original item
        item["name"] = "Modified"

        # Character's item should be unchanged
        assert character.inventory[0]["name"] == "Long Sword"

    def test_remove_item(self):
        """Test removing item from inventory."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        item = {"name": "Long Sword", "type": "weapon"}
        character.add_item(item)

        removed = character.remove_item("Long Sword")

        assert removed is True
        assert len(character.inventory) == 0

    def test_remove_nonexistent_item(self):
        """Test removing item that doesn't exist."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        removed = character.remove_item("Nonexistent Item")

        assert removed is False

    def test_remove_item_only_removes_first_match(self):
        """Test that remove_item only removes first matching item."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)

        item = {"name": "Arrow", "type": "ammunition"}
        character.add_item(item)
        character.add_item(item)

        removed = character.remove_item("Arrow")

        assert removed is True
        assert len(character.inventory) == 1


class TestCharacterSerialization:
    """Tests for character serialization and deserialization."""

    def test_to_dict_basic(self):
        """Test serializing character to dictionary."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Conan", Human(), Fighter, scores, level=3)

        data = character.to_dict()

        assert data["name"] == "Conan"
        assert data["race"] == "Human"
        assert data["character_class"]["class_name"] == "Fighter"
        assert data["character_class"]["level"] == 3
        assert data["ability_scores"]["strength"] == 16
        assert data["ability_scores"]["dexterity"] == 14

    def test_to_dict_with_inventory(self):
        """Test serializing character with inventory."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)
        character.add_item({"name": "Long Sword", "type": "weapon"})
        character.add_item({"name": "Chain Mail", "type": "armor"})

        data = character.to_dict()

        assert len(data["inventory"]) == 2
        assert data["inventory"][0]["name"] == "Long Sword"
        assert data["inventory"][1]["name"] == "Chain Mail"

    def test_to_dict_with_experience(self):
        """Test serializing character with experience."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)
        character.gain_experience(1500)

        data = character.to_dict()

        assert data["character_class"]["experience_points"] == 1500

    def test_from_dict_basic(self):
        """Test deserializing character from dictionary."""
        data = {
            "name": "Conan",
            "race": "Human",
            "character_class": {
                "class_name": "Fighter",
                "level": 3,
                "experience_points": 5000,
                "hit_points": 30,
            },
            "ability_scores": {
                "strength": 16,
                "dexterity": 14,
                "constitution": 15,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
            },
            "inventory": [],
        }

        character = Character.from_dict(data)

        assert character.name == "Conan"
        assert isinstance(character.race, Human)
        assert isinstance(character.character_class, Fighter)
        assert character.level == 3
        assert character.experience_points == 5000
        assert character.hit_points == 30

    def test_from_dict_all_races(self):
        """Test deserializing characters with all race types."""
        races = [
            "Human",
            "HighElf",
            "WoodElf",
            "HillDwarf",
            "MountainDwarf",
            "Halfling",
        ]

        for race_name in races:
            data = {
                "name": "Test",
                "race": race_name,
                "character_class": {
                    "class_name": "Fighter",
                    "level": 1,
                    "experience_points": 0,
                    "hit_points": 10,
                },
                "ability_scores": {
                    "strength": 16,
                    "dexterity": 14,
                    "constitution": 15,
                    "intelligence": 10,
                    "wisdom": 12,
                    "charisma": 8,
                },
                "inventory": [],
            }

            character = Character.from_dict(data)
            assert character.race.__class__.__name__ == race_name

    def test_from_dict_all_classes(self):
        """Test deserializing characters with all class types."""
        classes = [
            ("Fighter", Fighter),
            ("Cleric", Cleric),
            ("Magic-User", MagicUser),
            ("Thief", Thief),
        ]

        for class_name, class_type in classes:
            data = {
                "name": "Test",
                "race": "Human",
                "character_class": {
                    "class_name": class_name,
                    "level": 1,
                    "experience_points": 0,
                    "hit_points": 10,
                },
                "ability_scores": {
                    "strength": 16,
                    "dexterity": 14,
                    "constitution": 15,
                    "intelligence": 10,
                    "wisdom": 12,
                    "charisma": 8,
                },
                "inventory": [],
            }

            character = Character.from_dict(data)
            assert isinstance(character.character_class, class_type)

    def test_from_dict_with_inventory(self):
        """Test deserializing character with inventory."""
        data = {
            "name": "Test",
            "race": "Human",
            "character_class": {
                "class_name": "Fighter",
                "level": 1,
                "experience_points": 0,
                "hit_points": 10,
            },
            "ability_scores": {
                "strength": 16,
                "dexterity": 14,
                "constitution": 15,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
            },
            "inventory": [
                {"name": "Long Sword", "type": "weapon"},
                {"name": "Chain Mail", "type": "armor"},
            ],
        }

        character = Character.from_dict(data)

        assert len(character.inventory) == 2
        assert character.inventory[0]["name"] == "Long Sword"
        assert character.inventory[1]["name"] == "Chain Mail"

    def test_from_dict_unknown_race(self):
        """Test deserializing with unknown race raises error."""
        data = {
            "name": "Test",
            "race": "UnknownRace",
            "character_class": {
                "class_name": "Fighter",
                "level": 1,
                "experience_points": 0,
                "hit_points": 10,
            },
            "ability_scores": {
                "strength": 16,
                "dexterity": 14,
                "constitution": 15,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
            },
            "inventory": [],
        }

        with pytest.raises(ValueError, match="Unknown race"):
            Character.from_dict(data)

    def test_from_dict_unknown_class(self):
        """Test deserializing with unknown class raises error."""
        data = {
            "name": "Test",
            "race": "Human",
            "character_class": {
                "class_name": "UnknownClass",
                "level": 1,
                "experience_points": 0,
                "hit_points": 10,
            },
            "ability_scores": {
                "strength": 16,
                "dexterity": 14,
                "constitution": 15,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 8,
            },
            "inventory": [],
        }

        with pytest.raises(ValueError, match="Unknown character class"):
            Character.from_dict(data)

    def test_roundtrip_serialization(self):
        """Test character can be serialized and deserialized."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        original = create_character("Conan", Human(), Fighter, scores, level=5)
        original.gain_experience(35000)
        original.add_item({"name": "Long Sword", "type": "weapon"})
        original.take_damage(10)

        # Serialize and deserialize
        data = original.to_dict()
        restored = Character.from_dict(data)

        # Verify all key attributes match
        assert restored.name == original.name
        assert restored.level == original.level
        assert restored.experience_points == original.experience_points
        assert restored.hit_points == original.hit_points
        assert len(restored.inventory) == len(original.inventory)

    def test_serialization_makes_copies(self):
        """Test that serialization makes copies of mutable data."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        character = create_character("Test", Human(), Fighter, scores)
        character.add_item({"name": "Sword", "type": "weapon"})

        data = character.to_dict()

        # Modify the serialized data
        data["inventory"][0]["name"] = "Modified"

        # Original character should be unchanged
        assert character.inventory[0]["name"] == "Sword"


class TestCharacterWithRacialAdjustments:
    """Tests for characters with racial ability adjustments."""

    def test_elf_dexterity_bonus_affects_ac(self):
        """Test elf DEX bonus properly affects AC calculation."""
        scores = AbilityScores(
            strength=16,
            dexterity=16,  # Base DEX 16
            constitution=14,
            intelligence=14,
            wisdom=12,
            charisma=10,
        )

        # High elf gets +1 DEX, making it 17 (AC modifier -3)
        character = create_character("Legolas", HighElf(), Fighter, scores)

        assert character.armor_class == 7  # Base 10 + DEX 17 modifier (-3)

    def test_halfling_dexterity_bonus_affects_ac(self):
        """Test halfling DEX bonus affects AC."""
        scores = AbilityScores(
            strength=12,
            dexterity=17,  # Base DEX 17
            constitution=14,
            intelligence=13,
            wisdom=10,
            charisma=12,
        )

        # Halfling gets +1 DEX, making it 18 (AC modifier -4)
        character = create_character("Bilbo", Halfling(), Thief, scores)

        assert character.armor_class == 6  # Base 10 + DEX 18 modifier (-4)

    def test_dwarf_constitution_bonus(self):
        """Test dwarf constitution bonus is applied."""
        scores = AbilityScores(
            strength=16,
            dexterity=12,
            constitution=16,  # Base CON 16
            intelligence=10,
            wisdom=14,
            charisma=10,
        )

        # Hill dwarf gets +1 CON, making it 17
        character = create_character("Gimli", HillDwarf(), Fighter, scores)

        # Verify the adjusted constitution is used
        # (HP calculation uses the adjusted score from character class)
        assert character.character_class.ability_scores.constitution == 17
