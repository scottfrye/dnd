"""Time system for game time tracking and conversion.

This module provides the TimeSystem class which manages game time,
converts between time units (ticks, rounds, turns, days), and advances time.
"""

import logging

logger = logging.getLogger(__name__)


class TimeSystem:
    """Manages game time and time unit conversions.

    TimeSystem tracks the current game time in ticks and provides methods
    to convert between different time units (ticks, rounds, turns, days)
    and to advance time.

    Time unit definitions (based on AD&D 1E):
    - 1 tick = smallest time unit (1 second)
    - 1 round = 10 ticks (10 seconds, combat round)
    - 1 turn = 10 minutes = 600 ticks
    - 1 day = 24 hours = 86400 ticks

    Attributes:
        current_tick: The current game time in ticks.
    """

    # Time unit constants
    TICKS_PER_ROUND = 10  # 10 seconds per round
    TICKS_PER_TURN = 600  # 10 minutes per turn
    TICKS_PER_HOUR = 3600  # 60 minutes per hour
    TICKS_PER_DAY = 86400  # 24 hours per day

    def __init__(self, starting_tick: int = 0) -> None:
        """Initialize a new TimeSystem.

        Args:
            starting_tick: The initial tick count. Defaults to 0.
        """
        self._current_tick: int = starting_tick
        logger.debug("TimeSystem initialized at tick %d", self._current_tick)

    @property
    def current_tick(self) -> int:
        """Get the current game time in ticks.

        Returns:
            The current tick count.
        """
        return self._current_tick

    def advance(self, ticks: int = 1) -> int:
        """Advance the game time by the specified number of ticks.

        Args:
            ticks: Number of ticks to advance. Defaults to 1.

        Returns:
            The new current tick value after advancing.

        Raises:
            ValueError: If ticks is negative.
        """
        if ticks < 0:
            raise ValueError("Cannot advance time by negative ticks")

        self._current_tick += ticks
        logger.debug("Time advanced by %d ticks to %d", ticks, self._current_tick)
        return self._current_tick

    def ticks_to_rounds(self, ticks: int) -> float:
        """Convert ticks to rounds.

        Args:
            ticks: Number of ticks to convert.

        Returns:
            The equivalent number of rounds (may be fractional).
        """
        return ticks / self.TICKS_PER_ROUND

    def ticks_to_turns(self, ticks: int) -> float:
        """Convert ticks to turns.

        Args:
            ticks: Number of ticks to convert.

        Returns:
            The equivalent number of turns (may be fractional).
        """
        return ticks / self.TICKS_PER_TURN

    def ticks_to_hours(self, ticks: int) -> float:
        """Convert ticks to hours.

        Args:
            ticks: Number of ticks to convert.

        Returns:
            The equivalent number of hours (may be fractional).
        """
        return ticks / self.TICKS_PER_HOUR

    def ticks_to_days(self, ticks: int) -> float:
        """Convert ticks to days.

        Args:
            ticks: Number of ticks to convert.

        Returns:
            The equivalent number of days (may be fractional).
        """
        return ticks / self.TICKS_PER_DAY

    def rounds_to_ticks(self, rounds: int) -> int:
        """Convert rounds to ticks.

        Args:
            rounds: Number of rounds to convert.

        Returns:
            The equivalent number of ticks.
        """
        return rounds * self.TICKS_PER_ROUND

    def turns_to_ticks(self, turns: int) -> int:
        """Convert turns to ticks.

        Args:
            turns: Number of turns to convert.

        Returns:
            The equivalent number of ticks.
        """
        return turns * self.TICKS_PER_TURN

    def hours_to_ticks(self, hours: int) -> int:
        """Convert hours to ticks.

        Args:
            hours: Number of hours to convert.

        Returns:
            The equivalent number of ticks.
        """
        return hours * self.TICKS_PER_HOUR

    def days_to_ticks(self, days: int) -> int:
        """Convert days to ticks.

        Args:
            days: Number of days to convert.

        Returns:
            The equivalent number of ticks.
        """
        return days * self.TICKS_PER_DAY

    def get_time_components(self) -> dict[str, int]:
        """Get the current time broken down into components.

        Returns:
            Dictionary with 'days', 'hours', 'minutes', 'seconds' components.
        """
        total_seconds = self._current_tick
        days = total_seconds // self.TICKS_PER_DAY
        remaining = total_seconds % self.TICKS_PER_DAY

        hours = remaining // self.TICKS_PER_HOUR
        remaining = remaining % self.TICKS_PER_HOUR

        minutes = remaining // 60
        seconds = remaining % 60

        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }
