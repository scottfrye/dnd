"""Unit tests for the WorldState class.

These tests verify that the WorldState class correctly:
- Adds entities and prevents duplicate ids
- Removes entities
- Queries entities by id
- Advances time via tick() and emits logged events
"""

import logging

import pytest

from src.entities.entity import Entity, Position
from src.world.world_state import WorldState


class TestWorldStateEntityManagement:
    """Tests for entity add/remove/query operations."""

    def test_add_entity(self):
        """Test adding an entity to the world."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)

        world.add_entity(entity)

        assert world.get_entity("entity_1") is entity

    def test_add_multiple_entities(self):
        """Test adding multiple entities to the world."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="test")
        pos2 = Position(x=1, y=1, location_id="test")
        entity1 = Entity(id="entity_1", position=pos1)
        entity2 = Entity(id="entity_2", position=pos2)

        world.add_entity(entity1)
        world.add_entity(entity2)

        assert world.get_entity("entity_1") is entity1
        assert world.get_entity("entity_2") is entity2

    def test_add_duplicate_entity_raises_error(self):
        """Test that adding an entity with duplicate id raises ValueError."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity1 = Entity(id="entity_1", position=pos)
        entity2 = Entity(id="entity_1", position=pos)

        world.add_entity(entity1)

        with pytest.raises(
            ValueError, match="Entity with id 'entity_1' already exists"
        ):
            world.add_entity(entity2)

    def test_remove_entity(self):
        """Test removing an entity from the world."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        result = world.remove_entity("entity_1")

        assert result is True
        assert world.get_entity("entity_1") is None

    def test_remove_nonexistent_entity_returns_false(self):
        """Test that removing a nonexistent entity returns False."""
        world = WorldState()

        result = world.remove_entity("nonexistent")

        assert result is False

    def test_get_entity_returns_entity(self):
        """Test querying an entity by id returns the entity."""
        world = WorldState()
        pos = Position(x=5, y=10, location_id="dungeon")
        entity = Entity(id="goblin_001", position=pos, properties={"hp": 7})
        world.add_entity(entity)

        result = world.get_entity("goblin_001")

        assert result is entity
        assert result.id == "goblin_001"
        assert result.properties["hp"] == 7

    def test_get_nonexistent_entity_returns_none(self):
        """Test querying a nonexistent entity returns None."""
        world = WorldState()

        result = world.get_entity("nonexistent")

        assert result is None

    def test_get_all_entity_ids_empty_world(self):
        """Test getting all entity IDs from an empty world returns empty list."""
        world = WorldState()

        result = world.get_all_entity_ids()

        assert result == []

    def test_get_all_entity_ids_single_entity(self):
        """Test getting all entity IDs with one entity."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        result = world.get_all_entity_ids()

        assert len(result) == 1
        assert "entity_1" in result

    def test_get_all_entity_ids_multiple_entities(self):
        """Test getting all entity IDs with multiple entities."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="test")
        pos2 = Position(x=1, y=1, location_id="test")
        pos3 = Position(x=2, y=2, location_id="test")
        entity1 = Entity(id="entity_1", position=pos1)
        entity2 = Entity(id="entity_2", position=pos2)
        entity3 = Entity(id="entity_3", position=pos3)
        world.add_entity(entity1)
        world.add_entity(entity2)
        world.add_entity(entity3)

        result = world.get_all_entity_ids()

        assert len(result) == 3
        assert "entity_1" in result
        assert "entity_2" in result
        assert "entity_3" in result


class TestWorldStateTick:
    """Tests for the tick/time system."""

    def test_initial_time_is_zero(self):
        """Test that initial time is 0."""
        world = WorldState()

        assert world.time == 0

    def test_tick_advances_time(self):
        """Test that tick() advances the internal time counter."""
        world = WorldState()

        world.tick()

        assert world.time == 1

    def test_multiple_ticks_advance_time(self):
        """Test that multiple ticks advance time correctly."""
        world = WorldState()

        world.tick()
        world.tick()
        world.tick()

        assert world.time == 3

    def test_tick_returns_new_time(self):
        """Test that tick() returns the new time value."""
        world = WorldState()

        result = world.tick()

        assert result == 1

    def test_tick_emits_logged_event(self, caplog):
        """Test that tick() emits a logged event."""
        world = WorldState()

        with caplog.at_level(logging.INFO):
            world.tick()

        assert "World tick: time is now 1" in caplog.text

    def test_tick_logs_correct_time_value(self, caplog):
        """Test that tick() logs the correct time value after multiple ticks."""
        world = WorldState()
        world.tick()  # time = 1
        world.tick()  # time = 2

        with caplog.at_level(logging.INFO):
            world.tick()  # time = 3

        assert "World tick: time is now 3" in caplog.text


class TestWorldStateIndependence:
    """Tests to verify WorldState instances are independent."""

    def test_multiple_world_states_are_independent(self):
        """Test that multiple WorldState instances don't share state."""
        world1 = WorldState()
        world2 = WorldState()

        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world1.add_entity(entity)
        world1.tick()

        assert world1.get_entity("entity_1") is entity
        assert world2.get_entity("entity_1") is None
        assert world1.time == 1
        assert world2.time == 0
