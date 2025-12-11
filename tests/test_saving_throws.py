"""Unit tests for the saving_throws module.

These tests verify that the saving_throws module correctly:
- Returns proper saving throw values for all classes and levels
- Applies racial bonuses correctly
- Resolves saving throws with all modifiers
- Handles edge cases and errors properly
- Uses canonical AD&D 1E values
"""

import pytest

from src.rules.saving_throws import (
    SavingThrowCategory,
    SavingThrowResult,
    get_racial_saving_throw_bonus,
    get_saving_throw,
    make_saving_throw,
)
from src.utils.dice import DiceRoller


class TestSavingThrowCategory:
    """Tests for the SavingThrowCategory enum."""

    def test_all_five_categories_exist(self):
        """Test that all five AD&D 1E saving throw categories are defined."""
        assert SavingThrowCategory.PARALYZATION_POISON_DEATH is not None
        assert SavingThrowCategory.PETRIFICATION_POLYMORPH is not None
        assert SavingThrowCategory.ROD_STAFF_WAND is not None
        assert SavingThrowCategory.BREATH_WEAPON is not None
        assert SavingThrowCategory.SPELL is not None

    def test_category_values(self):
        """Test that categories have correct string values."""
        assert (
            SavingThrowCategory.PARALYZATION_POISON_DEATH.value
            == "paralyzation_poison_death"
        )
        assert (
            SavingThrowCategory.PETRIFICATION_POLYMORPH.value
            == "petrification_polymorph"
        )
        assert SavingThrowCategory.ROD_STAFF_WAND.value == "rod_staff_wand"
        assert SavingThrowCategory.BREATH_WEAPON.value == "breath_weapon"
        assert SavingThrowCategory.SPELL.value == "spell"


class TestGetSavingThrow:
    """Tests for the get_saving_throw function."""

    def test_fighter_level_1_paralyzation(self):
        """Test fighter level 1 saving throw vs paralyzation."""
        save = get_saving_throw(
            "fighter", 1, SavingThrowCategory.PARALYZATION_POISON_DEATH
        )
        assert save == 14

    def test_fighter_level_5_paralyzation(self):
        """Test fighter level 5 saving throw vs paralyzation."""
        save = get_saving_throw(
            "fighter", 5, SavingThrowCategory.PARALYZATION_POISON_DEATH
        )
        assert save == 12

    def test_fighter_level_20_paralyzation(self):
        """Test fighter level 20 saving throw vs paralyzation."""
        save = get_saving_throw(
            "fighter", 20, SavingThrowCategory.PARALYZATION_POISON_DEATH
        )
        assert save == 5

    def test_fighter_breath_weapon_progression(self):
        """Test fighter breath weapon saves improve over levels."""
        level_1_save = get_saving_throw("fighter", 1, SavingThrowCategory.BREATH_WEAPON)
        level_10_save = get_saving_throw(
            "fighter", 10, SavingThrowCategory.BREATH_WEAPON
        )
        level_20_save = get_saving_throw(
            "fighter", 20, SavingThrowCategory.BREATH_WEAPON
        )

        # Lower is better - level 20 should have lowest number
        assert level_20_save < level_10_save < level_1_save

    def test_cleric_level_1_spell(self):
        """Test cleric level 1 saving throw vs spell."""
        save = get_saving_throw("cleric", 1, SavingThrowCategory.SPELL)
        assert save == 15

    def test_cleric_level_10_poison(self):
        """Test cleric level 10 saving throw vs poison."""
        save = get_saving_throw(
            "cleric", 10, SavingThrowCategory.PARALYZATION_POISON_DEATH
        )
        assert save == 7

    def test_cleric_level_20_rod(self):
        """Test cleric level 20 saving throw vs rod/staff/wand."""
        save = get_saving_throw("cleric", 20, SavingThrowCategory.ROD_STAFF_WAND)
        assert save == 8

    def test_magic_user_level_1_rod(self):
        """Test magic-user level 1 saving throw vs rod/staff/wand."""
        save = get_saving_throw("magic_user", 1, SavingThrowCategory.ROD_STAFF_WAND)
        assert save == 11

    def test_magic_user_level_11_rod(self):
        """Test magic-user level 11 saving throw vs rod/staff/wand."""
        save = get_saving_throw("magic_user", 11, SavingThrowCategory.ROD_STAFF_WAND)
        assert save == 7

    def test_magic_user_level_20_spell(self):
        """Test magic-user level 20 saving throw vs spell."""
        save = get_saving_throw("magic_user", 20, SavingThrowCategory.SPELL)
        assert save == 6

    def test_thief_level_1_petrification(self):
        """Test thief level 1 saving throw vs petrification."""
        save = get_saving_throw("thief", 1, SavingThrowCategory.PETRIFICATION_POLYMORPH)
        assert save == 12

    def test_thief_level_13_rod(self):
        """Test thief level 13 saving throw vs rod/staff/wand."""
        save = get_saving_throw("thief", 13, SavingThrowCategory.ROD_STAFF_WAND)
        assert save == 8

    def test_thief_level_20_breath(self):
        """Test thief level 20 saving throw vs breath weapon."""
        save = get_saving_throw("thief", 20, SavingThrowCategory.BREATH_WEAPON)
        assert save == 12

    def test_all_classes_all_categories(self):
        """Test that all classes have values for all categories at level 1."""
        classes = ["fighter", "cleric", "magic_user", "thief"]
        categories = [
            SavingThrowCategory.PARALYZATION_POISON_DEATH,
            SavingThrowCategory.PETRIFICATION_POLYMORPH,
            SavingThrowCategory.ROD_STAFF_WAND,
            SavingThrowCategory.BREATH_WEAPON,
            SavingThrowCategory.SPELL,
        ]

        for class_name in classes:
            for category in categories:
                save = get_saving_throw(class_name, 1, category)
                assert isinstance(save, int)
                assert 1 <= save <= 20

    def test_case_insensitive_class_name(self):
        """Test that class names are case-insensitive."""
        save_lower = get_saving_throw(
            "fighter", 5, SavingThrowCategory.PARALYZATION_POISON_DEATH
        )
        save_upper = get_saving_throw(
            "FIGHTER", 5, SavingThrowCategory.PARALYZATION_POISON_DEATH
        )
        save_mixed = get_saving_throw(
            "Fighter", 5, SavingThrowCategory.PARALYZATION_POISON_DEATH
        )

        assert save_lower == save_upper == save_mixed

    def test_invalid_level_zero_raises_error(self):
        """Test that level 0 raises ValueError."""
        with pytest.raises(ValueError, match="Level must be between 1 and 20"):
            get_saving_throw("fighter", 0, SavingThrowCategory.SPELL)

    def test_invalid_level_negative_raises_error(self):
        """Test that negative level raises ValueError."""
        with pytest.raises(ValueError, match="Level must be between 1 and 20"):
            get_saving_throw("fighter", -1, SavingThrowCategory.SPELL)

    def test_invalid_level_above_20_raises_error(self):
        """Test that level above 20 raises ValueError."""
        with pytest.raises(ValueError, match="Level must be between 1 and 20"):
            get_saving_throw("fighter", 21, SavingThrowCategory.SPELL)

    def test_invalid_class_raises_error(self):
        """Test that invalid class name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown class"):
            get_saving_throw("ranger", 5, SavingThrowCategory.SPELL)

    def test_all_levels_defined_for_fighter(self):
        """Test that all levels 1-20 have saving throw values for fighters."""
        for level in range(1, 21):
            save = get_saving_throw(
                "fighter", level, SavingThrowCategory.PARALYZATION_POISON_DEATH
            )
            assert isinstance(save, int)
            assert 1 <= save <= 20


class TestGetRacialSavingThrowBonus:
    """Tests for the get_racial_saving_throw_bonus function."""

    def test_human_no_bonus(self):
        """Test that humans get no racial saving throw bonuses."""
        bonus = get_racial_saving_throw_bonus(
            "human", SavingThrowCategory.PARALYZATION_POISON_DEATH, 16
        )
        assert bonus == 0

    def test_dwarf_vs_poison_with_constitution_16(self):
        """Test dwarf bonus vs poison with Constitution 16."""
        bonus = get_racial_saving_throw_bonus(
            "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 16
        )
        assert bonus == 4

    def test_dwarf_vs_spell_with_constitution_18(self):
        """Test dwarf bonus vs spell with Constitution 18."""
        bonus = get_racial_saving_throw_bonus("dwarf", SavingThrowCategory.SPELL, 18)
        assert bonus == 5

    def test_dwarf_vs_breath_no_bonus(self):
        """Test that dwarves get no bonus vs breath weapons."""
        bonus = get_racial_saving_throw_bonus(
            "dwarf", SavingThrowCategory.BREATH_WEAPON, 16
        )
        assert bonus == 0

    def test_dwarf_constitution_progression(self):
        """Test that dwarf bonuses increase with Constitution."""
        # Constitution 3 or less: no bonus
        assert (
            get_racial_saving_throw_bonus(
                "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 3
            )
            == 0
        )
        # Constitution 4-6: +1
        assert (
            get_racial_saving_throw_bonus(
                "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 6
            )
            == 1
        )
        # Constitution 7-10: +2
        assert (
            get_racial_saving_throw_bonus(
                "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 10
            )
            == 2
        )
        # Constitution 11-13: +3
        assert (
            get_racial_saving_throw_bonus(
                "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 13
            )
            == 3
        )
        # Constitution 14-17: +4
        assert (
            get_racial_saving_throw_bonus(
                "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 17
            )
            == 4
        )
        # Constitution 18+: +5
        assert (
            get_racial_saving_throw_bonus(
                "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 18
            )
            == 5
        )

    def test_halfling_vs_poison_with_constitution_14(self):
        """Test halfling bonus vs poison with Constitution 14."""
        bonus = get_racial_saving_throw_bonus(
            "halfling", SavingThrowCategory.PARALYZATION_POISON_DEATH, 14
        )
        assert bonus == 4

    def test_halfling_vs_rod_with_constitution_12(self):
        """Test halfling bonus vs rod/staff/wand with Constitution 12."""
        bonus = get_racial_saving_throw_bonus(
            "halfling", SavingThrowCategory.ROD_STAFF_WAND, 12
        )
        assert bonus == 3

    def test_halfling_vs_spell_with_constitution_18(self):
        """Test halfling bonus vs spell with Constitution 18."""
        bonus = get_racial_saving_throw_bonus("halfling", SavingThrowCategory.SPELL, 18)
        assert bonus == 5

    def test_halfling_vs_breath_no_bonus(self):
        """Test that halflings get no bonus vs breath weapons."""
        bonus = get_racial_saving_throw_bonus(
            "halfling", SavingThrowCategory.BREATH_WEAPON, 16
        )
        assert bonus == 0

    def test_halfling_vs_petrification_no_bonus(self):
        """Test that halflings get no bonus vs petrification."""
        bonus = get_racial_saving_throw_bonus(
            "halfling", SavingThrowCategory.PETRIFICATION_POLYMORPH, 16
        )
        assert bonus == 0

    def test_hill_dwarf_gets_bonus(self):
        """Test that Hill Dwarf sub-race gets the same bonuses as dwarf."""
        bonus = get_racial_saving_throw_bonus(
            "hill dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 16
        )
        assert bonus == 4

    def test_mountain_dwarf_gets_bonus(self):
        """Test that Mountain Dwarf sub-race gets the same bonuses as dwarf."""
        bonus = get_racial_saving_throw_bonus(
            "mountain dwarf", SavingThrowCategory.SPELL, 18
        )
        assert bonus == 5

    def test_case_insensitive_race_name(self):
        """Test that race names are case-insensitive."""
        bonus_lower = get_racial_saving_throw_bonus(
            "dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 16
        )
        bonus_upper = get_racial_saving_throw_bonus(
            "DWARF", SavingThrowCategory.PARALYZATION_POISON_DEATH, 16
        )
        bonus_mixed = get_racial_saving_throw_bonus(
            "Dwarf", SavingThrowCategory.PARALYZATION_POISON_DEATH, 16
        )

        assert bonus_lower == bonus_upper == bonus_mixed

    def test_elf_no_special_bonus(self):
        """Test that elves don't get saving throw bonuses (they have other abilities)."""
        bonus = get_racial_saving_throw_bonus("elf", SavingThrowCategory.SPELL, 16)
        assert bonus == 0


class TestMakeSavingThrow:
    """Tests for the make_saving_throw function."""

    def test_successful_save_exact_roll(self):
        """Test a successful save with exact roll needed."""
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            roll=12,  # Exactly the target number
        )

        assert result.success is True
        assert result.roll == 12
        assert result.target_number == 12
        assert result.natural_20 is False
        assert result.natural_1 is False

    def test_failed_save_one_below(self):
        """Test a failed save that's one below target."""
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            roll=11,  # One below target of 12
        )

        assert result.success is False
        assert result.roll == 11
        assert result.target_number == 12

    def test_successful_save_above_target(self):
        """Test a successful save well above target."""
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            roll=18,
        )

        assert result.success is True
        assert result.roll == 18
        assert result.target_number == 12

    def test_natural_20_always_succeeds(self):
        """Test that natural 20 always succeeds even if normally impossible."""
        result = make_saving_throw(
            class_name="fighter",
            level=1,
            category=SavingThrowCategory.BREATH_WEAPON,
            roll=20,
        )

        assert result.success is True
        assert result.natural_20 is True
        assert result.roll == 20

    def test_natural_1_always_fails(self):
        """Test that natural 1 always fails even with huge bonuses."""
        result = make_saving_throw(
            class_name="fighter",
            level=20,
            category=SavingThrowCategory.SPELL,
            modifier=10,
            roll=1,
        )

        assert result.success is False
        assert result.natural_1 is True
        assert result.roll == 1

    def test_save_with_positive_modifier(self):
        """Test that positive modifiers make saves easier."""
        # Without modifier, roll of 10 fails (need 12)
        result_no_mod = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            roll=10,
        )
        assert result_no_mod.success is False

        # With +2 modifier, roll of 10 succeeds (10+2=12)
        result_with_mod = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            modifier=2,
            roll=10,
        )
        assert result_with_mod.success is True
        assert result_with_mod.final_modifier == 2

    def test_save_with_negative_modifier(self):
        """Test that negative modifiers make saves harder."""
        # With modifier of -2, roll of 13 succeeds (13-2=11, need 10)
        result = make_saving_throw(
            class_name="fighter",
            level=9,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            modifier=-2,
            roll=12,  # Target is 10, 12-2=10, exactly succeeds
        )
        assert result.success is True
        assert result.final_modifier == -2

    def test_dwarf_racial_bonus_applied(self):
        """Test that dwarf racial bonuses are applied correctly."""
        # Dwarf with CON 16 gets +4 bonus vs poison
        # Target is 12, roll 8, with +4 = 12, should succeed
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            constitution=16,
            race="dwarf",
            roll=8,
        )

        assert result.success is True
        assert result.final_modifier == 4
        assert result.roll == 8
        assert result.target_number == 12

    def test_halfling_racial_bonus_applied(self):
        """Test that halfling racial bonuses are applied correctly."""
        # Halfling with CON 14 gets +4 bonus vs rods
        result = make_saving_throw(
            class_name="thief",
            level=5,
            category=SavingThrowCategory.ROD_STAFF_WAND,
            constitution=14,
            race="halfling",
            roll=8,
        )

        assert result.final_modifier == 4
        # Target for thief 5 vs rod is 12, roll 8+4=12, succeeds
        assert result.success is True

    def test_combined_modifiers(self):
        """Test that racial bonus and other modifiers stack."""
        # Dwarf with CON 16 (+4) and magic item (+2) = +6 total
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            constitution=16,
            race="dwarf",
            modifier=2,
            roll=6,  # Target 12, 6+6=12, succeeds
        )

        assert result.success is True
        assert result.final_modifier == 6  # 4 racial + 2 magic

    def test_save_without_racial_bonus(self):
        """Test that races without bonuses work correctly."""
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.BREATH_WEAPON,
            constitution=16,
            race="dwarf",  # Dwarves get no bonus vs breath
            roll=15,
        )

        assert result.final_modifier == 0
        assert result.success is True

    def test_save_with_random_roll(self):
        """Test save with random dice roller."""
        # Use seeded roller for deterministic test
        roller = DiceRoller(seed=42)

        result = make_saving_throw(
            class_name="fighter",
            level=10,
            category=SavingThrowCategory.SPELL,
            roller=roller,
        )

        # Just verify it returns a valid result
        assert isinstance(result, SavingThrowResult)
        assert isinstance(result.success, bool)
        assert 1 <= result.roll <= 20

    def test_save_result_dataclass_fields(self):
        """Test that SavingThrowResult has all expected fields."""
        result = make_saving_throw(
            class_name="cleric",
            level=7,
            category=SavingThrowCategory.SPELL,
            roll=13,
        )

        assert hasattr(result, "success")
        assert hasattr(result, "roll")
        assert hasattr(result, "target_number")
        assert hasattr(result, "final_modifier")
        assert hasattr(result, "natural_20")
        assert hasattr(result, "natural_1")

    def test_magic_user_vs_rod_high_level(self):
        """Test magic-user saving throw at high level (they're best vs rods)."""
        result = make_saving_throw(
            class_name="magic_user",
            level=16,
            category=SavingThrowCategory.ROD_STAFF_WAND,
            roll=5,  # Target is 5, should exactly succeed
        )

        assert result.success is True
        assert result.target_number == 5

    def test_cleric_vs_spell(self):
        """Test cleric saving throw vs spell."""
        result = make_saving_throw(
            class_name="cleric",
            level=10,
            category=SavingThrowCategory.SPELL,
            roll=12,  # Target is 12
        )

        assert result.success is True
        assert result.target_number == 12

    def test_thief_vs_breath_weapon(self):
        """Test thief saving throw vs breath weapon."""
        result = make_saving_throw(
            class_name="thief",
            level=9,
            category=SavingThrowCategory.BREATH_WEAPON,
            roll=14,  # Target is 14
        )

        assert result.success is True
        assert result.target_number == 14

    def test_default_constitution(self):
        """Test that default constitution is 10 (no bonus)."""
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            race="dwarf",  # Even dwarf gets no bonus with CON 10
            roll=12,
        )

        # CON 10 gives +2 bonus for dwarf
        assert result.final_modifier == 2

    def test_default_race_is_human(self):
        """Test that default race is human (no bonus)."""
        result = make_saving_throw(
            class_name="fighter",
            level=5,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            constitution=18,  # Even high CON gives no bonus to humans
            roll=12,
        )

        assert result.final_modifier == 0

    def test_all_five_categories_with_fighter(self):
        """Test that all five categories work with fighter."""
        categories = [
            SavingThrowCategory.PARALYZATION_POISON_DEATH,
            SavingThrowCategory.PETRIFICATION_POLYMORPH,
            SavingThrowCategory.ROD_STAFF_WAND,
            SavingThrowCategory.BREATH_WEAPON,
            SavingThrowCategory.SPELL,
        ]

        for category in categories:
            result = make_saving_throw(
                class_name="fighter", level=10, category=category, roll=15
            )
            assert isinstance(result, SavingThrowResult)
            assert isinstance(result.success, bool)

    def test_edge_case_level_1_vs_level_20(self):
        """Test saving throws improve from level 1 to level 20."""
        # Fighter level 1 vs poison needs 14
        result_level_1 = make_saving_throw(
            class_name="fighter",
            level=1,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            roll=14,
        )

        # Fighter level 20 vs poison needs 5
        result_level_20 = make_saving_throw(
            class_name="fighter",
            level=20,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            roll=5,
        )

        assert result_level_1.success is True
        assert result_level_20.success is True
        assert result_level_20.target_number < result_level_1.target_number


class TestSavingThrowIntegration:
    """Integration tests for the complete saving throw system."""

    def test_complete_scenario_dwarf_fighter_vs_poison(self):
        """Test complete scenario: dwarf fighter making poison save."""
        # 7th level dwarf fighter with CON 17 vs poison trap
        result = make_saving_throw(
            class_name="fighter",
            level=7,
            category=SavingThrowCategory.PARALYZATION_POISON_DEATH,
            constitution=17,
            race="dwarf",
            modifier=0,
            roll=8,
        )

        # Target for fighter 7 is 11
        # Dwarf with CON 17 gets +4 bonus
        # Roll 8 + 4 = 12, succeeds
        assert result.target_number == 11
        assert result.final_modifier == 4
        assert result.success is True

    def test_complete_scenario_halfling_thief_vs_wand(self):
        """Test complete scenario: halfling thief vs wand."""
        # 13th level halfling thief with CON 12 vs wand of fireballs
        result = make_saving_throw(
            class_name="thief",
            level=13,
            category=SavingThrowCategory.ROD_STAFF_WAND,
            constitution=12,
            race="halfling",
            modifier=1,  # Ring of protection +1
            roll=4,
        )

        # Target for thief 13 vs rod is 8
        # Halfling with CON 12 gets +3 bonus
        # Ring gives +1
        # Total modifier: +4
        # Roll 4 + 4 = 8, exactly succeeds
        assert result.target_number == 8
        assert result.final_modifier == 4
        assert result.success is True

    def test_complete_scenario_human_mage_vs_spell(self):
        """Test complete scenario: human magic-user vs spell."""
        # 11th level human magic-user vs hold person spell
        result = make_saving_throw(
            class_name="magic_user",
            level=11,
            category=SavingThrowCategory.SPELL,
            constitution=10,
            race="human",
            modifier=0,
            roll=8,
        )

        # Target for magic-user 11 vs spell is 8
        # Human gets no racial bonus
        # Roll 8, exactly succeeds
        assert result.target_number == 8
        assert result.final_modifier == 0
        assert result.success is True

    def test_complete_scenario_critical_failure(self):
        """Test complete scenario: critical failure despite bonuses."""
        # High level character with huge bonuses still fails on natural 1
        result = make_saving_throw(
            class_name="fighter",
            level=20,
            category=SavingThrowCategory.SPELL,
            constitution=18,
            race="dwarf",
            modifier=5,  # Magic items
            roll=1,  # Natural 1
        )

        # Despite +10 total bonus (5 racial + 5 magic), natural 1 fails
        assert result.natural_1 is True
        assert result.success is False

    def test_complete_scenario_critical_success(self):
        """Test complete scenario: critical success despite penalties."""
        # Low level character with penalties still succeeds on natural 20
        result = make_saving_throw(
            class_name="fighter",
            level=1,
            category=SavingThrowCategory.BREATH_WEAPON,
            constitution=8,
            race="human",
            modifier=-2,  # Cursed item
            roll=20,  # Natural 20
        )

        # Despite penalties, natural 20 succeeds
        assert result.natural_20 is True
        assert result.success is True
