"""Unit tests for the GameEngine class.

These tests verify that the GameEngine:
- Can be initialized in different modes
- Advances world ticks in step() method
- Runs headless mode for multiple ticks
- Integrates correctly with WorldState
"""

import logging

import pytest

from src.entities.entity import Entity, Position
from src.game.game_engine import GameEngine, GameMode
from src.simulation.npc_ai import Action
from src.world.world_state import WorldState


class TestGameEngineInitialization:
    """Tests for GameEngine initialization."""

    def test_default_initialization(self):
        """Test default initialization creates a new world in player mode."""
        engine = GameEngine()

        assert engine.world is not None
        assert engine.mode == GameMode.PLAYER
        assert engine.world.time == 0

    def test_initialization_with_world(self):
        """Test initialization with an existing world."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        engine = GameEngine(world=world)

        assert engine.world is world
        assert engine.world.get_entity("entity_1") is entity

    def test_initialization_in_headless_mode(self):
        """Test initialization in headless mode."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        assert engine.mode == GameMode.HEADLESS
        assert engine.world is not None

    def test_initialization_with_world_and_mode(self):
        """Test initialization with both world and mode."""
        world = WorldState()
        engine = GameEngine(world=world, mode=GameMode.HEADLESS)

        assert engine.world is world
        assert engine.mode == GameMode.HEADLESS


class TestGameEnginePlayerMode:
    """Tests for GameEngine in player mode."""

    def test_step_advances_world_time(self):
        """Test that step() advances the world time by one tick."""
        engine = GameEngine(mode=GameMode.PLAYER)
        initial_time = engine.world.time

        engine.step()

        assert engine.world.time == initial_time + 1

    def test_step_returns_current_time(self):
        """Test that step() returns the current world time."""
        engine = GameEngine(mode=GameMode.PLAYER)

        result = engine.step()

        assert result == 1

    def test_multiple_steps_advance_time(self):
        """Test that multiple steps advance time correctly."""
        engine = GameEngine(mode=GameMode.PLAYER)

        engine.step()
        engine.step()
        result = engine.step()

        assert engine.world.time == 3
        assert result == 3

    def test_step_with_action(self):
        """Test that step() can accept an action in player mode."""
        engine = GameEngine(mode=GameMode.PLAYER)
        pos = Position(x=0, y=0, location_id="test")
        action = Action(action_type="move", target_position=pos)

        result = engine.step(action=action)

        # Action is logged but not applied by GameEngine itself
        assert result == 1
        assert engine.world.time == 1

    def test_step_without_action_in_player_mode(self):
        """Test that step() works without an action in player mode."""
        engine = GameEngine(mode=GameMode.PLAYER)

        result = engine.step()

        assert result == 1
        assert engine.world.time == 1

    def test_step_logs_action_type(self, caplog):
        """Test that step() logs the action type when provided."""
        engine = GameEngine(mode=GameMode.PLAYER)
        action = Action(action_type="attack", target_entity_id="enemy_1")

        with caplog.at_level(logging.DEBUG):
            engine.step(action=action)

        assert "Processing action: attack" in caplog.text


class TestGameEngineHeadlessMode:
    """Tests for GameEngine in headless mode."""

    def test_run_headless_advances_ticks(self):
        """Test that run_headless advances time by specified ticks."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        result = engine.run_headless(ticks=5)

        assert engine.world.time == 5
        assert result == 5

    def test_run_headless_zero_ticks(self):
        """Test that run_headless with 0 ticks does nothing."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        result = engine.run_headless(ticks=0)

        assert engine.world.time == 0
        assert result == 0

    def test_run_headless_negative_ticks_raises_error(self):
        """Test that run_headless with negative ticks raises ValueError."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        with pytest.raises(ValueError, match="Number of ticks must be non-negative"):
            engine.run_headless(ticks=-1)

    def test_run_headless_large_number_of_ticks(self):
        """Test run_headless with a large number of ticks."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        result = engine.run_headless(ticks=100)

        assert engine.world.time == 100
        assert result == 100

    def test_run_headless_multiple_times(self):
        """Test calling run_headless multiple times accumulates ticks."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        engine.run_headless(ticks=10)
        engine.run_headless(ticks=15)
        result = engine.run_headless(ticks=5)

        assert engine.world.time == 30
        assert result == 30

    def test_run_headless_logs_completion(self, caplog):
        """Test that run_headless logs completion."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        with caplog.at_level(logging.INFO):
            engine.run_headless(ticks=3)

        assert "Running headless simulation for 3 ticks" in caplog.text
        assert "Headless simulation completed, final time: 3" in caplog.text


class TestGameEngineModeManagement:
    """Tests for game mode management."""

    def test_set_mode_changes_mode(self):
        """Test that set_mode changes the game mode."""
        engine = GameEngine(mode=GameMode.PLAYER)

        engine.set_mode(GameMode.HEADLESS)

        assert engine.mode == GameMode.HEADLESS

    def test_set_mode_from_headless_to_player(self):
        """Test changing mode from headless to player."""
        engine = GameEngine(mode=GameMode.HEADLESS)

        engine.set_mode(GameMode.PLAYER)

        assert engine.mode == GameMode.PLAYER

    def test_set_mode_logs_change(self, caplog):
        """Test that set_mode logs the mode change."""
        engine = GameEngine(mode=GameMode.PLAYER)

        with caplog.at_level(logging.INFO):
            engine.set_mode(GameMode.HEADLESS)

        assert "Changing game mode from player to headless" in caplog.text

    def test_set_mode_to_same_mode_does_not_log(self, caplog):
        """Test that setting the same mode doesn't log a change."""
        engine = GameEngine(mode=GameMode.PLAYER)

        with caplog.at_level(logging.INFO):
            engine.set_mode(GameMode.PLAYER)

        # Should not log a mode change
        assert "Changing game mode" not in caplog.text


class TestGameEngineTimeQueries:
    """Tests for time-related queries."""

    def test_get_current_time_initial(self):
        """Test getting current time at initialization."""
        engine = GameEngine()

        assert engine.get_current_time() == 0

    def test_get_current_time_after_steps(self):
        """Test getting current time after advancing."""
        engine = GameEngine()
        engine.step()
        engine.step()

        assert engine.get_current_time() == 2

    def test_get_current_time_after_headless(self):
        """Test getting current time after headless run."""
        engine = GameEngine(mode=GameMode.HEADLESS)
        engine.run_headless(ticks=25)

        assert engine.get_current_time() == 25


class TestGameEngineIntegration:
    """Integration tests for GameEngine with WorldState."""

    def test_engine_with_entities_in_world(self):
        """Test engine operates correctly with entities in world."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="test")
        pos2 = Position(x=5, y=5, location_id="test")
        entity1 = Entity(id="entity_1", position=pos1)
        entity2 = Entity(id="entity_2", position=pos2)
        world.add_entity(entity1)
        world.add_entity(entity2)

        engine = GameEngine(world=world)
        engine.step()

        assert engine.world.get_entity("entity_1") is entity1
        assert engine.world.get_entity("entity_2") is entity2
        assert engine.world.time == 1

    def test_engine_preserves_world_state_across_ticks(self):
        """Test that world state is preserved across ticks."""
        world = WorldState()
        pos = Position(x=10, y=20, location_id="dungeon")
        entity = Entity(id="hero", position=pos, properties={"hp": 50})
        world.add_entity(entity)

        engine = GameEngine(world=world)
        engine.step()
        engine.step()

        retrieved = engine.world.get_entity("hero")
        assert retrieved is entity
        assert retrieved.properties["hp"] == 50
        assert retrieved.position.x == 10
        assert retrieved.position.y == 20

    def test_mixed_mode_operation(self):
        """Test switching between modes and advancing time."""
        engine = GameEngine(mode=GameMode.PLAYER)

        # Player mode steps
        engine.step()
        engine.step()

        # Switch to headless
        engine.set_mode(GameMode.HEADLESS)
        engine.run_headless(ticks=10)

        # Back to player mode
        engine.set_mode(GameMode.PLAYER)
        engine.step()

        assert engine.world.time == 13
