"""Unit tests for the combat_system module.

These tests verify that the combat_system module correctly:
- Calculates THAC0 values for different classes and levels
- Resolves attacks using THAC0 mechanics
- Handles natural 20 (critical hit) and natural 1 (critical miss)
- Uses deterministic rolls for testing
"""

import pytest

from src.rules.combat_system import (
    AttackResult,
    CombatStats,
    calculate_target_number,
    get_thac0,
    resolve_attack,
    resolve_attack_simple,
)
from src.utils.dice import DiceRoller


class TestCombatStats:
    """Tests for the CombatStats dataclass."""

    def test_create_combat_stats_default(self):
        """Test creating CombatStats with default values."""
        stats = CombatStats()
        assert stats.thac0 == 20
        assert stats.armor_class == 10
        assert stats.hit_modifier == 0
        assert stats.damage_modifier == 0

    def test_create_combat_stats_custom(self):
        """Test creating CombatStats with custom values."""
        stats = CombatStats(
            thac0=15,
            armor_class=2,
            hit_modifier=3,
            damage_modifier=2,
        )
        assert stats.thac0 == 15
        assert stats.armor_class == 2
        assert stats.hit_modifier == 3
        assert stats.damage_modifier == 2

    def test_combat_stats_negative_ac(self):
        """Test creating CombatStats with negative AC (very good armor)."""
        stats = CombatStats(armor_class=-5)
        assert stats.armor_class == -5

    def test_combat_stats_negative_thac0(self):
        """Test creating CombatStats with negative THAC0 (very powerful)."""
        stats = CombatStats(thac0=-2)
        assert stats.thac0 == -2


class TestGetThac0:
    """Tests for THAC0 calculation by class and level."""

    def test_fighter_level_1_thac0(self):
        """Test Fighter level 1 has THAC0 of 20."""
        assert get_thac0(1, "fighter") == 20

    def test_fighter_level_10_thac0(self):
        """Test Fighter level 10 has THAC0 of 11."""
        assert get_thac0(10, "fighter") == 11

    def test_fighter_level_20_thac0(self):
        """Test Fighter level 20 has THAC0 of 1."""
        assert get_thac0(20, "fighter") == 1

    def test_fighter_level_0_thac0(self):
        """Test Fighter level 0 (normal man) has THAC0 of 21."""
        assert get_thac0(0, "fighter") == 21

    def test_cleric_level_1_thac0(self):
        """Test Cleric level 1 has THAC0 of 20."""
        assert get_thac0(1, "cleric") == 20

    def test_cleric_level_4_thac0(self):
        """Test Cleric level 4 has THAC0 of 18."""
        assert get_thac0(4, "cleric") == 18

    def test_cleric_level_10_thac0(self):
        """Test Cleric level 10 has THAC0 of 14."""
        assert get_thac0(10, "cleric") == 14

    def test_thief_level_1_thac0(self):
        """Test Thief level 1 has THAC0 of 21."""
        assert get_thac0(1, "thief") == 21

    def test_thief_level_5_thac0(self):
        """Test Thief level 5 has THAC0 of 19."""
        assert get_thac0(5, "thief") == 19

    def test_magic_user_level_1_thac0(self):
        """Test Magic-User level 1 has THAC0 of 21."""
        assert get_thac0(1, "magic_user") == 21

    def test_magic_user_level_6_thac0(self):
        """Test Magic-User level 6 has THAC0 of 19."""
        assert get_thac0(6, "magic_user") == 19

    def test_magic_user_level_11_thac0(self):
        """Test Magic-User level 11 has THAC0 of 16."""
        assert get_thac0(11, "magic_user") == 16

    def test_default_class_is_fighter(self):
        """Test that default class group is fighter."""
        assert get_thac0(5) == get_thac0(5, "fighter")

    def test_level_above_20_caps_at_20(self):
        """Test that levels above 20 use level 20 THAC0."""
        assert get_thac0(25, "fighter") == get_thac0(20, "fighter")

    def test_invalid_negative_level_raises_error(self):
        """Test that negative level raises ValueError."""
        with pytest.raises(ValueError):
            get_thac0(-1, "fighter")

    def test_invalid_class_group_raises_error(self):
        """Test that invalid class group raises ValueError."""
        with pytest.raises(ValueError):
            get_thac0(1, "invalid_class")


class TestCalculateTargetNumber:
    """Tests for target number calculation."""

    def test_target_number_thac0_20_ac_10(self):
        """Test target number: THAC0 20, AC 10 -> need 10."""
        assert calculate_target_number(20, 10) == 10

    def test_target_number_thac0_20_ac_0(self):
        """Test target number: THAC0 20, AC 0 -> need 20."""
        assert calculate_target_number(20, 0) == 20

    def test_target_number_thac0_15_ac_5(self):
        """Test target number: THAC0 15, AC 5 -> need 10."""
        assert calculate_target_number(15, 5) == 10

    def test_target_number_negative_ac(self):
        """Test target number with negative AC (good armor)."""
        # THAC0 20, AC -5 -> need 25 (impossible without modifiers)
        assert calculate_target_number(20, -5) == 25

    def test_target_number_high_ac(self):
        """Test target number with high AC (bad armor)."""
        # THAC0 20, AC 15 -> need 5
        assert calculate_target_number(20, 15) == 5


class TestResolveAttack:
    """Tests for attack resolution using THAC0 mechanics."""

    def test_hit_with_exact_roll(self):
        """Test that rolling exactly the target number hits."""
        attacker = CombatStats(thac0=20, hit_modifier=0)
        defender = CombatStats(armor_class=10)

        # Target number is 20 - 10 = 10, roll exactly 10
        result = resolve_attack(attacker, defender, roll=10)

        assert result.hit is True
        assert result.roll == 10
        assert result.target_number == 10
        assert result.total_attack == 10

    def test_miss_with_low_roll(self):
        """Test that rolling below target number misses."""
        attacker = CombatStats(thac0=20, hit_modifier=0)
        defender = CombatStats(armor_class=10)

        # Target number is 10, roll 9
        result = resolve_attack(attacker, defender, roll=9)

        assert result.hit is False
        assert result.roll == 9
        assert result.target_number == 10

    def test_hit_with_modifier(self):
        """Test that hit modifier affects attack success."""
        attacker = CombatStats(thac0=20, hit_modifier=3)
        defender = CombatStats(armor_class=10)

        # Target number is 10, roll 8 + 3 modifier = 11 (hit)
        result = resolve_attack(attacker, defender, roll=8)

        assert result.hit is True
        assert result.roll == 8
        assert result.total_attack == 11

    def test_natural_20_always_hits(self):
        """Test that natural 20 always hits regardless of target number."""
        attacker = CombatStats(thac0=20, hit_modifier=0)
        defender = CombatStats(armor_class=-10)  # Very low AC

        # Target number is 30, but natural 20 always hits
        result = resolve_attack(attacker, defender, roll=20)

        assert result.hit is True
        assert result.critical_hit is True
        assert result.roll == 20

    def test_natural_1_always_misses(self):
        """Test that natural 1 always misses regardless of modifiers."""
        attacker = CombatStats(thac0=5, hit_modifier=10)  # Great attacker
        defender = CombatStats(armor_class=20)  # Terrible armor

        # Target number is -15 (easy hit), but natural 1 always misses
        result = resolve_attack(attacker, defender, roll=1)

        assert result.hit is False
        assert result.critical_miss is True
        assert result.roll == 1

    def test_attack_with_seeded_roller(self):
        """Test deterministic attack resolution with seeded roller."""
        attacker = CombatStats(thac0=20, hit_modifier=0)
        defender = CombatStats(armor_class=10)

        roller = DiceRoller(seed=42)
        result1 = resolve_attack(attacker, defender, roller=roller)

        roller = DiceRoller(seed=42)
        result2 = resolve_attack(attacker, defender, roller=roller)

        assert result1.roll == result2.roll
        assert result1.hit == result2.hit


class TestResolveAttackSimple:
    """Tests for the simplified attack resolution function."""

    def test_simple_hit(self):
        """Test simple attack resolution - hit."""
        hit, roll = resolve_attack_simple(20, 10, roll=15)
        assert hit is True
        assert roll == 15

    def test_simple_miss(self):
        """Test simple attack resolution - miss."""
        hit, roll = resolve_attack_simple(20, 10, roll=5)
        assert hit is False
        assert roll == 5

    def test_simple_with_modifier(self):
        """Test simple attack resolution with hit modifier."""
        # Need 10 to hit, roll 8 + 3 modifier = 11 (hit)
        hit, roll = resolve_attack_simple(20, 10, hit_modifier=3, roll=8)
        assert hit is True
        assert roll == 8

    def test_simple_natural_20(self):
        """Test simple attack resolution - natural 20 always hits."""
        hit, roll = resolve_attack_simple(20, -10, roll=20)  # Target 30
        assert hit is True
        assert roll == 20

    def test_simple_natural_1(self):
        """Test simple attack resolution - natural 1 always misses."""
        hit, roll = resolve_attack_simple(20, 20, roll=1)  # Target 0
        assert hit is False
        assert roll == 1


class TestAttackResult:
    """Tests for the AttackResult dataclass."""

    def test_attack_result_basic(self):
        """Test creating a basic AttackResult."""
        result = AttackResult(
            hit=True,
            roll=15,
            total_attack=17,
            target_number=10,
        )

        assert result.hit is True
        assert result.roll == 15
        assert result.total_attack == 17
        assert result.target_number == 10
        assert result.critical_hit is False
        assert result.critical_miss is False

    def test_attack_result_with_critical_hit(self):
        """Test creating AttackResult with critical hit."""
        result = AttackResult(
            hit=True,
            roll=20,
            total_attack=20,
            target_number=10,
            critical_hit=True,
        )

        assert result.critical_hit is True
        assert result.critical_miss is False

    def test_attack_result_with_critical_miss(self):
        """Test creating AttackResult with critical miss."""
        result = AttackResult(
            hit=False,
            roll=1,
            total_attack=1,
            target_number=10,
            critical_miss=True,
        )

        assert result.critical_miss is True
        assert result.critical_hit is False


class TestDeterministicCombat:
    """Tests verifying deterministic combat resolution with mocked stats."""

    def test_deterministic_hit_scenario(self):
        """Test a fully deterministic hit scenario with specific stats.

        Fighter level 5 (THAC0 16) attacks AC 10 target.
        With +2 strength bonus and roll of 10:
        Total attack = 10 + 2 = 12
        Target number = 16 - 10 = 6
        Result: 12 >= 6 = HIT
        """
        attacker = CombatStats(
            thac0=get_thac0(5, "fighter"),  # THAC0 16
            hit_modifier=2,  # +2 STR bonus
        )
        defender = CombatStats(armor_class=10)

        result = resolve_attack(attacker, defender, roll=10)

        assert attacker.thac0 == 16
        assert result.target_number == 6
        assert result.total_attack == 12
        assert result.hit is True

    def test_deterministic_miss_scenario(self):
        """Test a fully deterministic miss scenario with specific stats.

        Magic-User level 1 (THAC0 21) attacks AC 5 target.
        With no bonuses and roll of 10:
        Total attack = 10
        Target number = 21 - 5 = 16
        Result: 10 < 16 = MISS
        """
        attacker = CombatStats(
            thac0=get_thac0(1, "magic_user"),  # THAC0 21
            hit_modifier=0,
        )
        defender = CombatStats(armor_class=5)

        result = resolve_attack(attacker, defender, roll=10)

        assert attacker.thac0 == 21
        assert result.target_number == 16
        assert result.total_attack == 10
        assert result.hit is False

    def test_deterministic_edge_case_exactly_hits(self):
        """Test edge case where roll exactly matches target number.

        Cleric level 4 (THAC0 18) attacks AC 8 target.
        With roll of 10:
        Target number = 18 - 8 = 10
        Result: 10 >= 10 = HIT (exactly)
        """
        attacker = CombatStats(
            thac0=get_thac0(4, "cleric"),  # THAC0 18
            hit_modifier=0,
        )
        defender = CombatStats(armor_class=8)

        result = resolve_attack(attacker, defender, roll=10)

        assert attacker.thac0 == 18
        assert result.target_number == 10
        assert result.total_attack == 10
        assert result.hit is True

    def test_deterministic_edge_case_just_misses(self):
        """Test edge case where roll is just below target number.

        Thief level 1 (THAC0 21) attacks AC 10 target.
        With roll of 10:
        Target number = 21 - 10 = 11
        Result: 10 < 11 = MISS (just)
        """
        attacker = CombatStats(
            thac0=get_thac0(1, "thief"),  # THAC0 21
            hit_modifier=0,
        )
        defender = CombatStats(armor_class=10)

        result = resolve_attack(attacker, defender, roll=10)

        assert attacker.thac0 == 21
        assert result.target_number == 11
        assert result.total_attack == 10
        assert result.hit is False
