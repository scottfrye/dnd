"""Unit tests for the TimeSystem class.

These tests verify that the TimeSystem class correctly:
- Tracks game time in ticks
- Converts between time units (ticks, rounds, turns, days)
- Advances time
- Provides time component breakdown
"""

import logging

import pytest

from src.world.time_system import TimeSystem


class TestTimeSystemInitialization:
    """Tests for TimeSystem initialization."""

    def test_default_initialization(self):
        """Test that TimeSystem initializes with tick 0 by default."""
        time_system = TimeSystem()

        assert time_system.current_tick == 0

    def test_initialization_with_starting_tick(self):
        """Test that TimeSystem can be initialized with a specific tick."""
        time_system = TimeSystem(starting_tick=1000)

        assert time_system.current_tick == 1000

    def test_initialization_with_zero_tick(self):
        """Test that TimeSystem can be explicitly initialized at tick 0."""
        time_system = TimeSystem(starting_tick=0)

        assert time_system.current_tick == 0


class TestTimeAdvancement:
    """Tests for time advancement."""

    def test_advance_default_one_tick(self):
        """Test that advance() advances by 1 tick by default."""
        time_system = TimeSystem()

        result = time_system.advance()

        assert result == 1
        assert time_system.current_tick == 1

    def test_advance_multiple_ticks(self):
        """Test advancing by multiple ticks."""
        time_system = TimeSystem()

        result = time_system.advance(10)

        assert result == 10
        assert time_system.current_tick == 10

    def test_advance_returns_new_tick(self):
        """Test that advance() returns the new tick value."""
        time_system = TimeSystem(starting_tick=100)

        result = time_system.advance(50)

        assert result == 150

    def test_multiple_advances_accumulate(self):
        """Test that multiple advance calls accumulate."""
        time_system = TimeSystem()

        time_system.advance(5)
        time_system.advance(10)
        time_system.advance(3)

        assert time_system.current_tick == 18

    def test_advance_negative_ticks_raises_error(self):
        """Test that advancing by negative ticks raises ValueError."""
        time_system = TimeSystem()

        with pytest.raises(ValueError, match="Cannot advance time by negative ticks"):
            time_system.advance(-1)

    def test_advance_zero_ticks(self):
        """Test that advancing by zero ticks is allowed."""
        time_system = TimeSystem(starting_tick=100)

        result = time_system.advance(0)

        assert result == 100
        assert time_system.current_tick == 100


class TestTimeUnitConversions:
    """Tests for converting between time units."""

    def test_ticks_to_rounds(self):
        """Test converting ticks to rounds."""
        time_system = TimeSystem()

        assert time_system.ticks_to_rounds(10) == 1.0
        assert time_system.ticks_to_rounds(20) == 2.0
        assert time_system.ticks_to_rounds(5) == 0.5

    def test_ticks_to_turns(self):
        """Test converting ticks to turns."""
        time_system = TimeSystem()

        assert time_system.ticks_to_turns(600) == 1.0
        assert time_system.ticks_to_turns(1200) == 2.0
        assert time_system.ticks_to_turns(300) == 0.5

    def test_ticks_to_hours(self):
        """Test converting ticks to hours."""
        time_system = TimeSystem()

        assert time_system.ticks_to_hours(3600) == 1.0
        assert time_system.ticks_to_hours(7200) == 2.0
        assert time_system.ticks_to_hours(1800) == 0.5

    def test_ticks_to_days(self):
        """Test converting ticks to days."""
        time_system = TimeSystem()

        assert time_system.ticks_to_days(86400) == 1.0
        assert time_system.ticks_to_days(172800) == 2.0
        assert time_system.ticks_to_days(43200) == 0.5

    def test_rounds_to_ticks(self):
        """Test converting rounds to ticks."""
        time_system = TimeSystem()

        assert time_system.rounds_to_ticks(1) == 10
        assert time_system.rounds_to_ticks(5) == 50
        assert time_system.rounds_to_ticks(0) == 0

    def test_turns_to_ticks(self):
        """Test converting turns to ticks."""
        time_system = TimeSystem()

        assert time_system.turns_to_ticks(1) == 600
        assert time_system.turns_to_ticks(3) == 1800
        assert time_system.turns_to_ticks(0) == 0

    def test_hours_to_ticks(self):
        """Test converting hours to ticks."""
        time_system = TimeSystem()

        assert time_system.hours_to_ticks(1) == 3600
        assert time_system.hours_to_ticks(2) == 7200
        assert time_system.hours_to_ticks(0) == 0

    def test_days_to_ticks(self):
        """Test converting days to ticks."""
        time_system = TimeSystem()

        assert time_system.days_to_ticks(1) == 86400
        assert time_system.days_to_ticks(3) == 259200
        assert time_system.days_to_ticks(0) == 0


class TestTimeConstants:
    """Tests for time unit constants."""

    def test_ticks_per_round_constant(self):
        """Test that TICKS_PER_ROUND is 10."""
        assert TimeSystem.TICKS_PER_ROUND == 10

    def test_ticks_per_turn_constant(self):
        """Test that TICKS_PER_TURN is 600."""
        assert TimeSystem.TICKS_PER_TURN == 600

    def test_ticks_per_hour_constant(self):
        """Test that TICKS_PER_HOUR is 3600."""
        assert TimeSystem.TICKS_PER_HOUR == 3600

    def test_ticks_per_day_constant(self):
        """Test that TICKS_PER_DAY is 86400."""
        assert TimeSystem.TICKS_PER_DAY == 86400


class TestTimeComponents:
    """Tests for time component breakdown."""

    def test_get_time_components_at_zero(self):
        """Test time components at tick 0."""
        time_system = TimeSystem()

        components = time_system.get_time_components()

        assert components == {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}

    def test_get_time_components_one_day(self):
        """Test time components after one day."""
        time_system = TimeSystem(starting_tick=86400)

        components = time_system.get_time_components()

        assert components == {"days": 1, "hours": 0, "minutes": 0, "seconds": 0}

    def test_get_time_components_mixed(self):
        """Test time components with mixed values."""
        # 1 day + 2 hours + 30 minutes + 45 seconds = 95445 ticks
        time_system = TimeSystem(starting_tick=95445)

        components = time_system.get_time_components()

        assert components == {"days": 1, "hours": 2, "minutes": 30, "seconds": 45}

    def test_get_time_components_after_advance(self):
        """Test time components after advancing time."""
        time_system = TimeSystem()
        time_system.advance(3665)  # 1 hour, 1 minute, 5 seconds

        components = time_system.get_time_components()

        assert components == {"days": 0, "hours": 1, "minutes": 1, "seconds": 5}


class TestTimeSystemIndependence:
    """Tests to verify TimeSystem instances are independent."""

    def test_multiple_time_systems_are_independent(self):
        """Test that multiple TimeSystem instances don't share state."""
        time_system1 = TimeSystem()
        time_system2 = TimeSystem()

        time_system1.advance(100)

        assert time_system1.current_tick == 100
        assert time_system2.current_tick == 0

    def test_time_systems_with_different_starting_ticks(self):
        """Test TimeSystem instances with different starting ticks."""
        time_system1 = TimeSystem(starting_tick=100)
        time_system2 = TimeSystem(starting_tick=200)

        assert time_system1.current_tick == 100
        assert time_system2.current_tick == 200


class TestTimeSystemLogging:
    """Tests for TimeSystem logging behavior."""

    def test_initialization_logs_debug_message(self, caplog):
        """Test that initialization logs a debug message."""
        with caplog.at_level(logging.DEBUG):
            time_system = TimeSystem(starting_tick=50)

        assert "TimeSystem initialized at tick 50" in caplog.text

    def test_advance_logs_debug_message(self, caplog):
        """Test that advance() logs a debug message."""
        time_system = TimeSystem()

        with caplog.at_level(logging.DEBUG):
            time_system.advance(25)

        assert "Time advanced by 25 ticks to 25" in caplog.text
