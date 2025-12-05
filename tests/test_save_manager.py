"""Unit tests for the save_manager module.

These tests verify that the save_manager correctly:
- Serializes WorldState to YAML and JSON
- Deserializes WorldState from YAML and JSON
- Performs round-trip save/load with entity counts and time preservation
- Handles errors appropriately
"""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from src.entities.entity import Entity, Position
from src.persistence import save_manager
from src.world.world_state import WorldState


class TestEntitySerialization:
    """Tests for Entity serialization/deserialization."""

    def test_entity_from_dict_basic(self):
        """Test deserializing a basic entity from dict."""
        data = {
            "id": "entity_1",
            "position": {"x": 10, "y": 20, "location_id": "dungeon"},
            "properties": {},
        }

        entity = Entity.from_dict(data)

        assert entity.id == "entity_1"
        assert entity.position.x == 10
        assert entity.position.y == 20
        assert entity.position.location_id == "dungeon"
        assert entity.properties == {}

    def test_entity_from_dict_with_properties(self):
        """Test deserializing an entity with properties."""
        data = {
            "id": "goblin_1",
            "position": {"x": 5, "y": 5, "location_id": "cave"},
            "properties": {"hp": 7, "name": "Goblin Scout", "hostile": True},
        }

        entity = Entity.from_dict(data)

        assert entity.id == "goblin_1"
        assert entity.properties["hp"] == 7
        assert entity.properties["name"] == "Goblin Scout"
        assert entity.properties["hostile"] is True

    def test_entity_roundtrip(self):
        """Test that entity can be serialized and deserialized."""
        pos = Position(x=15, y=25, location_id="temple")
        original = Entity(
            id="test_entity", position=pos, properties={"level": 5, "name": "Hero"}
        )

        data = original.to_dict()
        restored = Entity.from_dict(data)

        assert restored.id == original.id
        assert restored.position.x == original.position.x
        assert restored.position.y == original.position.y
        assert restored.position.location_id == original.position.location_id
        assert restored.properties == original.properties


class TestWorldStateSerialization:
    """Tests for WorldState serialization/deserialization."""

    def test_world_state_to_dict_empty(self):
        """Test serializing an empty WorldState."""
        world = WorldState()

        data = world.to_dict()

        assert data["time"] == 0
        assert data["entities"] == []

    def test_world_state_to_dict_with_time(self):
        """Test serializing a WorldState with advanced time."""
        world = WorldState()
        world.tick()
        world.tick()
        world.tick()

        data = world.to_dict()

        assert data["time"] == 3

    def test_world_state_to_dict_with_entities(self):
        """Test serializing a WorldState with entities."""
        world = WorldState()
        pos1 = Position(x=1, y=2, location_id="loc1")
        pos2 = Position(x=3, y=4, location_id="loc2")
        entity1 = Entity(id="e1", position=pos1)
        entity2 = Entity(id="e2", position=pos2)
        world.add_entity(entity1)
        world.add_entity(entity2)

        data = world.to_dict()

        assert len(data["entities"]) == 2
        assert any(e["id"] == "e1" for e in data["entities"])
        assert any(e["id"] == "e2" for e in data["entities"])

    def test_world_state_from_dict_empty(self):
        """Test deserializing an empty WorldState."""
        data = {"time": 0, "entities": []}

        world = WorldState.from_dict(data)

        assert world.time == 0
        assert world.get_all_entity_ids() == []

    def test_world_state_from_dict_with_time(self):
        """Test deserializing a WorldState with time."""
        data = {"time": 42, "entities": []}

        world = WorldState.from_dict(data)

        assert world.time == 42

    def test_world_state_from_dict_with_entities(self):
        """Test deserializing a WorldState with entities."""
        data = {
            "time": 5,
            "entities": [
                {
                    "id": "entity_1",
                    "position": {"x": 10, "y": 20, "location_id": "loc"},
                    "properties": {"hp": 100},
                },
                {
                    "id": "entity_2",
                    "position": {"x": 30, "y": 40, "location_id": "loc"},
                    "properties": {},
                },
            ],
        }

        world = WorldState.from_dict(data)

        assert world.time == 5
        assert len(world.get_all_entity_ids()) == 2
        entity1 = world.get_entity("entity_1")
        assert entity1 is not None
        assert entity1.properties["hp"] == 100
        entity2 = world.get_entity("entity_2")
        assert entity2 is not None

    def test_world_state_roundtrip(self):
        """Test that WorldState can be serialized and deserialized."""
        original = WorldState()
        original.tick()
        original.tick()
        pos1 = Position(x=5, y=10, location_id="dungeon")
        pos2 = Position(x=15, y=20, location_id="temple")
        entity1 = Entity(id="e1", position=pos1, properties={"name": "Hero"})
        entity2 = Entity(id="e2", position=pos2, properties={"name": "Monster"})
        original.add_entity(entity1)
        original.add_entity(entity2)

        data = original.to_dict()
        restored = WorldState.from_dict(data)

        assert restored.time == original.time
        assert len(restored.get_all_entity_ids()) == len(original.get_all_entity_ids())
        for entity_id in original.get_all_entity_ids():
            original_entity = original.get_entity(entity_id)
            restored_entity = restored.get_entity(entity_id)
            assert restored_entity is not None
            assert restored_entity.id == original_entity.id
            assert restored_entity.position.x == original_entity.position.x
            assert restored_entity.position.y == original_entity.position.y


class TestSaveManagerYAML:
    """Tests for save_manager YAML functionality."""

    def test_save_yaml_basic(self):
        """Test saving a WorldState to YAML."""
        world = WorldState()
        world.tick()
        pos = Position(x=10, y=20, location_id="temple")
        entity = Entity(id="entity_1", position=pos, properties={"hp": 50})
        world.add_entity(entity)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)

        try:
            save_manager.save(world, temp_path, format="yaml")

            assert temp_path.exists()
            with open(temp_path, "r") as f:
                data = yaml.safe_load(f)

            assert data["time"] == 1
            assert len(data["entities"]) == 1
            assert data["entities"][0]["id"] == "entity_1"
        finally:
            temp_path.unlink(missing_ok=True)

    def test_load_yaml_basic(self):
        """Test loading a WorldState from YAML."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            temp_path = Path(f.name)
            yaml.safe_dump(
                {
                    "time": 10,
                    "entities": [
                        {
                            "id": "test_entity",
                            "position": {"x": 5, "y": 15, "location_id": "dungeon"},
                            "properties": {"name": "TestEntity"},
                        }
                    ],
                },
                f,
            )

        try:
            world = save_manager.load(temp_path)

            assert world.time == 10
            assert len(world.get_all_entity_ids()) == 1
            entity = world.get_entity("test_entity")
            assert entity is not None
            assert entity.position.x == 5
            assert entity.properties["name"] == "TestEntity"
        finally:
            temp_path.unlink(missing_ok=True)

    def test_yaml_roundtrip(self):
        """Test round-trip save and load with YAML format."""
        original = WorldState()
        original.tick()
        original.tick()
        original.tick()
        pos1 = Position(x=1, y=2, location_id="location_a")
        pos2 = Position(x=3, y=4, location_id="location_b")
        pos3 = Position(x=5, y=6, location_id="location_c")
        entity1 = Entity(id="entity_1", position=pos1, properties={"type": "player"})
        entity2 = Entity(id="entity_2", position=pos2, properties={"type": "npc"})
        entity3 = Entity(id="entity_3", position=pos3, properties={"type": "monster"})
        original.add_entity(entity1)
        original.add_entity(entity2)
        original.add_entity(entity3)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)

        try:
            save_manager.save(original, temp_path, format="yaml")
            restored = save_manager.load(temp_path)

            # Verify time
            assert restored.time == original.time
            # Verify entity count
            assert len(restored.get_all_entity_ids()) == len(
                original.get_all_entity_ids()
            )
            # Verify each entity
            for entity_id in original.get_all_entity_ids():
                orig_entity = original.get_entity(entity_id)
                rest_entity = restored.get_entity(entity_id)
                assert rest_entity is not None
                assert rest_entity.id == orig_entity.id
                assert rest_entity.position.x == orig_entity.position.x
                assert rest_entity.position.y == orig_entity.position.y
                assert rest_entity.position.location_id == orig_entity.position.location_id
                assert rest_entity.properties == orig_entity.properties
        finally:
            temp_path.unlink(missing_ok=True)


class TestSaveManagerJSON:
    """Tests for save_manager JSON functionality."""

    def test_save_json_basic(self):
        """Test saving a WorldState to JSON."""
        world = WorldState()
        world.tick()
        world.tick()
        pos = Position(x=10, y=20, location_id="temple")
        entity = Entity(id="entity_1", position=pos, properties={"hp": 50})
        world.add_entity(entity)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        try:
            save_manager.save(world, temp_path, format="json")

            assert temp_path.exists()
            with open(temp_path, "r") as f:
                data = json.load(f)

            assert data["time"] == 2
            assert len(data["entities"]) == 1
            assert data["entities"][0]["id"] == "entity_1"
        finally:
            temp_path.unlink(missing_ok=True)

    def test_load_json_basic(self):
        """Test loading a WorldState from JSON."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            temp_path = Path(f.name)
            json.dump(
                {
                    "time": 20,
                    "entities": [
                        {
                            "id": "json_entity",
                            "position": {"x": 7, "y": 14, "location_id": "cave"},
                            "properties": {"name": "JsonEntity"},
                        }
                    ],
                },
                f,
            )

        try:
            world = save_manager.load(temp_path)

            assert world.time == 20
            assert len(world.get_all_entity_ids()) == 1
            entity = world.get_entity("json_entity")
            assert entity is not None
            assert entity.position.x == 7
            assert entity.properties["name"] == "JsonEntity"
        finally:
            temp_path.unlink(missing_ok=True)

    def test_json_roundtrip(self):
        """Test round-trip save and load with JSON format."""
        original = WorldState()
        for _ in range(5):
            original.tick()
        pos1 = Position(x=10, y=20, location_id="loc1")
        pos2 = Position(x=30, y=40, location_id="loc2")
        entity1 = Entity(id="json_e1", position=pos1, properties={"hp": 100})
        entity2 = Entity(id="json_e2", position=pos2, properties={"hp": 200})
        original.add_entity(entity1)
        original.add_entity(entity2)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        try:
            save_manager.save(original, temp_path, format="json")
            restored = save_manager.load(temp_path)

            # Verify time
            assert restored.time == original.time
            # Verify entity count
            assert len(restored.get_all_entity_ids()) == len(
                original.get_all_entity_ids()
            )
            # Verify each entity
            for entity_id in original.get_all_entity_ids():
                orig_entity = original.get_entity(entity_id)
                rest_entity = restored.get_entity(entity_id)
                assert rest_entity is not None
                assert rest_entity.id == orig_entity.id
                assert rest_entity.position.x == orig_entity.position.x
                assert rest_entity.position.y == orig_entity.position.y
                assert rest_entity.position.location_id == orig_entity.position.location_id
                assert rest_entity.properties == orig_entity.properties
        finally:
            temp_path.unlink(missing_ok=True)


class TestSaveManagerErrors:
    """Tests for save_manager error handling."""

    def test_save_unsupported_format(self):
        """Test that unsupported format raises ValueError."""
        world = WorldState()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="Unsupported format"):
                save_manager.save(world, temp_path, format="xml")
        finally:
            temp_path.unlink(missing_ok=True)

    def test_load_nonexistent_file(self):
        """Test that loading a nonexistent file raises FileNotFoundError."""
        nonexistent_path = Path("/tmp/nonexistent_file_12345.yaml")

        with pytest.raises(FileNotFoundError):
            save_manager.load(nonexistent_path)

    def test_load_auto_detects_yaml_by_extension(self):
        """Test that .yaml extension is auto-detected."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            temp_path = Path(f.name)
            yaml.safe_dump({"time": 7, "entities": []}, f)

        try:
            world = save_manager.load(temp_path)
            assert world.time == 7
        finally:
            temp_path.unlink(missing_ok=True)

    def test_load_auto_detects_json_by_extension(self):
        """Test that .json extension is auto-detected."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            temp_path = Path(f.name)
            json.dump({"time": 9, "entities": []}, f)

        try:
            world = save_manager.load(temp_path)
            assert world.time == 9
        finally:
            temp_path.unlink(missing_ok=True)


class TestAcceptanceCriteria:
    """Tests that verify the specific acceptance criteria from the issue."""

    def test_save_serializes_to_yaml(self):
        """Acceptance: save_manager.save(world_state, path) serializes state to YAML."""
        world = WorldState()
        world.tick()
        pos = Position(x=5, y=10, location_id="test_loc")
        entity = Entity(id="test_entity", position=pos, properties={"test": "value"})
        world.add_entity(entity)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)

        try:
            save_manager.save(world, temp_path, format="yaml")

            # Verify file exists and contains YAML
            assert temp_path.exists()
            with open(temp_path, "r") as f:
                content = f.read()
                assert "time:" in content or "time :" in content
                assert "entities:" in content or "entities :" in content
        finally:
            temp_path.unlink(missing_ok=True)

    def test_load_restores_basic_world_state(self):
        """Acceptance: save_manager.load(path) restores basic WorldState objects (entity list, time)."""
        # Create a YAML file with known data
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            temp_path = Path(f.name)
            yaml.safe_dump(
                {
                    "time": 15,
                    "entities": [
                        {
                            "id": "entity_a",
                            "position": {"x": 1, "y": 2, "location_id": "loc"},
                            "properties": {},
                        },
                        {
                            "id": "entity_b",
                            "position": {"x": 3, "y": 4, "location_id": "loc"},
                            "properties": {},
                        },
                    ],
                },
                f,
            )

        try:
            world = save_manager.load(temp_path)

            # Verify entity list is restored
            assert len(world.get_all_entity_ids()) == 2
            assert "entity_a" in world.get_all_entity_ids()
            assert "entity_b" in world.get_all_entity_ids()
            # Verify time is restored
            assert world.time == 15
        finally:
            temp_path.unlink(missing_ok=True)

    def test_roundtrip_preserves_entity_count_and_time(self):
        """Acceptance: Round-trip test: save then load and verify entity counts and world time."""
        # Create original world state
        original = WorldState()
        # Set specific time
        for _ in range(7):
            original.tick()
        # Add specific number of entities
        for i in range(4):
            pos = Position(x=i * 10, y=i * 20, location_id=f"loc_{i}")
            entity = Entity(
                id=f"entity_{i}", position=pos, properties={"index": i}
            )
            original.add_entity(entity)

        original_time = original.time
        original_entity_count = len(original.get_all_entity_ids())

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Save to file
            save_manager.save(original, temp_path, format="yaml")
            # Load from file
            restored = save_manager.load(temp_path)

            # Verify entity count matches
            assert len(restored.get_all_entity_ids()) == original_entity_count
            # Verify world time matches
            assert restored.time == original_time
            # Also verify all entity IDs are present
            for entity_id in original.get_all_entity_ids():
                assert entity_id in restored.get_all_entity_ids()
        finally:
            temp_path.unlink(missing_ok=True)
