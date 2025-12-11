"""Unit tests for the races module.

These tests verify that the races module correctly:
- Creates race instances with proper attributes
- Applies racial ability score adjustments
- Enforces ability score limits (3-18)
- Returns correct level limits by class
- Lists special abilities
- Lists racial languages
- Reports infravision ranges
- Uses canonical AD&D 1E values
"""

from src.rules.abilities import AbilityScores
from src.rules.races import (
    Halfling,
    HighElf,
    HillDwarf,
    Human,
    MountainDwarf,
    RaceInfo,
    WoodElf,
)


class TestHuman:
    """Tests for the Human race."""

    def test_human_has_no_ability_adjustments(self):
        """Test that humans have no ability score adjustments."""
        human = Human()
        info = human.get_race_info()
        assert info.ability_adjustments == {}

    def test_human_has_no_level_limits(self):
        """Test that humans have no level limits."""
        human = Human()
        assert human.get_level_limit("fighter") is None
        assert human.get_level_limit("cleric") is None
        assert human.get_level_limit("magic_user") is None
        assert human.get_level_limit("thief") is None

    def test_human_has_no_special_abilities(self):
        """Test that humans have no special abilities."""
        human = Human()
        assert human.get_special_abilities() == []

    def test_human_speaks_common(self):
        """Test that humans speak Common."""
        human = Human()
        languages = human.get_languages()
        assert "Common" in languages
        assert len(languages) == 1

    def test_human_has_no_infravision(self):
        """Test that humans have no infravision."""
        human = Human()
        assert human.get_infravision_range() == 0

    def test_human_apply_ability_adjustments_unchanged(self):
        """Test that human ability adjustments leave scores unchanged."""
        human = Human()
        original = AbilityScores(
            strength=12,
            dexterity=14,
            constitution=10,
            intelligence=13,
            wisdom=15,
            charisma=8,
        )
        adjusted = human.apply_ability_adjustments(original)
        assert adjusted.strength == 12
        assert adjusted.dexterity == 14
        assert adjusted.constitution == 10
        assert adjusted.intelligence == 13
        assert adjusted.wisdom == 15
        assert adjusted.charisma == 8


class TestHighElf:
    """Tests for the High Elf race."""

    def test_high_elf_ability_adjustments(self):
        """Test high elf +1 DEX, -1 CON adjustments."""
        elf = HighElf()
        info = elf.get_race_info()
        assert info.ability_adjustments["dexterity"] == 1
        assert info.ability_adjustments["constitution"] == -1

    def test_high_elf_apply_ability_adjustments(self):
        """Test applying high elf ability adjustments."""
        elf = HighElf()
        original = AbilityScores(
            strength=12,
            dexterity=14,
            constitution=16,
            intelligence=10,
            wisdom=13,
            charisma=8,
        )
        adjusted = elf.apply_ability_adjustments(original)
        assert adjusted.strength == 12  # Unchanged
        assert adjusted.dexterity == 15  # +1
        assert adjusted.constitution == 15  # -1
        assert adjusted.intelligence == 10  # Unchanged
        assert adjusted.wisdom == 13  # Unchanged
        assert adjusted.charisma == 8  # Unchanged

    def test_high_elf_ability_adjustment_caps_at_18(self):
        """Test that ability adjustments respect the 18 cap."""
        elf = HighElf()
        original = AbilityScores(
            strength=12,
            dexterity=18,
            constitution=16,
            intelligence=10,
            wisdom=13,
            charisma=8,
        )
        adjusted = elf.apply_ability_adjustments(original)
        assert adjusted.dexterity == 18  # Capped at 18

    def test_high_elf_ability_adjustment_min_at_3(self):
        """Test that ability adjustments respect the 3 minimum."""
        elf = HighElf()
        original = AbilityScores(
            strength=12,
            dexterity=14,
            constitution=3,
            intelligence=10,
            wisdom=13,
            charisma=8,
        )
        adjusted = elf.apply_ability_adjustments(original)
        assert adjusted.constitution == 3  # Minimum is 3 (3-1=2, clamped to 3)

    def test_high_elf_level_limits(self):
        """Test high elf level limits for various classes."""
        elf = HighElf()
        assert elf.get_level_limit("fighter") == 7
        assert elf.get_level_limit("cleric") == 7
        assert elf.get_level_limit("magic_user") == 11
        assert elf.get_level_limit("thief") == 10
        assert elf.get_level_limit("ranger") == 8

    def test_high_elf_special_abilities(self):
        """Test that high elves have expected special abilities."""
        elf = HighElf()
        abilities = elf.get_special_abilities()
        assert "90% resistance to sleep and charm spells" in abilities
        assert any("Detect secret doors" in ability for ability in abilities)
        assert any("+1 to hit with bow" in ability for ability in abilities)

    def test_high_elf_languages(self):
        """Test high elf languages."""
        elf = HighElf()
        languages = elf.get_languages()
        assert "Common" in languages
        assert "Elvish" in languages
        assert "Gnome" in languages
        assert "Halfling" in languages

    def test_high_elf_infravision(self):
        """Test that high elves have 60' infravision."""
        elf = HighElf()
        assert elf.get_infravision_range() == 60


class TestWoodElf:
    """Tests for the Wood Elf race."""

    def test_wood_elf_ability_adjustments(self):
        """Test wood elf +1 DEX, -1 CON adjustments."""
        elf = WoodElf()
        info = elf.get_race_info()
        assert info.ability_adjustments["dexterity"] == 1
        assert info.ability_adjustments["constitution"] == -1

    def test_wood_elf_apply_ability_adjustments(self):
        """Test applying wood elf ability adjustments."""
        elf = WoodElf()
        original = AbilityScores(
            strength=12,
            dexterity=14,
            constitution=16,
            intelligence=10,
            wisdom=13,
            charisma=8,
        )
        adjusted = elf.apply_ability_adjustments(original)
        assert adjusted.dexterity == 15  # +1
        assert adjusted.constitution == 15  # -1

    def test_wood_elf_level_limits(self):
        """Test wood elf level limits (different from high elf)."""
        elf = WoodElf()
        assert elf.get_level_limit("fighter") == 7
        assert elf.get_level_limit("cleric") == 7
        assert elf.get_level_limit("magic_user") == 9  # Lower than high elf
        assert elf.get_level_limit("thief") == 11  # Higher than high elf

    def test_wood_elf_special_abilities(self):
        """Test that wood elves have expected special abilities."""
        elf = WoodElf()
        abilities = elf.get_special_abilities()
        assert "90% resistance to sleep and charm spells" in abilities

    def test_wood_elf_languages(self):
        """Test wood elf languages."""
        elf = WoodElf()
        languages = elf.get_languages()
        assert "Common" in languages
        assert "Elvish" in languages

    def test_wood_elf_infravision(self):
        """Test that wood elves have 60' infravision."""
        elf = WoodElf()
        assert elf.get_infravision_range() == 60


class TestHillDwarf:
    """Tests for the Hill Dwarf race."""

    def test_hill_dwarf_ability_adjustments(self):
        """Test hill dwarf +1 CON, -1 CHA adjustments."""
        dwarf = HillDwarf()
        info = dwarf.get_race_info()
        assert info.ability_adjustments["constitution"] == 1
        assert info.ability_adjustments["charisma"] == -1

    def test_hill_dwarf_apply_ability_adjustments(self):
        """Test applying hill dwarf ability adjustments."""
        dwarf = HillDwarf()
        original = AbilityScores(
            strength=16,
            dexterity=10,
            constitution=14,
            intelligence=12,
            wisdom=13,
            charisma=10,
        )
        adjusted = dwarf.apply_ability_adjustments(original)
        assert adjusted.strength == 16  # Unchanged
        assert adjusted.dexterity == 10  # Unchanged
        assert adjusted.constitution == 15  # +1
        assert adjusted.intelligence == 12  # Unchanged
        assert adjusted.wisdom == 13  # Unchanged
        assert adjusted.charisma == 9  # -1

    def test_hill_dwarf_level_limits(self):
        """Test hill dwarf level limits."""
        dwarf = HillDwarf()
        assert dwarf.get_level_limit("fighter") == 9
        assert dwarf.get_level_limit("cleric") == 8
        assert dwarf.get_level_limit("thief") == 9
        assert dwarf.get_level_limit("assassin") == 9

    def test_hill_dwarf_special_abilities(self):
        """Test that hill dwarves have stonework detection abilities."""
        dwarf = HillDwarf()
        abilities = dwarf.get_special_abilities()
        assert any("Detect grade or slope" in ability for ability in abilities)
        assert any("Detect new tunnel" in ability for ability in abilities)
        assert any("Saving throw bonus vs. magic" in ability for ability in abilities)
        assert any("Saving throw bonus vs. poison" in ability for ability in abilities)

    def test_hill_dwarf_languages(self):
        """Test hill dwarf languages."""
        dwarf = HillDwarf()
        languages = dwarf.get_languages()
        assert "Common" in languages
        assert "Dwarvish" in languages
        assert "Gnome" in languages

    def test_hill_dwarf_infravision(self):
        """Test that hill dwarves have 60' infravision."""
        dwarf = HillDwarf()
        assert dwarf.get_infravision_range() == 60


class TestMountainDwarf:
    """Tests for the Mountain Dwarf race."""

    def test_mountain_dwarf_ability_adjustments(self):
        """Test mountain dwarf +1 CON, -1 CHA adjustments."""
        dwarf = MountainDwarf()
        info = dwarf.get_race_info()
        assert info.ability_adjustments["constitution"] == 1
        assert info.ability_adjustments["charisma"] == -1

    def test_mountain_dwarf_apply_ability_adjustments(self):
        """Test applying mountain dwarf ability adjustments."""
        dwarf = MountainDwarf()
        original = AbilityScores(
            strength=16,
            dexterity=10,
            constitution=14,
            intelligence=12,
            wisdom=13,
            charisma=10,
        )
        adjusted = dwarf.apply_ability_adjustments(original)
        assert adjusted.constitution == 15  # +1
        assert adjusted.charisma == 9  # -1

    def test_mountain_dwarf_level_limits(self):
        """Test mountain dwarf level limits (slightly higher fighter limit)."""
        dwarf = MountainDwarf()
        assert dwarf.get_level_limit("fighter") == 10  # Higher than hill dwarf
        assert dwarf.get_level_limit("cleric") == 8
        assert dwarf.get_level_limit("thief") == 9

    def test_mountain_dwarf_special_abilities(self):
        """Test that mountain dwarves have stonework detection abilities."""
        dwarf = MountainDwarf()
        abilities = dwarf.get_special_abilities()
        assert any("Detect grade or slope" in ability for ability in abilities)

    def test_mountain_dwarf_languages(self):
        """Test mountain dwarf languages."""
        dwarf = MountainDwarf()
        languages = dwarf.get_languages()
        assert "Common" in languages
        assert "Dwarvish" in languages

    def test_mountain_dwarf_infravision(self):
        """Test that mountain dwarves have 60' infravision."""
        dwarf = MountainDwarf()
        assert dwarf.get_infravision_range() == 60


class TestHalfling:
    """Tests for the Halfling race."""

    def test_halfling_ability_adjustments(self):
        """Test halfling +1 DEX, -1 STR adjustments."""
        halfling = Halfling()
        info = halfling.get_race_info()
        assert info.ability_adjustments["dexterity"] == 1
        assert info.ability_adjustments["strength"] == -1

    def test_halfling_apply_ability_adjustments(self):
        """Test applying halfling ability adjustments."""
        halfling = Halfling()
        original = AbilityScores(
            strength=12,
            dexterity=14,
            constitution=16,
            intelligence=10,
            wisdom=13,
            charisma=8,
        )
        adjusted = halfling.apply_ability_adjustments(original)
        assert adjusted.strength == 11  # -1
        assert adjusted.dexterity == 15  # +1
        assert adjusted.constitution == 16  # Unchanged
        assert adjusted.intelligence == 10  # Unchanged
        assert adjusted.wisdom == 13  # Unchanged
        assert adjusted.charisma == 8  # Unchanged

    def test_halfling_level_limits(self):
        """Test halfling level limits."""
        halfling = Halfling()
        assert halfling.get_level_limit("fighter") == 6
        assert halfling.get_level_limit("cleric") == 6
        assert halfling.get_level_limit("thief") == 10

    def test_halfling_special_abilities(self):
        """Test that halflings have sling bonuses and stealth abilities."""
        halfling = Halfling()
        abilities = halfling.get_special_abilities()
        assert any("+3 to hit with slings" in ability for ability in abilities)
        assert any("Hide in shadows" in ability for ability in abilities)
        assert any("Saving throw bonus vs. magic" in ability for ability in abilities)

    def test_halfling_languages(self):
        """Test halfling languages."""
        halfling = Halfling()
        languages = halfling.get_languages()
        assert "Common" in languages
        assert "Halfling" in languages
        assert "Dwarvish" in languages

    def test_halfling_has_no_infravision(self):
        """Test that halflings have no infravision."""
        halfling = Halfling()
        assert halfling.get_infravision_range() == 0


class TestRaceInfo:
    """Tests for the RaceInfo dataclass."""

    def test_race_info_creation(self):
        """Test creating a RaceInfo instance."""
        info = RaceInfo(
            name="Test Race",
            ability_adjustments={"strength": 1},
            level_limits={"fighter": 10},
            special_abilities=["Test ability"],
            languages=["Common"],
            infravision_range=60,
        )
        assert info.name == "Test Race"
        assert info.ability_adjustments == {"strength": 1}
        assert info.level_limits == {"fighter": 10}
        assert info.special_abilities == ["Test ability"]
        assert info.languages == ["Common"]
        assert info.infravision_range == 60

    def test_race_info_default_infravision(self):
        """Test that RaceInfo defaults to 0 infravision."""
        info = RaceInfo(
            name="Test Race",
            ability_adjustments={},
            level_limits={},
            special_abilities=[],
            languages=["Common"],
        )
        assert info.infravision_range == 0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_ability_adjustment_at_lower_boundary(self):
        """Test ability adjustments at minimum score (3)."""
        halfling = Halfling()
        original = AbilityScores(
            strength=3,
            dexterity=3,
            constitution=3,
            intelligence=3,
            wisdom=3,
            charisma=3,
        )
        adjusted = halfling.apply_ability_adjustments(original)
        assert adjusted.strength == 3  # 3-1=2, clamped to 3
        assert adjusted.dexterity == 4  # 3+1=4
        assert adjusted.constitution == 3  # Unchanged

    def test_ability_adjustment_at_upper_boundary(self):
        """Test ability adjustments at maximum score (18)."""
        elf = HighElf()
        original = AbilityScores(
            strength=18,
            dexterity=18,
            constitution=18,
            intelligence=18,
            wisdom=18,
            charisma=18,
        )
        adjusted = elf.apply_ability_adjustments(original)
        assert adjusted.dexterity == 18  # 18+1=19, clamped to 18
        assert adjusted.constitution == 17  # 18-1=17
        assert adjusted.strength == 18  # Unchanged

    def test_get_level_limit_for_nonexistent_class(self):
        """Test that getting level limit for unknown class returns None."""
        human = Human()
        assert human.get_level_limit("unknown_class") is None

        elf = HighElf()
        assert elf.get_level_limit("unknown_class") is None

    def test_languages_list_is_copy(self):
        """Test that get_languages returns a copy, not a reference."""
        elf = HighElf()
        languages1 = elf.get_languages()
        languages2 = elf.get_languages()
        languages1.append("Test Language")
        assert "Test Language" not in languages2

    def test_special_abilities_list_is_copy(self):
        """Test that get_special_abilities returns a copy."""
        elf = HighElf()
        abilities1 = elf.get_special_abilities()
        abilities2 = elf.get_special_abilities()
        abilities1.append("Test Ability")
        assert "Test Ability" not in abilities2


class TestMultipleRaceInstances:
    """Tests for creating multiple instances of races."""

    def test_multiple_human_instances(self):
        """Test creating multiple human instances."""
        human1 = Human()
        human2 = Human()
        assert human1.get_race_info().name == human2.get_race_info().name

    def test_multiple_elf_instances(self):
        """Test creating multiple elf instances."""
        elf1 = HighElf()
        elf2 = HighElf()
        assert elf1.get_race_info().name == elf2.get_race_info().name
        assert elf1.get_infravision_range() == elf2.get_infravision_range()

    def test_different_elf_subraces(self):
        """Test that different elf sub-races have different properties."""
        high_elf = HighElf()
        wood_elf = WoodElf()
        assert high_elf.get_level_limit("magic_user") != wood_elf.get_level_limit(
            "magic_user"
        )
        assert high_elf.get_level_limit("thief") != wood_elf.get_level_limit("thief")

    def test_different_dwarf_subraces(self):
        """Test that different dwarf sub-races have different properties."""
        hill_dwarf = HillDwarf()
        mountain_dwarf = MountainDwarf()
        assert hill_dwarf.get_level_limit("fighter") != mountain_dwarf.get_level_limit(
            "fighter"
        )
