"""Unit tests for the Entity base class.

These tests verify that the Entity base class correctly:
- Stores id, position (x, y, location_id), and properties
- Allows setting and getting properties
- Serializes to a dictionary via to_dict()
"""

import pytest

from src.entities.entity import Entity, Position


class TestPosition:
    """Tests for the Position dataclass."""

    def test_create_position(self):
        """Test creating a valid Position instance."""
        pos = Position(x=5, y=10, location_id="dungeon_level_1")

        assert pos.x == 5
        assert pos.y == 10
        assert pos.location_id == "dungeon_level_1"

    def test_position_with_negative_coordinates(self):
        """Test creating a Position with negative coordinates."""
        pos = Position(x=-3, y=-7, location_id="underground")

        assert pos.x == -3
        assert pos.y == -7

    def test_position_at_origin(self):
        """Test creating a Position at the origin."""
        pos = Position(x=0, y=0, location_id="start")

        assert pos.x == 0
        assert pos.y == 0


class TestEntity:
    """Tests for the Entity base class."""

    def test_create_entity(self):
        """Test creating a basic Entity with id and position."""
        pos = Position(x=10, y=20, location_id="town_square")
        entity = Entity(id="entity_001", position=pos)

        assert entity.id == "entity_001"
        assert entity.position.x == 10
        assert entity.position.y == 20
        assert entity.position.location_id == "town_square"

    def test_entity_default_properties(self):
        """Test that Entity has empty properties dict by default."""
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test_entity", position=pos)

        assert entity.properties == {}

    def test_entity_with_initial_properties(self):
        """Test creating an Entity with initial properties."""
        pos = Position(x=5, y=5, location_id="dungeon")
        props = {"name": "Goblin", "hp": 7, "hostile": True}
        entity = Entity(id="goblin_001", position=pos, properties=props)

        assert entity.properties["name"] == "Goblin"
        assert entity.properties["hp"] == 7
        assert entity.properties["hostile"] is True

    def test_entity_set_property(self):
        """Test setting a property on an Entity."""
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test_entity", position=pos)

        entity.properties["strength"] = 15

        assert entity.properties["strength"] == 15

    def test_entity_get_property(self):
        """Test getting a property from an Entity."""
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test_entity", position=pos, properties={"level": 3})

        level = entity.properties.get("level")

        assert level == 3

    def test_entity_get_missing_property_returns_none(self):
        """Test getting a missing property returns None with .get()."""
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test_entity", position=pos)

        result = entity.properties.get("nonexistent")

        assert result is None

    def test_entity_update_property(self):
        """Test updating an existing property."""
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test_entity", position=pos, properties={"hp": 10})

        entity.properties["hp"] = 8

        assert entity.properties["hp"] == 8


class TestEntitySerialization:
    """Tests for Entity to_dict() serialization."""

    def test_to_dict_basic(self):
        """Test to_dict() with basic Entity."""
        pos = Position(x=5, y=10, location_id="temple")
        entity = Entity(id="entity_123", position=pos)

        result = entity.to_dict()

        assert result["id"] == "entity_123"
        assert result["position"]["x"] == 5
        assert result["position"]["y"] == 10
        assert result["position"]["location_id"] == "temple"
        assert result["properties"] == {}

    def test_to_dict_with_properties(self):
        """Test to_dict() with properties."""
        pos = Position(x=0, y=0, location_id="test")
        props = {"name": "Orc Warrior", "hp": 15, "ac": 6}
        entity = Entity(id="orc_001", position=pos, properties=props)

        result = entity.to_dict()

        assert result["properties"]["name"] == "Orc Warrior"
        assert result["properties"]["hp"] == 15
        assert result["properties"]["ac"] == 6

    def test_to_dict_returns_copy_of_properties(self):
        """Test that to_dict() returns a copy of properties, not the original."""
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="test", position=pos, properties={"value": 100})

        result = entity.to_dict()
        result["properties"]["value"] = 999

        # Original entity properties should be unchanged
        assert entity.properties["value"] == 100

    def test_to_dict_structure(self):
        """Test the overall structure of to_dict() output."""
        pos = Position(x=1, y=2, location_id="loc")
        entity = Entity(id="e1", position=pos, properties={"key": "val"})

        result = entity.to_dict()

        assert set(result.keys()) == {"id", "position", "properties"}
        assert set(result["position"].keys()) == {"x", "y", "location_id"}

    def test_to_dict_with_complex_properties(self):
        """Test to_dict() with nested/complex property values."""
        pos = Position(x=0, y=0, location_id="test")
        props = {
            "inventory": ["sword", "shield"],
            "stats": {"str": 16, "dex": 14},
            "active": True,
        }
        entity = Entity(id="complex_entity", position=pos, properties=props)

        result = entity.to_dict()

        assert result["properties"]["inventory"] == ["sword", "shield"]
        assert result["properties"]["stats"] == {"str": 16, "dex": 14}
        assert result["properties"]["active"] is True


class TestEntityIndependence:
    """Tests to verify entity instances are independent."""

    def test_entity_properties_are_independent(self):
        """Test that different Entity instances have independent properties."""
        pos1 = Position(x=0, y=0, location_id="test")
        pos2 = Position(x=1, y=1, location_id="test")
        entity1 = Entity(id="e1", position=pos1)
        entity2 = Entity(id="e2", position=pos2)

        entity1.properties["key"] = "value1"
        entity2.properties["key"] = "value2"

        assert entity1.properties["key"] == "value1"
        assert entity2.properties["key"] == "value2"
