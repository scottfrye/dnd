"""Admin command infrastructure and core commands.

This module provides:
- A minimal command dispatch API through AdminCommandRegistry
- Core admin commands: teleport, reveal_map, show_factions, advance_time
- Command discovery and help functionality
"""

import logging
from collections.abc import Callable
from typing import Any

from src.entities.entity import Position
from src.world.world_state import WorldState

logger = logging.getLogger(__name__)


class CommandResult:
    """Result of executing an admin command.

    Attributes:
        success: Whether the command executed successfully.
        message: Human-readable result message.
        data: Optional structured data from the command.
    """

    def __init__(self, success: bool, message: str, data: dict[str, Any] | None = None):
        self.success = success
        self.message = message
        self.data = data or {}


# Core command implementations - defined before AdminCommandRegistry


def cmd_advance_time(world: WorldState, ticks: int = 1, **kwargs: Any) -> CommandResult:
    """Advance game time by specified ticks.

    Args:
        world: The WorldState to operate on.
        ticks: Number of ticks to advance (default: 1).
        **kwargs: Additional keyword arguments (ignored).

    Returns:
        CommandResult with the new world time.
    """
    if ticks < 0:
        return CommandResult(False, "Cannot advance time by negative ticks")

    start_time = world.time
    for _ in range(ticks):
        world.tick()
    end_time = world.time

    return CommandResult(
        True,
        f"Advanced time by {ticks} ticks (from {start_time} to {end_time})",
        {"start_time": start_time, "end_time": end_time, "ticks": ticks},
    )


def cmd_show_factions(
    world: WorldState, detail: bool = False, **kwargs: Any
) -> CommandResult:
    """Display faction information.

    This is a placeholder implementation that demonstrates the command structure.
    In a full implementation, this would query faction data from the WorldState.

    Args:
        world: The WorldState to operate on.
        detail: Whether to show detailed information (default: False).
        **kwargs: Additional keyword arguments (ignored).

    Returns:
        CommandResult with faction information.
    """
    # For now, return a stub message
    # In a full implementation, this would query actual faction data
    mode = "detailed" if detail else "summary"
    message = f"Faction display ({mode}) - No factions currently defined"
    data = {"mode": mode, "factions": [], "total": 0}

    return CommandResult(True, message, data)


def cmd_teleport(
    world: WorldState, entity_id: str, location_id: str, x: int, y: int, **kwargs: Any
) -> CommandResult:
    """Teleport an entity to a location.

    Args:
        world: The WorldState to operate on.
        entity_id: The ID of the entity to teleport.
        location_id: The target location ID.
        x: The x-coordinate.
        y: The y-coordinate.
        **kwargs: Additional keyword arguments (ignored).

    Returns:
        CommandResult indicating success or failure.
    """
    entity = world.get_entity(entity_id)
    if entity is None:
        return CommandResult(False, f"Entity not found: {entity_id}")

    old_pos = entity.position
    entity.position = Position(x=x, y=y, location_id=location_id)

    return CommandResult(
        True,
        f"Teleported {entity_id} from [{old_pos.x}, {old_pos.y}] to "
        f"[{x}, {y}] in {location_id}",
        {
            "entity_id": entity_id,
            "old_position": {
                "x": old_pos.x,
                "y": old_pos.y,
                "location_id": old_pos.location_id,
            },
            "new_position": {"x": x, "y": y, "location_id": location_id},
        },
    )


def cmd_reveal_map(
    world: WorldState, area: str = "current", **kwargs: Any
) -> CommandResult:
    """Reveal map areas (remove fog of war).

    This is a placeholder implementation. In a full implementation,
    this would interact with a map visibility system.

    Args:
        world: The WorldState to operate on.
        area: The area to reveal ("current", "all", or location name).
        **kwargs: Additional keyword arguments (ignored).

    Returns:
        CommandResult indicating what was revealed.
    """
    # Placeholder implementation
    message = f"Map revealed: {area}"
    data = {"area": area, "revealed": True}

    return CommandResult(True, message, data)


class AdminCommandRegistry:
    """Registry for admin commands with discovery and dispatch.

    The AdminCommandRegistry maintains a collection of admin commands
    and provides methods for registering, discovering, and executing them.
    Commands are callable functions that take a WorldState and optional
    arguments, returning a CommandResult.
    """

    def __init__(self) -> None:
        """Initialize the command registry."""
        self._commands: dict[str, Callable] = {}
        self._descriptions: dict[str, str] = {}
        self._register_core_commands()

    def register(self, name: str, func: Callable, description: str = "") -> None:
        """Register a command with the registry.

        Args:
            name: The command name (used for dispatch).
            func: The callable function implementing the command.
            description: Brief description of what the command does.
        """
        self._commands[name] = func
        self._descriptions[name] = description
        logger.debug("Registered command: %s", name)

    def get_command(self, name: str) -> Callable | None:
        """Get a command by name.

        Args:
            name: The command name to look up.

        Returns:
            The command function if found, None otherwise.
        """
        return self._commands.get(name)

    def list_commands(self) -> list[str]:
        """Get a list of all registered command names.

        Returns:
            Sorted list of command names.
        """
        return sorted(self._commands.keys())

    def get_description(self, name: str) -> str:
        """Get the description for a command.

        Args:
            name: The command name.

        Returns:
            The command description, or empty string if not found.
        """
        return self._descriptions.get(name, "")

    def execute(
        self, command: str, world: WorldState, *args: Any, **kwargs: Any
    ) -> CommandResult:
        """Execute a command by name.

        Args:
            command: The name of the command to execute.
            world: The WorldState to operate on.
            *args: Positional arguments to pass to the command.
            **kwargs: Keyword arguments to pass to the command.

        Returns:
            CommandResult with execution status and message.
        """
        cmd_func = self.get_command(command)
        if cmd_func is None:
            return CommandResult(False, f"Unknown command: {command}")

        try:
            return cmd_func(world, *args, **kwargs)
        except Exception as e:
            logger.exception("Error executing command '%s'", command)
            return CommandResult(False, f"Command failed: {str(e)}")

    def _register_core_commands(self) -> None:
        """Register the core admin commands."""
        self.register(
            "advance_time", cmd_advance_time, "Advance game time by specified ticks"
        )
        self.register("show_factions", cmd_show_factions, "Display faction information")
        self.register("teleport", cmd_teleport, "Teleport an entity to a location")
        self.register(
            "reveal_map", cmd_reveal_map, "Reveal map areas (remove fog of war)"
        )


# Global registry instance
_registry = AdminCommandRegistry()


def execute_command(
    command: str, world: WorldState, *args: Any, **kwargs: Any
) -> CommandResult:
    """Execute an admin command using the global registry.

    This is a convenience function that uses the global AdminCommandRegistry.

    Args:
        command: The name of the command to execute.
        world: The WorldState to operate on.
        *args: Positional arguments to pass to the command.
        **kwargs: Keyword arguments to pass to the command.

    Returns:
        CommandResult with execution status and message.
    """
    return _registry.execute(command, world, *args, **kwargs)


def get_registry() -> AdminCommandRegistry:
    """Get the global command registry.

    Returns:
        The global AdminCommandRegistry instance.
    """
    return _registry
