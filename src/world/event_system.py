"""Event system for scheduling and dispatching time-based events.

This module provides the EventSystem class which allows scheduling
callable events at future ticks and dispatches them when the time arrives.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ScheduledEvent:
    """Represents a scheduled event.

    Attributes:
        tick: The tick at which the event should fire.
        callback: The callable to invoke when the event fires.
        args: Positional arguments to pass to the callback.
        kwargs: Keyword arguments to pass to the callback.
        event_id: Optional identifier for the event.
    """

    tick: int
    callback: Callable[..., Any]
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] | None = None
    event_id: str | None = None


class EventSystem:
    """Manages scheduling and dispatching of time-based events.

    EventSystem allows scheduling callable events to fire at specific future
    ticks. When tick() is called with the current game time, all events
    scheduled for that tick or earlier are dispatched in order.

    Events are stored in a list and dispatched in the order they were scheduled
    for each tick.
    """

    def __init__(self) -> None:
        """Initialize a new EventSystem with an empty event queue."""
        self._events: list[ScheduledEvent] = []
        self._next_event_id: int = 0
        logger.debug("EventSystem initialized")

    def schedule(
        self,
        tick: int,
        callback: Callable[..., Any],
        *args: Any,
        event_id: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Schedule an event to fire at a specific tick.

        Args:
            tick: The tick at which the event should fire.
            callback: The callable to invoke when the event fires.
            *args: Positional arguments to pass to the callback.
            event_id: Optional identifier for the event. If not provided,
                     a unique ID will be generated.
            **kwargs: Keyword arguments to pass to the callback.

        Returns:
            The event_id of the scheduled event.

        Raises:
            ValueError: If tick is negative.
        """
        if tick < 0:
            raise ValueError("Cannot schedule event at negative tick")

        if event_id is None:
            event_id = f"event_{self._next_event_id}"
            self._next_event_id += 1

        event = ScheduledEvent(
            tick=tick,
            callback=callback,
            args=args,
            kwargs=kwargs if kwargs else {},
            event_id=event_id,
        )
        self._events.append(event)
        logger.debug("Scheduled event '%s' at tick %d", event_id, tick)

        return event_id

    def tick(self, current_tick: int) -> list[tuple[str | None, Any]]:
        """Dispatch all events scheduled for the current tick or earlier.

        Events are dispatched in the order they were scheduled. After dispatch,
        the events are removed from the queue.

        Args:
            current_tick: The current game time tick.

        Returns:
            List of tuples containing (event_id, return_value) for each
            dispatched event.
        """
        # Find all events that should fire
        events_to_fire = [e for e in self._events if e.tick <= current_tick]

        if not events_to_fire:
            return []

        # Sort by tick, then by original order (stable sort)
        events_to_fire.sort(key=lambda e: e.tick)

        results: list[tuple[str | None, Any]] = []

        for event in events_to_fire:
            logger.info(
                "Dispatching event '%s' at tick %d", event.event_id, current_tick
            )
            try:
                result = event.callback(*event.args, **event.kwargs)
                results.append((event.event_id, result))
            except Exception as e:
                logger.error(
                    "Error dispatching event '%s': %s",
                    event.event_id,
                    e,
                    exc_info=True,
                )
                results.append((event.event_id, e))

        # Remove all fired events from the queue efficiently
        self._events = [e for e in self._events if e not in events_to_fire]

        return results

    def cancel_event(self, event_id: str) -> bool:
        """Cancel a scheduled event.

        Args:
            event_id: The ID of the event to cancel.

        Returns:
            True if the event was found and cancelled, False otherwise.
        """
        for event in self._events:
            if event.event_id == event_id:
                self._events.remove(event)
                logger.debug("Cancelled event '%s'", event_id)
                return True
        return False

    def _get_callback_name(self, callback: Callable[..., Any]) -> str:
        """Get a readable name for a callback function.

        Args:
            callback: The callback function.

        Returns:
            The callback's __name__ attribute if available, otherwise str representation.
        """
        return callback.__name__ if hasattr(callback, "__name__") else str(callback)

    def get_pending_events(self) -> list[dict[str, Any]]:
        """Get information about all pending events.

        Returns:
            List of dictionaries containing event information (tick, event_id).
        """
        return [
            {
                "tick": event.tick,
                "event_id": event.event_id,
                "callback": self._get_callback_name(event.callback),
            }
            for event in self._events
        ]

    def clear_all_events(self) -> int:
        """Clear all scheduled events from the queue.

        Returns:
            The number of events that were cleared.
        """
        count = len(self._events)
        self._events.clear()
        logger.debug("Cleared %d events from queue", count)
        return count
