"""Unit tests for the character_classes module.

These tests verify that the character_classes module correctly:
- Creates character instances for Fighter, Cleric, Magic-User, and Thief
- Calculates THAC0 progression for each class
- Calculates hit points with Constitution modifiers
- Handles experience point requirements and leveling
- Enforces class restrictions (armor, weapons)
- Supports multi-class and dual-class characters
- Uses canonical AD&D 1E values
"""

import pytest

from src.rules.abilities import AbilityScores
from src.rules.character_classes import (
    ArmorType,
    Cleric,
    DualClassCharacter,
    Fighter,
    MagicUser,
    MultiClassCharacter,
    Thief,
    WeaponType,
    calculate_hp,
)
from src.utils.dice import DiceRoller


class TestCalculateHP:
    """Tests for the calculate_hp function."""

    def test_calculate_hp_level_1_no_modifier(self):
        """Test HP calculation for level 1 with no CON modifier."""
        roller = DiceRoller(seed=12345)
        hp = calculate_hp(10, 1, 0, roller=roller)
        assert hp >= 1 and hp <= 10

    def test_calculate_hp_with_positive_modifier(self):
        """Test HP calculation with positive CON modifier."""
        # Fixed rolls for deterministic testing
        fixed_rolls = [5, 6, 4]
        hp = calculate_hp(8, 3, 2, fixed_rolls=fixed_rolls)
        # (5+2) + (6+2) + (4+2) = 7 + 8 + 6 = 21
        assert hp == 21

    def test_calculate_hp_with_negative_modifier_minimum_1(self):
        """Test HP calculation enforces minimum 1 HP per level."""
        # Roll of 1 with -2 modifier should give 1 HP (not -1)
        fixed_rolls = [1, 1, 1]
        hp = calculate_hp(4, 3, -2, fixed_rolls=fixed_rolls)
        # Each level: max(1, 1-2) = 1
        assert hp == 3

    def test_calculate_hp_fighter_d10(self):
        """Test HP for fighter with d10 hit die."""
        fixed_rolls = [10, 8, 7, 6, 9]
        hp = calculate_hp(10, 5, 1, fixed_rolls=fixed_rolls)
        # (10+1) + (8+1) + (7+1) + (6+1) + (9+1) = 11+9+8+7+10 = 45
        assert hp == 45

    def test_calculate_hp_magic_user_d4(self):
        """Test HP for magic-user with d4 hit die."""
        fixed_rolls = [3, 2, 4, 1]
        hp = calculate_hp(4, 4, 0, fixed_rolls=fixed_rolls)
        # 3 + 2 + 4 + 1 = 10
        assert hp == 10

    def test_calculate_hp_invalid_level(self):
        """Test that invalid level raises ValueError."""
        with pytest.raises(ValueError, match="Level must be at least 1"):
            calculate_hp(8, 0, 0)

    def test_calculate_hp_invalid_hit_die(self):
        """Test that invalid hit die raises ValueError."""
        with pytest.raises(ValueError, match="Hit die must have at least 1 side"):
            calculate_hp(0, 5, 0)


class TestFighter:
    """Tests for the Fighter class."""

    def test_create_fighter_level_1(self):
        """Test creating a level 1 fighter."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        fighter = Fighter(name="Conan", ability_scores=scores, level=1)

        assert fighter.name == "Conan"
        assert fighter.class_name == "Fighter"
        assert fighter.level == 1
        assert fighter.hit_die_sides == 10
        assert fighter.thac0 == 20  # Level 1 fighter THAC0
        assert fighter.hit_points > 0

    def test_fighter_thac0_progression(self):
        """Test THAC0 improves every level for fighters."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )

        # Level 1: THAC0 20
        fighter1 = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)
        assert fighter1.thac0 == 20

        # Level 5: THAC0 16
        fighter5 = Fighter(name="Test", ability_scores=scores, level=5, hit_points=50)
        assert fighter5.thac0 == 16

        # Level 10: THAC0 11
        fighter10 = Fighter(
            name="Test", ability_scores=scores, level=10, hit_points=100
        )
        assert fighter10.thac0 == 11

        # Level 20: THAC0 1
        fighter20 = Fighter(
            name="Test", ability_scores=scores, level=20, hit_points=200
        )
        assert fighter20.thac0 == 1

    def test_fighter_can_use_all_armor(self):
        """Test fighters can use all armor types."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)

        assert fighter.can_use_armor(ArmorType.LEATHER)
        assert fighter.can_use_armor(ArmorType.CHAIN_MAIL)
        assert fighter.can_use_armor(ArmorType.PLATE_MAIL)
        assert fighter.can_use_armor(ArmorType.SHIELD)

    def test_fighter_can_use_all_weapons(self):
        """Test fighters can use all weapon types."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)

        assert fighter.can_use_weapon(WeaponType.LONG_SWORD)
        assert fighter.can_use_weapon(WeaponType.TWO_HANDED_SWORD)
        assert fighter.can_use_weapon(WeaponType.LONG_BOW)
        assert fighter.can_use_weapon(WeaponType.BATTLE_AXE)

    def test_fighter_xp_requirements(self):
        """Test fighter XP requirements match AD&D 1E tables."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)

        # Level 2 requires 2000 XP
        assert fighter.get_xp_for_next_level() == 2000

        fighter.level = 5
        # Level 6 requires 32000 XP
        assert fighter.get_xp_for_next_level() == 32000

        fighter.level = 20
        # Max level, no next level
        assert fighter.get_xp_for_next_level() == 0

    def test_fighter_gain_experience(self):
        """Test fighter gaining experience."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)

        # Gain some XP but not enough to level
        leveled_up = fighter.gain_experience(1000)
        assert not leveled_up
        assert fighter.experience_points == 1000

        # Gain enough to level up (total 2500 > 2000 needed)
        leveled_up = fighter.gain_experience(1500)
        assert leveled_up
        assert fighter.experience_points == 2500


class TestCleric:
    """Tests for the Cleric class."""

    def test_create_cleric_level_1(self):
        """Test creating a level 1 cleric."""
        scores = AbilityScores(
            strength=14,
            dexterity=12,
            constitution=15,
            intelligence=10,
            wisdom=16,
            charisma=13,
        )
        cleric = Cleric(name="Friar Tuck", ability_scores=scores, level=1)

        assert cleric.name == "Friar Tuck"
        assert cleric.class_name == "Cleric"
        assert cleric.level == 1
        assert cleric.hit_die_sides == 8
        assert cleric.thac0 == 20  # Level 1 cleric THAC0
        assert cleric.hit_points > 0

    def test_cleric_thac0_progression(self):
        """Test THAC0 improves every 3 levels for clerics."""
        scores = AbilityScores(
            strength=14,
            dexterity=12,
            constitution=15,
            intelligence=10,
            wisdom=16,
            charisma=13,
        )

        # Level 1-3: THAC0 20
        cleric1 = Cleric(name="Test", ability_scores=scores, level=1, hit_points=8)
        assert cleric1.thac0 == 20

        cleric3 = Cleric(name="Test", ability_scores=scores, level=3, hit_points=24)
        assert cleric3.thac0 == 20

        # Level 4-6: THAC0 18
        cleric4 = Cleric(name="Test", ability_scores=scores, level=4, hit_points=32)
        assert cleric4.thac0 == 18

        # Level 10-12: THAC0 14
        cleric10 = Cleric(name="Test", ability_scores=scores, level=10, hit_points=80)
        assert cleric10.thac0 == 14

    def test_cleric_armor_restrictions(self):
        """Test clerics can use all armor."""
        scores = AbilityScores(
            strength=14,
            dexterity=12,
            constitution=15,
            intelligence=10,
            wisdom=16,
            charisma=13,
        )
        cleric = Cleric(name="Test", ability_scores=scores, level=1, hit_points=8)

        assert cleric.can_use_armor(ArmorType.CHAIN_MAIL)
        assert cleric.can_use_armor(ArmorType.PLATE_MAIL)
        assert cleric.can_use_armor(ArmorType.SHIELD)

    def test_cleric_weapon_restrictions(self):
        """Test clerics can only use blunt weapons."""
        scores = AbilityScores(
            strength=14,
            dexterity=12,
            constitution=15,
            intelligence=10,
            wisdom=16,
            charisma=13,
        )
        cleric = Cleric(name="Test", ability_scores=scores, level=1, hit_points=8)

        # Can use blunt weapons
        assert cleric.can_use_weapon(WeaponType.MACE)
        assert cleric.can_use_weapon(WeaponType.FLAIL)
        assert cleric.can_use_weapon(WeaponType.WAR_HAMMER)
        assert cleric.can_use_weapon(WeaponType.STAFF)

        # Cannot use edged weapons
        assert not cleric.can_use_weapon(WeaponType.LONG_SWORD)
        assert not cleric.can_use_weapon(WeaponType.DAGGER)
        assert not cleric.can_use_weapon(WeaponType.AXE)

    def test_cleric_xp_requirements(self):
        """Test cleric XP requirements match AD&D 1E tables."""
        scores = AbilityScores(
            strength=14,
            dexterity=12,
            constitution=15,
            intelligence=10,
            wisdom=16,
            charisma=13,
        )
        cleric = Cleric(name="Test", ability_scores=scores, level=1, hit_points=8)

        # Level 2 requires 1500 XP
        assert cleric.get_xp_for_next_level() == 1500

        cleric.level = 5
        # Level 6 requires 27500 XP
        assert cleric.get_xp_for_next_level() == 27500


class TestMagicUser:
    """Tests for the Magic-User class."""

    def test_create_magic_user_level_1(self):
        """Test creating a level 1 magic-user."""
        scores = AbilityScores(
            strength=8,
            dexterity=14,
            constitution=12,
            intelligence=18,
            wisdom=13,
            charisma=10,
        )
        mage = MagicUser(name="Gandalf", ability_scores=scores, level=1)

        assert mage.name == "Gandalf"
        assert mage.class_name == "Magic-User"
        assert mage.level == 1
        assert mage.hit_die_sides == 4
        assert mage.thac0 == 21  # Level 1 magic-user THAC0
        assert mage.hit_points > 0

    def test_magic_user_thac0_progression(self):
        """Test THAC0 improves every 5 levels for magic-users."""
        scores = AbilityScores(
            strength=8,
            dexterity=14,
            constitution=12,
            intelligence=18,
            wisdom=13,
            charisma=10,
        )

        # Level 1-5: THAC0 21
        mage1 = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)
        assert mage1.thac0 == 21

        mage5 = MagicUser(name="Test", ability_scores=scores, level=5, hit_points=20)
        assert mage5.thac0 == 21

        # Level 6-10: THAC0 19
        mage6 = MagicUser(name="Test", ability_scores=scores, level=6, hit_points=24)
        assert mage6.thac0 == 19

        # Level 11-15: THAC0 16
        mage11 = MagicUser(name="Test", ability_scores=scores, level=11, hit_points=44)
        assert mage11.thac0 == 16

    def test_magic_user_armor_restrictions(self):
        """Test magic-users cannot wear armor."""
        scores = AbilityScores(
            strength=8,
            dexterity=14,
            constitution=12,
            intelligence=18,
            wisdom=13,
            charisma=10,
        )
        mage = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)

        assert mage.can_use_armor(ArmorType.NONE)
        assert not mage.can_use_armor(ArmorType.LEATHER)
        assert not mage.can_use_armor(ArmorType.CHAIN_MAIL)
        assert not mage.can_use_armor(ArmorType.SHIELD)

    def test_magic_user_weapon_restrictions(self):
        """Test magic-users have very limited weapon selection."""
        scores = AbilityScores(
            strength=8,
            dexterity=14,
            constitution=12,
            intelligence=18,
            wisdom=13,
            charisma=10,
        )
        mage = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)

        # Can use dagger and staff
        assert mage.can_use_weapon(WeaponType.DAGGER)
        assert mage.can_use_weapon(WeaponType.STAFF)

        # Cannot use most weapons
        assert not mage.can_use_weapon(WeaponType.LONG_SWORD)
        assert not mage.can_use_weapon(WeaponType.MACE)
        assert not mage.can_use_weapon(WeaponType.LONG_BOW)

    def test_magic_user_xp_requirements(self):
        """Test magic-user XP requirements match AD&D 1E tables."""
        scores = AbilityScores(
            strength=8,
            dexterity=14,
            constitution=12,
            intelligence=18,
            wisdom=13,
            charisma=10,
        )
        mage = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)

        # Level 2 requires 2500 XP
        assert mage.get_xp_for_next_level() == 2500

        mage.level = 5
        # Level 6 requires 40000 XP
        assert mage.get_xp_for_next_level() == 40000


class TestThief:
    """Tests for the Thief class."""

    def test_create_thief_level_1(self):
        """Test creating a level 1 thief."""
        scores = AbilityScores(
            strength=12,
            dexterity=18,
            constitution=14,
            intelligence=13,
            wisdom=10,
            charisma=12,
        )
        thief = Thief(name="Bilbo", ability_scores=scores, level=1)

        assert thief.name == "Bilbo"
        assert thief.class_name == "Thief"
        assert thief.level == 1
        assert thief.hit_die_sides == 6
        assert thief.thac0 == 21  # Level 1 thief THAC0
        assert thief.hit_points > 0

    def test_thief_thac0_progression(self):
        """Test THAC0 improves every 4 levels for thieves."""
        scores = AbilityScores(
            strength=12,
            dexterity=18,
            constitution=14,
            intelligence=13,
            wisdom=10,
            charisma=12,
        )

        # Level 1-4: THAC0 21
        thief1 = Thief(name="Test", ability_scores=scores, level=1, hit_points=6)
        assert thief1.thac0 == 21

        thief4 = Thief(name="Test", ability_scores=scores, level=4, hit_points=24)
        assert thief4.thac0 == 21

        # Level 5-8: THAC0 19
        thief5 = Thief(name="Test", ability_scores=scores, level=5, hit_points=30)
        assert thief5.thac0 == 19

        # Level 9-12: THAC0 16
        thief9 = Thief(name="Test", ability_scores=scores, level=9, hit_points=54)
        assert thief9.thac0 == 16

    def test_thief_armor_restrictions(self):
        """Test thieves can only use leather armor."""
        scores = AbilityScores(
            strength=12,
            dexterity=18,
            constitution=14,
            intelligence=13,
            wisdom=10,
            charisma=12,
        )
        thief = Thief(name="Test", ability_scores=scores, level=1, hit_points=6)

        assert thief.can_use_armor(ArmorType.NONE)
        assert thief.can_use_armor(ArmorType.LEATHER)
        assert not thief.can_use_armor(ArmorType.CHAIN_MAIL)
        assert not thief.can_use_armor(ArmorType.PLATE_MAIL)
        assert not thief.can_use_armor(ArmorType.SHIELD)

    def test_thief_weapon_restrictions(self):
        """Test thieves have limited weapon selection."""
        scores = AbilityScores(
            strength=12,
            dexterity=18,
            constitution=14,
            intelligence=13,
            wisdom=10,
            charisma=12,
        )
        thief = Thief(name="Test", ability_scores=scores, level=1, hit_points=6)

        # Can use small/concealable weapons
        assert thief.can_use_weapon(WeaponType.DAGGER)
        assert thief.can_use_weapon(WeaponType.SHORT_SWORD)
        assert thief.can_use_weapon(WeaponType.SHORT_BOW)
        assert thief.can_use_weapon(WeaponType.SLING)

        # Cannot use large weapons
        assert not thief.can_use_weapon(WeaponType.LONG_SWORD)
        assert not thief.can_use_weapon(WeaponType.TWO_HANDED_SWORD)
        assert not thief.can_use_weapon(WeaponType.LONG_BOW)

    def test_thief_xp_requirements(self):
        """Test thief XP requirements match AD&D 1E tables."""
        scores = AbilityScores(
            strength=12,
            dexterity=18,
            constitution=14,
            intelligence=13,
            wisdom=10,
            charisma=12,
        )
        thief = Thief(name="Test", ability_scores=scores, level=1, hit_points=6)

        # Level 2 requires 1250 XP
        assert thief.get_xp_for_next_level() == 1250

        thief.level = 5
        # Level 6 requires 20000 XP
        assert thief.get_xp_for_next_level() == 20000


class TestCharacterValidation:
    """Tests for character validation."""

    def test_invalid_level_too_low(self):
        """Test that level < 1 raises ValueError."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        with pytest.raises(ValueError, match="Level must be between 1 and 20"):
            Fighter(name="Test", ability_scores=scores, level=0)

    def test_invalid_level_too_high(self):
        """Test that level > 20 raises ValueError."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        with pytest.raises(ValueError, match="Level must be between 1 and 20"):
            Fighter(name="Test", ability_scores=scores, level=21)

    def test_negative_experience_gain(self):
        """Test that negative XP gain raises ValueError."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )
        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)

        with pytest.raises(ValueError, match="Cannot gain negative experience"):
            fighter.gain_experience(-100)


class TestMultiClass:
    """Tests for multi-class characters."""

    def test_create_multiclass_character(self):
        """Test creating a multi-class character."""
        scores = AbilityScores(
            strength=16,
            dexterity=16,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )

        # Create a Fighter/Thief multi-class (common for elves)
        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)
        thief = Thief(name="Test", ability_scores=scores, level=1, hit_points=6)

        multi = MultiClassCharacter(
            name="Legolas",
            ability_scores=scores,
            classes=[fighter, thief],
        )

        assert multi.name == "Legolas"
        assert len(multi.classes) == 2
        assert multi.experience_points == 0

    def test_multiclass_experience_division(self):
        """Test that XP is divided among all classes."""
        scores = AbilityScores(
            strength=16,
            dexterity=16,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )

        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)
        thief = Thief(name="Test", ability_scores=scores, level=1, hit_points=6)

        multi = MultiClassCharacter(
            name="Test",
            ability_scores=scores,
            classes=[fighter, thief],
        )

        # Gain 2000 XP, should be divided 1000 to each class
        multi.gain_experience(2000)
        assert multi.experience_points == 2000
        assert fighter.experience_points == 1000
        assert thief.experience_points == 1000

    def test_multiclass_requires_at_least_two_classes(self):
        """Test that multi-class requires at least 2 classes."""
        scores = AbilityScores(
            strength=16,
            dexterity=16,
            constitution=15,
            intelligence=10,
            wisdom=12,
            charisma=8,
        )

        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)

        with pytest.raises(ValueError, match="at least 2 classes"):
            MultiClassCharacter(
                name="Test",
                ability_scores=scores,
                classes=[fighter],
            )

    def test_multiclass_max_three_classes(self):
        """Test that multi-class cannot have more than 3 classes."""
        scores = AbilityScores(
            strength=16,
            dexterity=16,
            constitution=15,
            intelligence=16,
            wisdom=16,
            charisma=8,
        )

        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)
        cleric = Cleric(name="Test", ability_scores=scores, level=1, hit_points=8)
        thief = Thief(name="Test", ability_scores=scores, level=1, hit_points=6)
        mage = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)

        with pytest.raises(ValueError, match="cannot have more than 3 classes"):
            MultiClassCharacter(
                name="Test",
                ability_scores=scores,
                classes=[fighter, cleric, thief, mage],
            )


class TestDualClass:
    """Tests for dual-class characters."""

    def test_create_dualclass_character(self):
        """Test creating a dual-class character."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=16,
            wisdom=12,
            charisma=8,
        )

        # Start as a level 5 fighter, then dual-class to magic-user
        fighter = Fighter(name="Test", ability_scores=scores, level=5, hit_points=50)
        mage = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)

        dual = DualClassCharacter(
            name="Elric",
            ability_scores=scores,
            original_class=fighter,
            new_class=mage,
        )

        assert dual.name == "Elric"
        assert dual.original_class.level == 5
        assert dual.new_class.level == 1
        assert dual.experience_points == 0

    def test_dualclass_experience_to_new_class_only(self):
        """Test that XP only goes to the new class."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=16,
            wisdom=12,
            charisma=8,
        )

        fighter = Fighter(name="Test", ability_scores=scores, level=5, hit_points=50)
        mage = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)

        dual = DualClassCharacter(
            name="Test",
            ability_scores=scores,
            original_class=fighter,
            new_class=mage,
        )

        # Gain 3000 XP, should all go to the new class (mage)
        dual.gain_experience(3000)
        assert dual.experience_points == 3000
        assert mage.experience_points == 3000
        # Fighter should not gain any XP
        assert fighter.experience_points == 0

    def test_dualclass_requires_level_2_original(self):
        """Test that original class must be at least level 2."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=16,
            wisdom=12,
            charisma=8,
        )

        fighter = Fighter(name="Test", ability_scores=scores, level=1, hit_points=10)
        mage = MagicUser(name="Test", ability_scores=scores, level=1, hit_points=4)

        with pytest.raises(ValueError, match="Original class must be at least level 2"):
            DualClassCharacter(
                name="Test",
                ability_scores=scores,
                original_class=fighter,
                new_class=mage,
            )

    def test_dualclass_new_class_must_be_level_1(self):
        """Test that new class must start at level 1."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=15,
            intelligence=16,
            wisdom=12,
            charisma=8,
        )

        fighter = Fighter(name="Test", ability_scores=scores, level=5, hit_points=50)
        mage = MagicUser(name="Test", ability_scores=scores, level=2, hit_points=8)

        with pytest.raises(ValueError, match="New class must start at level 1"):
            DualClassCharacter(
                name="Test",
                ability_scores=scores,
                original_class=fighter,
                new_class=mage,
            )


class TestHPCalculationIntegration:
    """Integration tests for HP calculation with Constitution modifiers."""

    def test_fighter_high_constitution(self):
        """Test fighter with high CON gets HP bonus."""
        scores = AbilityScores(
            strength=16,
            dexterity=14,
            constitution=18,  # +4 HP per level
            intelligence=10,
            wisdom=12,
            charisma=8,
        )

        # Use fixed rolls for deterministic test
        fixed_rolls = [10, 10, 10]
        fighter = Fighter(
            name="Test",
            ability_scores=scores,
            level=3,
            hit_points=calculate_hp(10, 3, 4, fixed_rolls=fixed_rolls),
        )

        # (10+4) + (10+4) + (10+4) = 42
        assert fighter.hit_points == 42

    def test_magic_user_low_constitution(self):
        """Test magic-user with low CON gets HP penalty."""
        scores = AbilityScores(
            strength=8,
            dexterity=14,
            constitution=6,  # -1 HP per level
            intelligence=18,
            wisdom=13,
            charisma=10,
        )

        # Use fixed rolls, ensure minimum 1 HP per level
        fixed_rolls = [2, 1, 3]
        mage = MagicUser(
            name="Test",
            ability_scores=scores,
            level=3,
            hit_points=calculate_hp(4, 3, -1, fixed_rolls=fixed_rolls),
        )

        # (2-1) + max(1, 1-1) + (3-1) = 1 + 1 + 2 = 4
        assert mage.hit_points == 4
