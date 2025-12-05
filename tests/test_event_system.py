"""Unit tests for the EventSystem class.

These tests verify that the EventSystem class correctly:
- Schedules events at future ticks
- Dispatches events when tick() is called
- Fires events at the expected time
- Handles multiple events
- Supports event cancellation
"""

import logging

import pytest

from src.world.event_system import EventSystem, ScheduledEvent


class TestEventSystemInitialization:
    """Tests for EventSystem initialization."""

    def test_initialization(self):
        """Test that EventSystem initializes correctly."""
        event_system = EventSystem()

        assert event_system is not None

    def test_no_pending_events_on_init(self):
        """Test that a new EventSystem has no pending events."""
        event_system = EventSystem()

        pending = event_system.get_pending_events()

        assert pending == []


class TestEventScheduling:
    """Tests for scheduling events."""

    def test_schedule_simple_event(self):
        """Test scheduling a simple event."""
        event_system = EventSystem()
        called = []

        def callback():
            called.append(True)

        event_id = event_system.schedule(10, callback)

        assert event_id is not None
        assert isinstance(event_id, str)
        assert len(called) == 0  # Not yet fired

    def test_schedule_event_with_custom_id(self):
        """Test scheduling an event with a custom ID."""
        event_system = EventSystem()

        event_id = event_system.schedule(10, lambda: None, event_id="custom_event")

        assert event_id == "custom_event"

    def test_schedule_event_with_args(self):
        """Test scheduling an event with positional arguments."""
        event_system = EventSystem()
        results = []

        def callback(a, b):
            results.append(a + b)

        event_system.schedule(5, callback, 10, 20)
        event_system.tick(5)

        assert results == [30]

    def test_schedule_event_with_kwargs(self):
        """Test scheduling an event with keyword arguments."""
        event_system = EventSystem()
        results = []

        def callback(x=0, y=0):
            results.append(x * y)

        event_system.schedule(5, callback, x=5, y=3)
        event_system.tick(5)

        assert results == [15]

    def test_schedule_event_with_args_and_kwargs(self):
        """Test scheduling an event with both args and kwargs."""
        event_system = EventSystem()
        results = []

        def callback(a, b, multiplier=1):
            results.append((a + b) * multiplier)

        event_system.schedule(5, callback, 10, 20, multiplier=2)
        event_system.tick(5)

        assert results == [60]

    def test_schedule_event_at_negative_tick_raises_error(self):
        """Test that scheduling at negative tick raises ValueError."""
        event_system = EventSystem()

        with pytest.raises(ValueError, match="Cannot schedule event at negative tick"):
            event_system.schedule(-1, lambda: None)

    def test_schedule_event_at_tick_zero(self):
        """Test scheduling an event at tick 0."""
        event_system = EventSystem()
        called = []

        event_system.schedule(0, lambda: called.append(True))
        event_system.tick(0)

        assert len(called) == 1

    def test_get_pending_events(self):
        """Test getting pending events information."""
        event_system = EventSystem()

        event_system.schedule(10, lambda: None, event_id="event1")
        event_system.schedule(20, lambda: None, event_id="event2")

        pending = event_system.get_pending_events()

        assert len(pending) == 2
        assert any(e["event_id"] == "event1" and e["tick"] == 10 for e in pending)
        assert any(e["event_id"] == "event2" and e["tick"] == 20 for e in pending)


class TestEventDispatching:
    """Tests for event dispatching."""

    def test_tick_fires_event_at_exact_time(self):
        """Test that tick() fires an event at the exact scheduled time."""
        event_system = EventSystem()
        called = []

        event_system.schedule(10, lambda: called.append(True))

        # Before the scheduled time
        event_system.tick(9)
        assert len(called) == 0

        # At the scheduled time
        event_system.tick(10)
        assert len(called) == 1

    def test_tick_fires_overdue_events(self):
        """Test that tick() fires events that are overdue."""
        event_system = EventSystem()
        called = []

        event_system.schedule(5, lambda: called.append(True))

        # Skip past the scheduled time
        event_system.tick(10)
        assert len(called) == 1

    def test_tick_fires_multiple_events(self):
        """Test that tick() fires all events scheduled for that tick."""
        event_system = EventSystem()
        results = []

        event_system.schedule(10, lambda: results.append("a"))
        event_system.schedule(10, lambda: results.append("b"))
        event_system.schedule(10, lambda: results.append("c"))

        event_system.tick(10)

        assert len(results) == 3
        assert "a" in results
        assert "b" in results
        assert "c" in results

    def test_tick_fires_events_in_order_scheduled(self):
        """Test that events scheduled at the same tick fire in order."""
        event_system = EventSystem()
        results = []

        event_system.schedule(10, lambda: results.append(1))
        event_system.schedule(10, lambda: results.append(2))
        event_system.schedule(10, lambda: results.append(3))

        event_system.tick(10)

        assert results == [1, 2, 3]

    def test_tick_fires_events_by_tick_order(self):
        """Test that events fire in tick order when scheduled at different times."""
        event_system = EventSystem()
        results = []

        event_system.schedule(20, lambda: results.append("late"))
        event_system.schedule(10, lambda: results.append("early"))
        event_system.schedule(15, lambda: results.append("middle"))

        event_system.tick(25)

        assert results == ["early", "middle", "late"]

    def test_tick_returns_event_results(self):
        """Test that tick() returns results from fired events."""
        event_system = EventSystem()

        event_system.schedule(5, lambda: 42, event_id="event1")
        event_system.schedule(5, lambda: "hello", event_id="event2")

        results = event_system.tick(5)

        assert len(results) == 2
        assert ("event1", 42) in results
        assert ("event2", "hello") in results

    def test_tick_removes_fired_events(self):
        """Test that fired events are removed from the queue."""
        event_system = EventSystem()

        event_system.schedule(5, lambda: None)

        assert len(event_system.get_pending_events()) == 1

        event_system.tick(5)

        assert len(event_system.get_pending_events()) == 0

    def test_tick_with_no_events_returns_empty_list(self):
        """Test that tick() returns empty list when no events fire."""
        event_system = EventSystem()

        results = event_system.tick(10)

        assert results == []

    def test_tick_with_future_events_returns_empty_list(self):
        """Test that tick() returns empty list when events are in the future."""
        event_system = EventSystem()

        event_system.schedule(20, lambda: None)

        results = event_system.tick(10)

        assert results == []

    def test_event_callback_exception_is_handled(self):
        """Test that exceptions in event callbacks are caught and logged."""
        event_system = EventSystem()

        def failing_callback():
            raise RuntimeError("Test error")

        event_system.schedule(5, failing_callback, event_id="failing_event")

        results = event_system.tick(5)

        assert len(results) == 1
        assert results[0][0] == "failing_event"
        assert isinstance(results[0][1], RuntimeError)


class TestEventCancellation:
    """Tests for cancelling scheduled events."""

    def test_cancel_event(self):
        """Test cancelling a scheduled event."""
        event_system = EventSystem()
        called = []

        event_id = event_system.schedule(10, lambda: called.append(True), event_id="test_event")

        result = event_system.cancel_event(event_id)

        assert result is True
        event_system.tick(10)
        assert len(called) == 0

    def test_cancel_nonexistent_event(self):
        """Test that cancelling a nonexistent event returns False."""
        event_system = EventSystem()

        result = event_system.cancel_event("nonexistent")

        assert result is False

    def test_cancel_removes_event_from_pending(self):
        """Test that cancelled events are removed from pending events."""
        event_system = EventSystem()

        event_id = event_system.schedule(10, lambda: None, event_id="test_event")

        assert len(event_system.get_pending_events()) == 1

        event_system.cancel_event(event_id)

        assert len(event_system.get_pending_events()) == 0


class TestClearAllEvents:
    """Tests for clearing all scheduled events."""

    def test_clear_all_events(self):
        """Test clearing all scheduled events."""
        event_system = EventSystem()

        event_system.schedule(10, lambda: None)
        event_system.schedule(20, lambda: None)
        event_system.schedule(30, lambda: None)

        count = event_system.clear_all_events()

        assert count == 3
        assert len(event_system.get_pending_events()) == 0

    def test_clear_all_events_when_empty(self):
        """Test clearing events when queue is empty."""
        event_system = EventSystem()

        count = event_system.clear_all_events()

        assert count == 0


class TestScheduledEventDataclass:
    """Tests for the ScheduledEvent dataclass."""

    def test_create_scheduled_event(self):
        """Test creating a ScheduledEvent."""
        event = ScheduledEvent(tick=10, callback=lambda: None)

        assert event.tick == 10
        assert event.callback is not None
        assert event.args == ()
        assert event.kwargs == {}
        assert event.event_id is None

    def test_scheduled_event_with_all_fields(self):
        """Test creating a ScheduledEvent with all fields."""
        callback = lambda x, y: x + y
        event = ScheduledEvent(
            tick=50, callback=callback, args=(1, 2), kwargs={"z": 3}, event_id="test"
        )

        assert event.tick == 50
        assert event.callback is callback
        assert event.args == (1, 2)
        assert event.kwargs == {"z": 3}
        assert event.event_id == "test"


class TestEventSystemIndependence:
    """Tests to verify EventSystem instances are independent."""

    def test_multiple_event_systems_are_independent(self):
        """Test that multiple EventSystem instances don't share state."""
        event_system1 = EventSystem()
        event_system2 = EventSystem()
        results1 = []
        results2 = []

        event_system1.schedule(5, lambda: results1.append(1))
        event_system2.schedule(5, lambda: results2.append(2))

        event_system1.tick(5)

        assert results1 == [1]
        assert results2 == []

        event_system2.tick(5)

        assert results1 == [1]
        assert results2 == [2]


class TestEventSystemLogging:
    """Tests for EventSystem logging behavior."""

    def test_initialization_logs_debug_message(self, caplog):
        """Test that initialization logs a debug message."""
        with caplog.at_level(logging.DEBUG):
            EventSystem()

        assert "EventSystem initialized" in caplog.text

    def test_schedule_logs_debug_message(self, caplog):
        """Test that schedule() logs a debug message."""
        event_system = EventSystem()

        with caplog.at_level(logging.DEBUG):
            event_system.schedule(10, lambda: None, event_id="test_event")

        assert "Scheduled event 'test_event' at tick 10" in caplog.text

    def test_dispatch_logs_info_message(self, caplog):
        """Test that dispatching an event logs an info message."""
        event_system = EventSystem()
        event_system.schedule(5, lambda: None, event_id="test_event")

        with caplog.at_level(logging.INFO):
            event_system.tick(5)

        assert "Dispatching event 'test_event' at tick 5" in caplog.text

    def test_cancel_logs_debug_message(self, caplog):
        """Test that cancel_event() logs a debug message."""
        event_system = EventSystem()
        event_id = event_system.schedule(10, lambda: None, event_id="test_event")

        with caplog.at_level(logging.DEBUG):
            event_system.cancel_event(event_id)

        assert "Cancelled event 'test_event'" in caplog.text

    def test_clear_logs_debug_message(self, caplog):
        """Test that clear_all_events() logs a debug message."""
        event_system = EventSystem()
        event_system.schedule(10, lambda: None)
        event_system.schedule(20, lambda: None)

        with caplog.at_level(logging.DEBUG):
            event_system.clear_all_events()

        assert "Cleared 2 events from queue" in caplog.text


class TestIntegrationWithTimeSystem:
    """Integration tests with TimeSystem to verify complete functionality."""

    def test_event_fires_at_expected_time_with_time_system(self):
        """Test that event fires at expected time when integrated with TimeSystem."""
        from src.world.time_system import TimeSystem

        time_system = TimeSystem()
        event_system = EventSystem()
        results = []

        # Schedule event for 10 rounds (100 ticks)
        target_tick = time_system.rounds_to_ticks(10)
        event_system.schedule(target_tick, lambda: results.append("fired"))

        # Advance time by 10 rounds
        time_system.advance(target_tick)

        # Check that event fires
        event_system.tick(time_system.current_tick)

        assert results == ["fired"]

    def test_multiple_events_with_time_conversions(self):
        """Test multiple events scheduled using time unit conversions."""
        from src.world.time_system import TimeSystem

        time_system = TimeSystem()
        event_system = EventSystem()
        results = []

        # Schedule events at different time intervals
        event_system.schedule(time_system.rounds_to_ticks(1), lambda: results.append("round"))
        event_system.schedule(time_system.turns_to_ticks(1), lambda: results.append("turn"))
        event_system.schedule(time_system.hours_to_ticks(1), lambda: results.append("hour"))

        # Advance time by 1 hour and dispatch
        time_system.advance(time_system.hours_to_ticks(1))
        event_system.tick(time_system.current_tick)

        assert results == ["round", "turn", "hour"]

    def test_incremental_time_advancement_with_events(self):
        """Test incremental time advancement triggers events correctly."""
        from src.world.time_system import TimeSystem

        time_system = TimeSystem()
        event_system = EventSystem()
        results = []

        # Schedule events at ticks 10, 20, 30
        event_system.schedule(10, lambda: results.append(10))
        event_system.schedule(20, lambda: results.append(20))
        event_system.schedule(30, lambda: results.append(30))

        # Advance time incrementally
        time_system.advance(10)
        event_system.tick(time_system.current_tick)
        assert results == [10]

        time_system.advance(10)
        event_system.tick(time_system.current_tick)
        assert results == [10, 20]

        time_system.advance(10)
        event_system.tick(time_system.current_tick)
        assert results == [10, 20, 30]
