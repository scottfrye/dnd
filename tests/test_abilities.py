"""Unit tests for the abilities module.

These tests verify that the abilities module correctly:
- Stores ability scores (STR, DEX, CON, INT, WIS, CHA)
- Computes strength-based hit and damage modifiers
- Computes dexterity-based AC and initiative modifiers
- Computes constitution-based HP modifiers
- Uses canonical AD&D 1E values
"""

import pytest

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


class TestAbilityScores:
    """Tests for the AbilityScores dataclass."""

    def test_create_ability_scores(self):
        """Test creating a valid AbilityScores instance."""
        scores = AbilityScores(
            strength=15,
            dexterity=12,
            constitution=14,
            intelligence=10,
            wisdom=13,
            charisma=8,
        )

        assert scores.strength == 15
        assert scores.dexterity == 12
        assert scores.constitution == 14
        assert scores.intelligence == 10
        assert scores.wisdom == 13
        assert scores.charisma == 8

    def test_ability_scores_standard_array(self):
        """Test creating scores with typical rolled values (3-18 range)."""
        scores = AbilityScores(
            strength=18,
            dexterity=16,
            constitution=15,
            intelligence=12,
            wisdom=10,
            charisma=8,
        )

        assert 3 <= scores.strength <= 18
        assert 3 <= scores.dexterity <= 18
        assert 3 <= scores.constitution <= 18
        assert 3 <= scores.intelligence <= 18
        assert 3 <= scores.wisdom <= 18
        assert 3 <= scores.charisma <= 18

    def test_ability_scores_minimum_values(self):
        """Test creating scores at minimum value (1)."""
        scores = AbilityScores(
            strength=1,
            dexterity=1,
            constitution=1,
            intelligence=1,
            wisdom=1,
            charisma=1,
        )

        assert scores.strength == 1
        assert scores.dexterity == 1

    def test_ability_scores_invalid_zero_raises_error(self):
        """Test that zero ability score raises ValueError."""
        with pytest.raises(ValueError):
            AbilityScores(
                strength=0,
                dexterity=10,
                constitution=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
            )

    def test_ability_scores_invalid_negative_raises_error(self):
        """Test that negative ability score raises ValueError."""
        with pytest.raises(ValueError):
            AbilityScores(
                strength=10,
                dexterity=-1,
                constitution=10,
                intelligence=10,
                wisdom=10,
                charisma=10,
            )


class TestStrengthModifiers:
    """Tests for strength-based modifiers using canonical AD&D 1E values."""

    def test_strength_3_hit_modifier(self):
        """Test STR 3: -3 to hit (AD&D 1E PHB Table I)."""
        assert get_strength_hit_modifier(3) == -3

    def test_strength_3_damage_modifier(self):
        """Test STR 3: -1 to damage (AD&D 1E PHB Table I)."""
        assert get_strength_damage_modifier(3) == -1

    def test_strength_10_hit_modifier(self):
        """Test STR 10: no modifier to hit (AD&D 1E PHB Table I)."""
        assert get_strength_hit_modifier(10) == 0

    def test_strength_10_damage_modifier(self):
        """Test STR 10: no modifier to damage (AD&D 1E PHB Table I)."""
        assert get_strength_damage_modifier(10) == 0

    def test_strength_16_damage_modifier(self):
        """Test STR 16: +1 to damage (AD&D 1E PHB Table I)."""
        assert get_strength_damage_modifier(16) == 1

    def test_strength_17_hit_modifier(self):
        """Test STR 17: +1 to hit (AD&D 1E PHB Table I)."""
        assert get_strength_hit_modifier(17) == 1

    def test_strength_18_modifiers(self):
        """Test STR 18: +1 to hit, +2 to damage (AD&D 1E PHB Table I)."""
        hit, damage = get_strength_modifiers(18)
        assert hit == 1
        assert damage == 2

    def test_strength_low_modifiers_tuple(self):
        """Test combined strength modifiers for low STR."""
        hit, damage = get_strength_modifiers(6)
        assert hit == -1
        assert damage == 0

    def test_strength_invalid_zero_raises_error(self):
        """Test that STR 0 raises ValueError."""
        with pytest.raises(ValueError):
            get_strength_hit_modifier(0)

    def test_strength_invalid_negative_raises_error(self):
        """Test that negative STR raises ValueError."""
        with pytest.raises(ValueError):
            get_strength_damage_modifier(-5)


class TestDexterityModifiers:
    """Tests for dexterity-based modifiers using canonical AD&D 1E values."""

    def test_dexterity_3_ac_modifier(self):
        """Test DEX 3: +4 to AC (worse in AD&D) (AD&D 1E PHB Table II)."""
        assert get_dexterity_ac_modifier(3) == 4

    def test_dexterity_3_initiative_modifier(self):
        """Test DEX 3: -3 to initiative/reaction (AD&D 1E PHB Table II)."""
        assert get_dexterity_initiative_modifier(3) == -3

    def test_dexterity_10_ac_modifier(self):
        """Test DEX 10: no AC modifier (AD&D 1E PHB Table II)."""
        assert get_dexterity_ac_modifier(10) == 0

    def test_dexterity_10_initiative_modifier(self):
        """Test DEX 10: no initiative modifier (AD&D 1E PHB Table II)."""
        assert get_dexterity_initiative_modifier(10) == 0

    def test_dexterity_15_ac_modifier(self):
        """Test DEX 15: -1 to AC (better in AD&D) (AD&D 1E PHB Table II)."""
        assert get_dexterity_ac_modifier(15) == -1

    def test_dexterity_16_initiative_modifier(self):
        """Test DEX 16: +1 to initiative (AD&D 1E PHB Table II)."""
        assert get_dexterity_initiative_modifier(16) == 1

    def test_dexterity_18_modifiers(self):
        """Test DEX 18: +2 initiative, -4 AC (AD&D 1E PHB Table II)."""
        initiative, ac = get_dexterity_modifiers(18)
        assert initiative == 2
        assert ac == -4

    def test_dexterity_17_ac_modifier(self):
        """Test DEX 17: -3 to AC (AD&D 1E PHB Table II)."""
        assert get_dexterity_ac_modifier(17) == -3

    def test_dexterity_invalid_zero_raises_error(self):
        """Test that DEX 0 raises ValueError."""
        with pytest.raises(ValueError):
            get_dexterity_ac_modifier(0)

    def test_dexterity_invalid_negative_raises_error(self):
        """Test that negative DEX raises ValueError."""
        with pytest.raises(ValueError):
            get_dexterity_initiative_modifier(-1)


class TestConstitutionModifiers:
    """Tests for constitution-based HP modifiers using canonical AD&D 1E values."""

    def test_constitution_3_hp_modifier(self):
        """Test CON 3: -2 HP per level (AD&D 1E PHB Table III)."""
        assert get_constitution_hp_modifier(3) == -2

    def test_constitution_7_hp_modifier(self):
        """Test CON 7: no HP modifier (AD&D 1E PHB Table III)."""
        assert get_constitution_hp_modifier(7) == 0

    def test_constitution_10_hp_modifier(self):
        """Test CON 10: no HP modifier (AD&D 1E PHB Table III)."""
        assert get_constitution_hp_modifier(10) == 0

    def test_constitution_15_hp_modifier(self):
        """Test CON 15: +1 HP per level (AD&D 1E PHB Table III)."""
        assert get_constitution_hp_modifier(15) == 1

    def test_constitution_16_hp_modifier(self):
        """Test CON 16: +2 HP per level (AD&D 1E PHB Table III)."""
        assert get_constitution_hp_modifier(16) == 2

    def test_constitution_17_hp_modifier(self):
        """Test CON 17: +2 HP per level for non-fighters (AD&D 1E PHB Table III)."""
        # Note: Fighters get +3 at CON 17, but base modifier is +2
        assert get_constitution_hp_modifier(17) == 2

    def test_constitution_18_hp_modifier(self):
        """Test CON 18: +2 HP per level for non-fighters (AD&D 1E PHB Table III)."""
        # Note: Fighters get +4 at CON 18, but base modifier is +2
        assert get_constitution_hp_modifier(18) == 2

    def test_constitution_1_hp_modifier(self):
        """Test CON 1: -3 HP per level (AD&D 1E PHB Table III)."""
        assert get_constitution_hp_modifier(1) == -3

    def test_constitution_invalid_zero_raises_error(self):
        """Test that CON 0 raises ValueError."""
        with pytest.raises(ValueError):
            get_constitution_hp_modifier(0)

    def test_constitution_invalid_negative_raises_error(self):
        """Test that negative CON raises ValueError."""
        with pytest.raises(ValueError):
            get_constitution_hp_modifier(-3)


class TestHighAbilityScores:
    """Tests for ability scores above 18 (monsters/magic)."""

    def test_strength_19_plus_hit_modifier(self):
        """Test STR 19: +3 to hit (AD&D 1E)."""
        assert get_strength_hit_modifier(19) == 3

    def test_strength_19_plus_damage_modifier(self):
        """Test STR 19: +7 to damage (AD&D 1E)."""
        assert get_strength_damage_modifier(19) == 7

    def test_strength_above_25_uses_max(self):
        """Test that STR above 25 uses the value for 25."""
        assert get_strength_hit_modifier(30) == get_strength_hit_modifier(25)
        assert get_strength_damage_modifier(30) == get_strength_damage_modifier(25)

    def test_dexterity_above_25_uses_max(self):
        """Test that DEX above 25 uses the value for 25."""
        assert get_dexterity_ac_modifier(30) == get_dexterity_ac_modifier(25)
        assert (
            get_dexterity_initiative_modifier(30)
            == get_dexterity_initiative_modifier(25)
        )

    def test_constitution_above_25_uses_max(self):
        """Test that CON above 25 uses the value for 25."""
        assert get_constitution_hp_modifier(30) == get_constitution_hp_modifier(25)
