"""Unit tests for admin commands.

These tests verify the admin command infrastructure and core commands
operate correctly on WorldState instances.
"""

from src.admin.commands import (
    AdminCommandRegistry,
    CommandResult,
    cmd_advance_time,
    cmd_reveal_map,
    cmd_show_factions,
    cmd_teleport,
    execute_command,
    get_registry,
)
from src.entities.entity import Entity, Position
from src.world.world_state import WorldState


class TestCommandResult:
    """Tests for CommandResult class."""

    def test_command_result_success(self):
        """Test creating a successful command result."""
        result = CommandResult(True, "Success")

        assert result.success is True
        assert result.message == "Success"
        assert result.data == {}

    def test_command_result_with_data(self):
        """Test creating a command result with data."""
        data = {"key": "value"}
        result = CommandResult(True, "Success", data)

        assert result.success is True
        assert result.message == "Success"
        assert result.data == data

    def test_command_result_failure(self):
        """Test creating a failed command result."""
        result = CommandResult(False, "Error occurred")

        assert result.success is False
        assert result.message == "Error occurred"


class TestAdminCommandRegistry:
    """Tests for AdminCommandRegistry class."""

    def test_registry_initialization(self):
        """Test that registry initializes with core commands."""
        registry = AdminCommandRegistry()

        commands = registry.list_commands()
        assert "advance_time" in commands
        assert "show_factions" in commands
        assert "teleport" in commands
        assert "reveal_map" in commands

    def test_register_command(self):
        """Test registering a new command."""
        registry = AdminCommandRegistry()

        def test_command(world, **kwargs):
            return CommandResult(True, "Test")

        registry.register("test", test_command, "Test command")

        assert "test" in registry.list_commands()
        assert registry.get_command("test") is test_command
        assert registry.get_description("test") == "Test command"

    def test_get_nonexistent_command(self):
        """Test getting a command that doesn't exist."""
        registry = AdminCommandRegistry()

        result = registry.get_command("nonexistent")

        assert result is None

    def test_get_description_nonexistent(self):
        """Test getting description for nonexistent command."""
        registry = AdminCommandRegistry()

        result = registry.get_description("nonexistent")

        assert result == ""

    def test_execute_command_success(self):
        """Test executing a registered command successfully."""
        registry = AdminCommandRegistry()
        world = WorldState()

        result = registry.execute("show_factions", world)

        assert result.success is True

    def test_execute_unknown_command(self):
        """Test executing an unknown command."""
        registry = AdminCommandRegistry()
        world = WorldState()

        result = registry.execute("unknown", world)

        assert result.success is False
        assert "Unknown command" in result.message

    def test_execute_command_with_exception(self):
        """Test executing a command that raises an exception."""
        registry = AdminCommandRegistry()
        world = WorldState()

        def failing_command(world, **kwargs):
            raise ValueError("Test error")

        registry.register("fail", failing_command)

        result = registry.execute("fail", world)

        assert result.success is False
        assert "Command failed" in result.message


class TestGlobalRegistry:
    """Tests for global registry functions."""

    def test_get_registry_returns_same_instance(self):
        """Test that get_registry returns the same instance."""
        registry1 = get_registry()
        registry2 = get_registry()

        assert registry1 is registry2

    def test_execute_command_uses_global_registry(self):
        """Test that execute_command uses the global registry."""
        world = WorldState()

        result = execute_command("show_factions", world)

        assert result.success is True


class TestAdvanceTimeCommand:
    """Tests for the advance_time command."""

    def test_advance_time_default(self):
        """Test advancing time by default amount (1 tick)."""
        world = WorldState()
        initial_time = world.time

        result = cmd_advance_time(world)

        assert result.success is True
        assert world.time == initial_time + 1
        assert "Advanced time by 1 ticks" in result.message
        assert result.data["ticks"] == 1
        assert result.data["start_time"] == initial_time
        assert result.data["end_time"] == initial_time + 1

    def test_advance_time_multiple_ticks(self):
        """Test advancing time by multiple ticks."""
        world = WorldState()
        initial_time = world.time

        result = cmd_advance_time(world, ticks=10)

        assert result.success is True
        assert world.time == initial_time + 10
        assert "Advanced time by 10 ticks" in result.message
        assert result.data["ticks"] == 10

    def test_advance_time_large_amount(self):
        """Test advancing time by a large number of ticks."""
        world = WorldState()
        initial_time = world.time

        result = cmd_advance_time(world, ticks=1000)

        assert result.success is True
        assert world.time == initial_time + 1000

    def test_advance_time_zero_ticks(self):
        """Test advancing time by zero ticks."""
        world = WorldState()
        initial_time = world.time

        result = cmd_advance_time(world, ticks=0)

        assert result.success is True
        assert world.time == initial_time
        assert result.data["ticks"] == 0

    def test_advance_time_negative_ticks_fails(self):
        """Test that advancing by negative ticks fails."""
        world = WorldState()

        result = cmd_advance_time(world, ticks=-5)

        assert result.success is False
        assert "negative" in result.message.lower()

    def test_advance_time_updates_world_state(self):
        """Test that advance_time properly updates WorldState."""
        world = WorldState()
        # Add some entities to ensure state is maintained
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test_entity", position=pos)
        world.add_entity(entity)

        result = cmd_advance_time(world, ticks=5)

        assert result.success is True
        assert world.time == 5
        # Entity should still exist
        assert world.get_entity("test_entity") is entity


class TestShowFactionsCommand:
    """Tests for the show_factions command."""

    def test_show_factions_default(self):
        """Test showing factions with default settings."""
        world = WorldState()

        result = cmd_show_factions(world)

        assert result.success is True
        assert "summary" in result.message
        assert result.data["mode"] == "summary"
        assert result.data["total"] == 0
        assert isinstance(result.data["factions"], list)

    def test_show_factions_detailed(self):
        """Test showing factions with detail flag."""
        world = WorldState()

        result = cmd_show_factions(world, detail=True)

        assert result.success is True
        assert "detailed" in result.message
        assert result.data["mode"] == "detailed"

    def test_show_factions_summary(self):
        """Test showing factions in summary mode."""
        world = WorldState()

        result = cmd_show_factions(world, detail=False)

        assert result.success is True
        assert result.data["mode"] == "summary"

    def test_show_factions_operates_on_world_state(self):
        """Test that show_factions receives and can operate on WorldState."""
        world = WorldState()
        # Advance time to ensure we're working with the right world
        world.tick()
        world.tick()

        result = cmd_show_factions(world)

        # Command should succeed and work with the world state
        assert result.success is True
        # World state should be unmodified (read-only operation)
        assert world.time == 2


class TestTeleportCommand:
    """Tests for the teleport command."""

    def test_teleport_entity(self):
        """Test teleporting an entity to a new location."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="start")
        entity = Entity(id="player", position=pos)
        world.add_entity(entity)

        result = cmd_teleport(world, "player", "end", 10, 20)

        assert result.success is True
        assert "Teleported" in result.message
        assert entity.position.x == 10
        assert entity.position.y == 20
        assert entity.position.location_id == "end"
        assert result.data["entity_id"] == "player"
        assert result.data["old_position"]["x"] == 0
        assert result.data["old_position"]["y"] == 0
        assert result.data["new_position"]["x"] == 10
        assert result.data["new_position"]["y"] == 20

    def test_teleport_nonexistent_entity(self):
        """Test teleporting an entity that doesn't exist."""
        world = WorldState()

        result = cmd_teleport(world, "nonexistent", "location", 5, 5)

        assert result.success is False
        assert "not found" in result.message.lower()

    def test_teleport_preserves_other_properties(self):
        """Test that teleport preserves entity properties."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="start")
        entity = Entity(id="npc", position=pos, properties={"hp": 50, "name": "Bob"})
        world.add_entity(entity)

        result = cmd_teleport(world, "npc", "new_location", 15, 25)

        assert result.success is True
        assert entity.properties["hp"] == 50
        assert entity.properties["name"] == "Bob"


class TestRevealMapCommand:
    """Tests for the reveal_map command."""

    def test_reveal_map_current(self):
        """Test revealing the current map area."""
        world = WorldState()

        result = cmd_reveal_map(world)

        assert result.success is True
        assert "current" in result.message.lower()
        assert result.data["area"] == "current"
        assert result.data["revealed"] is True

    def test_reveal_map_all(self):
        """Test revealing all map areas."""
        world = WorldState()

        result = cmd_reveal_map(world, area="all")

        assert result.success is True
        assert "all" in result.message.lower()
        assert result.data["area"] == "all"

    def test_reveal_map_specific_area(self):
        """Test revealing a specific area."""
        world = WorldState()

        result = cmd_reveal_map(world, area="temple_level_1")

        assert result.success is True
        assert "temple_level_1" in result.message
        assert result.data["area"] == "temple_level_1"


class TestCommandIntegration:
    """Integration tests for command execution."""

    def test_execute_advance_time_through_registry(self):
        """Test executing advance_time through the registry."""
        world = WorldState()
        initial_time = world.time

        result = execute_command("advance_time", world, ticks=5)

        assert result.success is True
        assert world.time == initial_time + 5

    def test_execute_show_factions_through_registry(self):
        """Test executing show_factions through the registry."""
        world = WorldState()

        result = execute_command("show_factions", world, detail=True)

        assert result.success is True
        assert result.data["mode"] == "detailed"

    def test_execute_teleport_through_registry(self):
        """Test executing teleport through the registry."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="start")
        entity = Entity(id="entity1", position=pos)
        world.add_entity(entity)

        result = execute_command("teleport", world, "entity1", "end", 5, 10)

        assert result.success is True
        assert entity.position.x == 5

    def test_execute_reveal_map_through_registry(self):
        """Test executing reveal_map through the registry."""
        world = WorldState()

        result = execute_command("reveal_map", world, area="hommlet")

        assert result.success is True
        assert result.data["area"] == "hommlet"
