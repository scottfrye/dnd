"""Unit tests for the ActionHandler class.

These tests verify that the ActionHandler:
- Handles move actions correctly
- Handles attack actions correctly
- Handles idle actions correctly
- Integrates with WorldState
- Validates action parameters
"""

import logging

from src.entities.entity import Entity, Position
from src.game.action_handler import ActionHandler
from src.simulation.npc_ai import Action
from src.world.world_state import WorldState


class TestActionHandlerInitialization:
    """Tests for ActionHandler initialization."""

    def test_initialization(self):
        """Test basic initialization."""
        world = WorldState()
        handler = ActionHandler(world)

        assert handler.world is world

    def test_initialization_with_entities(self):
        """Test initialization with a world containing entities."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)

        assert handler.world.get_entity("entity_1") is entity


class TestActionHandlerMoveAction:
    """Tests for handling move actions."""

    def test_handle_move_action_single_step(self):
        """Test moving an entity one step toward target."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=5, y=5, location_id="test")
        action = Action(action_type="move", target_position=target)

        result = handler.handle_action(action, "entity_1")

        assert result is True
        assert entity.position.x == 1
        assert entity.position.y == 1

    def test_handle_move_action_x_axis_only(self):
        """Test moving along x-axis only."""
        world = WorldState()
        pos = Position(x=0, y=5, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=10, y=5, location_id="test")
        action = Action(action_type="move", target_position=target)

        result = handler.handle_action(action, "entity_1")

        assert result is True
        assert entity.position.x == 1
        assert entity.position.y == 5

    def test_handle_move_action_y_axis_only(self):
        """Test moving along y-axis only."""
        world = WorldState()
        pos = Position(x=5, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=5, y=10, location_id="test")
        action = Action(action_type="move", target_position=target)

        result = handler.handle_action(action, "entity_1")

        assert result is True
        assert entity.position.x == 5
        assert entity.position.y == 1

    def test_handle_move_action_negative_direction(self):
        """Test moving in negative direction."""
        world = WorldState()
        pos = Position(x=10, y=10, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=5, y=5, location_id="test")
        action = Action(action_type="move", target_position=target)

        result = handler.handle_action(action, "entity_1")

        assert result is True
        assert entity.position.x == 9
        assert entity.position.y == 9

    def test_handle_move_action_at_target(self):
        """Test moving when already at target position."""
        world = WorldState()
        pos = Position(x=5, y=5, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=5, y=5, location_id="test")
        action = Action(action_type="move", target_position=target)

        result = handler.handle_action(action, "entity_1")

        assert result is True
        assert entity.position.x == 5
        assert entity.position.y == 5

    def test_handle_move_action_without_target_position(self):
        """Test move action without target position returns False."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        action = Action(action_type="move")  # No target_position

        result = handler.handle_action(action, "entity_1")

        assert result is False

    def test_handle_move_action_logs_movement(self, caplog):
        """Test that move action logs the movement."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=3, y=3, location_id="test")
        action = Action(action_type="move", target_position=target)

        with caplog.at_level(logging.DEBUG):
            handler.handle_action(action, "entity_1")

        assert "Entity 'entity_1' moved from (0, 0) to (1, 1)" in caplog.text


class TestActionHandlerAttackAction:
    """Tests for handling attack actions."""

    def test_handle_attack_action_valid_target(self):
        """Test attacking a valid target."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="dungeon")
        pos2 = Position(x=1, y=1, location_id="dungeon")
        attacker = Entity(id="hero", position=pos1)
        target = Entity(id="goblin", position=pos2)
        world.add_entity(attacker)
        world.add_entity(target)

        handler = ActionHandler(world)
        action = Action(action_type="attack", target_entity_id="goblin")

        result = handler.handle_action(action, "hero")

        assert result is True

    def test_handle_attack_action_without_target(self):
        """Test attack action without target entity ID returns False."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        action = Action(action_type="attack")  # No target_entity_id

        result = handler.handle_action(action, "entity_1")

        assert result is False

    def test_handle_attack_action_nonexistent_target(self):
        """Test attacking a nonexistent target returns False."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        action = Action(action_type="attack", target_entity_id="nonexistent")

        result = handler.handle_action(action, "entity_1")

        assert result is False

    def test_handle_attack_action_different_locations(self):
        """Test attacking target in different location returns False."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="room1")
        pos2 = Position(x=0, y=0, location_id="room2")
        attacker = Entity(id="hero", position=pos1)
        target = Entity(id="monster", position=pos2)
        world.add_entity(attacker)
        world.add_entity(target)

        handler = ActionHandler(world)
        action = Action(action_type="attack", target_entity_id="monster")

        result = handler.handle_action(action, "hero")

        assert result is False

    def test_handle_attack_action_logs_attack(self, caplog):
        """Test that attack action logs the attack."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="arena")
        pos2 = Position(x=1, y=1, location_id="arena")
        attacker = Entity(id="fighter", position=pos1)
        target = Entity(id="orc", position=pos2)
        world.add_entity(attacker)
        world.add_entity(target)

        handler = ActionHandler(world)
        action = Action(action_type="attack", target_entity_id="orc")

        with caplog.at_level(logging.INFO):
            handler.handle_action(action, "fighter")

        assert "Entity 'fighter' attacks 'orc'" in caplog.text


class TestActionHandlerIdleAction:
    """Tests for handling idle actions."""

    def test_handle_idle_action(self):
        """Test handling an idle action."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        action = Action(action_type="idle")

        result = handler.handle_action(action, "entity_1")

        assert result is True

    def test_handle_idle_action_does_not_change_position(self):
        """Test that idle action doesn't change entity position."""
        world = WorldState()
        pos = Position(x=5, y=10, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        action = Action(action_type="idle")

        handler.handle_action(action, "entity_1")

        assert entity.position.x == 5
        assert entity.position.y == 10

    def test_handle_idle_action_logs_idle(self, caplog):
        """Test that idle action logs the idle state."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        action = Action(action_type="idle")

        with caplog.at_level(logging.DEBUG):
            handler.handle_action(action, "entity_1")

        assert "Entity 'entity_1' is idle" in caplog.text


class TestActionHandlerErrorHandling:
    """Tests for error handling."""

    def test_handle_action_nonexistent_entity(self):
        """Test handling action for nonexistent entity returns False."""
        world = WorldState()
        handler = ActionHandler(world)
        action = Action(
            action_type="move", target_position=Position(x=0, y=0, location_id="test")
        )

        result = handler.handle_action(action, "nonexistent")

        assert result is False

    def test_handle_action_unknown_action_type(self):
        """Test handling unknown action type returns False."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        action = Action(action_type="unknown_action")

        result = handler.handle_action(action, "entity_1")

        assert result is False

    def test_handle_action_nonexistent_entity_logs_warning(self, caplog):
        """Test that handling action for nonexistent entity logs warning."""
        world = WorldState()
        handler = ActionHandler(world)
        action = Action(action_type="idle")

        with caplog.at_level(logging.WARNING):
            handler.handle_action(action, "missing")

        assert "Cannot handle action: entity 'missing' not found" in caplog.text


class TestActionHandlerIntegration:
    """Integration tests for ActionHandler with WorldState."""

    def test_multiple_moves_toward_target(self):
        """Test multiple move actions moving entity toward target."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=3, y=3, location_id="test")
        action = Action(action_type="move", target_position=target)

        # Move multiple times
        handler.handle_action(action, "entity_1")
        handler.handle_action(action, "entity_1")
        handler.handle_action(action, "entity_1")

        assert entity.position.x == 3
        assert entity.position.y == 3

    def test_action_handler_with_game_tick(self):
        """Test that ActionHandler works correctly with world ticks."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        entity = Entity(id="entity_1", position=pos)
        world.add_entity(entity)

        handler = ActionHandler(world)
        target = Position(x=5, y=0, location_id="test")
        action = Action(action_type="move", target_position=target)

        # Apply action and tick
        handler.handle_action(action, "entity_1")
        world.tick()

        assert entity.position.x == 1
        assert world.time == 1

    def test_multiple_entities_with_actions(self):
        """Test handling actions for multiple entities."""
        world = WorldState()
        pos1 = Position(x=0, y=0, location_id="test")
        pos2 = Position(x=10, y=10, location_id="test")
        entity1 = Entity(id="entity_1", position=pos1)
        entity2 = Entity(id="entity_2", position=pos2)
        world.add_entity(entity1)
        world.add_entity(entity2)

        handler = ActionHandler(world)
        action1 = Action(
            action_type="move", target_position=Position(x=5, y=5, location_id="test")
        )
        action2 = Action(
            action_type="move", target_position=Position(x=5, y=5, location_id="test")
        )

        result1 = handler.handle_action(action1, "entity_1")
        result2 = handler.handle_action(action2, "entity_2")

        assert result1 is True
        assert result2 is True
        assert entity1.position.x == 1
        assert entity1.position.y == 1
        assert entity2.position.x == 9
        assert entity2.position.y == 9
