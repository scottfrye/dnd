"""Unit tests for the NPC AI behavior system.

These tests verify that:
- AI behavior functions accept an NPC and WorldState and return actions
- Idle behavior returns idle actions
- Patrol behavior moves NPCs between waypoints over ticks
- Attack-on-sight behavior detects and targets hostile entities
- Behaviors are decoupled from UI (only use Entity and WorldState)
"""

import pytest

from src.entities.entity import Entity, Position
from src.simulation.npc_ai import (
    Action,
    apply_action,
    attack_on_sight_behavior,
    idle_behavior,
    patrol_behavior,
)
from src.world.world_state import WorldState


class TestAction:
    """Tests for the Action dataclass."""

    def test_create_action_basic(self):
        """Test creating a basic Action."""
        action = Action(action_type="idle")

        assert action.action_type == "idle"
        assert action.target_position is None
        assert action.target_entity_id is None
        assert action.data == {}

    def test_create_action_with_position(self):
        """Test creating an Action with a target position."""
        pos = Position(x=10, y=20, location_id="dungeon")
        action = Action(action_type="move", target_position=pos)

        assert action.action_type == "move"
        assert action.target_position == pos
        assert action.target_position.x == 10
        assert action.target_position.y == 20

    def test_create_action_with_target_entity(self):
        """Test creating an Action with a target entity."""
        action = Action(action_type="attack", target_entity_id="enemy_001")

        assert action.action_type == "attack"
        assert action.target_entity_id == "enemy_001"

    def test_create_action_with_data(self):
        """Test creating an Action with additional data."""
        action = Action(action_type="cast_spell", data={"spell": "fireball", "level": 3})

        assert action.action_type == "cast_spell"
        assert action.data["spell"] == "fireball"
        assert action.data["level"] == 3


class TestIdleBehavior:
    """Tests for the idle behavior function."""

    def test_idle_behavior_returns_idle_action(self):
        """Test that idle behavior returns an idle action."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(id="npc_001", position=pos)

        action = idle_behavior(npc, world)

        assert action.action_type == "idle"

    def test_idle_behavior_with_any_npc_state(self):
        """Test that idle behavior works regardless of NPC state."""
        world = WorldState()
        pos = Position(x=5, y=10, location_id="dungeon")
        npc = Entity(
            id="npc_002",
            position=pos,
            properties={"hp": 20, "level": 5, "hostile": True},
        )

        action = idle_behavior(npc, world)

        assert action.action_type == "idle"

    def test_idle_behavior_does_not_modify_npc(self):
        """Test that idle behavior does not modify the NPC."""
        world = WorldState()
        pos = Position(x=3, y=7, location_id="test")
        npc = Entity(id="npc_003", position=pos, properties={"state": "calm"})
        original_x = npc.position.x
        original_y = npc.position.y
        original_properties = npc.properties.copy()

        idle_behavior(npc, world)

        assert npc.position.x == original_x
        assert npc.position.y == original_y
        assert npc.properties == original_properties


class TestPatrolBehavior:
    """Tests for the patrol behavior function."""

    def test_patrol_with_no_waypoints_returns_idle(self):
        """Test that patrol behavior returns idle when no waypoints are defined."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(id="npc_patrol_001", position=pos)

        action = patrol_behavior(npc, world)

        assert action.action_type == "idle"

    def test_patrol_moves_toward_first_waypoint(self):
        """Test that patrol behavior moves toward the first waypoint."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        waypoint1 = Position(x=10, y=10, location_id="test")
        waypoint2 = Position(x=20, y=20, location_id="test")
        npc = Entity(
            id="npc_patrol_002",
            position=pos,
            properties={"waypoints": [waypoint1, waypoint2], "current_waypoint_index": 0},
        )

        action = patrol_behavior(npc, world)

        assert action.action_type == "move"
        assert action.target_position == waypoint1
        assert action.data["waypoint_index"] == 0

    def test_patrol_advances_to_next_waypoint_on_arrival(self):
        """Test that patrol behavior advances to next waypoint when current is reached."""
        world = WorldState()
        waypoint1 = Position(x=10, y=10, location_id="test")
        waypoint2 = Position(x=20, y=20, location_id="test")
        # NPC is already at waypoint1
        pos = Position(x=10, y=10, location_id="test")
        npc = Entity(
            id="npc_patrol_003",
            position=pos,
            properties={"waypoints": [waypoint1, waypoint2], "current_waypoint_index": 0},
        )

        action = patrol_behavior(npc, world)

        # Should advance to waypoint2
        assert action.action_type == "move"
        assert action.target_position == waypoint2
        assert npc.properties["current_waypoint_index"] == 1

    def test_patrol_wraps_around_to_first_waypoint(self):
        """Test that patrol behavior wraps around to first waypoint after last."""
        world = WorldState()
        waypoint1 = Position(x=10, y=10, location_id="test")
        waypoint2 = Position(x=20, y=20, location_id="test")
        waypoint3 = Position(x=30, y=30, location_id="test")
        # NPC is at waypoint3 (last waypoint)
        pos = Position(x=30, y=30, location_id="test")
        npc = Entity(
            id="npc_patrol_004",
            position=pos,
            properties={
                "waypoints": [waypoint1, waypoint2, waypoint3],
                "current_waypoint_index": 2,
            },
        )

        action = patrol_behavior(npc, world)

        # Should wrap to waypoint1
        assert action.action_type == "move"
        assert action.target_position == waypoint1
        assert npc.properties["current_waypoint_index"] == 0

    def test_patrol_behavior_over_multiple_ticks(self):
        """Test that patrol behavior moves NPC between waypoints over multiple ticks."""
        world = WorldState()
        waypoint1 = Position(x=3, y=0, location_id="test")
        waypoint2 = Position(x=0, y=0, location_id="test")
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_patrol_005",
            position=pos,
            properties={"waypoints": [waypoint1, waypoint2], "current_waypoint_index": 0},
        )
        world.add_entity(npc)

        # Tick 1: At waypoint2, should move toward waypoint1
        action = patrol_behavior(npc, world)
        assert action.action_type == "move"
        assert action.target_position == waypoint1
        apply_action(action, npc, world)
        assert npc.position.x == 1  # Moved one step toward x=3

        # Tick 2: Continue moving toward waypoint1
        action = patrol_behavior(npc, world)
        assert action.action_type == "move"
        apply_action(action, npc, world)
        assert npc.position.x == 2

        # Tick 3: Continue moving toward waypoint1
        action = patrol_behavior(npc, world)
        assert action.action_type == "move"
        apply_action(action, npc, world)
        assert npc.position.x == 3  # Reached waypoint1

        # Tick 4: At waypoint1, should advance to waypoint2
        action = patrol_behavior(npc, world)
        assert action.action_type == "move"
        assert action.target_position == waypoint2
        assert npc.properties["current_waypoint_index"] == 1
        apply_action(action, npc, world)
        assert npc.position.x == 2  # Moving back toward x=0

    def test_patrol_initializes_waypoint_index_if_missing(self):
        """Test that patrol behavior initializes waypoint index if not present."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        waypoint1 = Position(x=5, y=5, location_id="test")
        npc = Entity(
            id="npc_patrol_006",
            position=pos,
            properties={"waypoints": [waypoint1]},
        )

        action = patrol_behavior(npc, world)

        assert action.action_type == "move"
        assert action.target_position == waypoint1
        # Index defaults to 0
        assert action.data["waypoint_index"] == 0


class TestAttackOnSightBehavior:
    """Tests for the attack-on-sight behavior function."""

    def test_attack_on_sight_with_no_targets_returns_idle(self):
        """Test that attack-on-sight returns idle when no targets are present."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_attack_001",
            position=pos,
            properties={"detection_range": 5, "hostile_to": ["player"]},
        )
        world.add_entity(npc)

        action = attack_on_sight_behavior(npc, world)

        assert action.action_type == "idle"

    def test_attack_on_sight_detects_hostile_target(self):
        """Test that attack-on-sight detects and targets hostile entities."""
        world = WorldState()
        npc_pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_attack_002",
            position=npc_pos,
            properties={"detection_range": 5, "hostile_to": ["player"]},
        )
        world.add_entity(npc)

        # Add a hostile target within range
        player_pos = Position(x=3, y=0, location_id="test")
        player = Entity(id="player_001", position=player_pos, properties={"type": "player"})
        world.add_entity(player)

        action = attack_on_sight_behavior(npc, world)

        assert action.action_type == "attack"
        assert action.target_entity_id == "player_001"
        assert action.data["distance"] == 3

    def test_attack_on_sight_ignores_targets_out_of_range(self):
        """Test that attack-on-sight ignores targets beyond detection range."""
        world = WorldState()
        npc_pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_attack_003",
            position=npc_pos,
            properties={"detection_range": 3, "hostile_to": ["player"]},
        )
        world.add_entity(npc)

        # Add a hostile target out of range
        player_pos = Position(x=5, y=0, location_id="test")
        player = Entity(id="player_002", position=player_pos, properties={"type": "player"})
        world.add_entity(player)

        action = attack_on_sight_behavior(npc, world)

        assert action.action_type == "idle"

    def test_attack_on_sight_ignores_non_hostile_entities(self):
        """Test that attack-on-sight ignores non-hostile entity types."""
        world = WorldState()
        npc_pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_attack_004",
            position=npc_pos,
            properties={"detection_range": 5, "hostile_to": ["player"]},
        )
        world.add_entity(npc)

        # Add a non-hostile entity within range
        friendly_pos = Position(x=2, y=0, location_id="test")
        friendly = Entity(
            id="friendly_001", position=friendly_pos, properties={"type": "merchant"}
        )
        world.add_entity(friendly)

        action = attack_on_sight_behavior(npc, world)

        assert action.action_type == "idle"

    def test_attack_on_sight_targets_closest_enemy(self):
        """Test that attack-on-sight targets the closest hostile entity."""
        world = WorldState()
        npc_pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_attack_005",
            position=npc_pos,
            properties={"detection_range": 10, "hostile_to": ["player"]},
        )
        world.add_entity(npc)

        # Add two hostile targets at different distances
        player1_pos = Position(x=5, y=0, location_id="test")
        player1 = Entity(id="player_003", position=player1_pos, properties={"type": "player"})
        world.add_entity(player1)

        player2_pos = Position(x=2, y=0, location_id="test")
        player2 = Entity(id="player_004", position=player2_pos, properties={"type": "player"})
        world.add_entity(player2)

        action = attack_on_sight_behavior(npc, world)

        # Should target the closer player
        assert action.action_type == "attack"
        assert action.target_entity_id == "player_004"
        assert action.data["distance"] == 2

    def test_attack_on_sight_ignores_different_locations(self):
        """Test that attack-on-sight ignores entities in different locations."""
        world = WorldState()
        npc_pos = Position(x=0, y=0, location_id="dungeon_level_1")
        npc = Entity(
            id="npc_attack_006",
            position=npc_pos,
            properties={"detection_range": 5, "hostile_to": ["player"]},
        )
        world.add_entity(npc)

        # Add a hostile target in a different location
        player_pos = Position(x=2, y=0, location_id="dungeon_level_2")
        player = Entity(id="player_005", position=player_pos, properties={"type": "player"})
        world.add_entity(player)

        action = attack_on_sight_behavior(npc, world)

        assert action.action_type == "idle"

    def test_attack_on_sight_uses_default_detection_range(self):
        """Test that attack-on-sight uses default detection range if not specified."""
        world = WorldState()
        npc_pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_attack_007",
            position=npc_pos,
            properties={"hostile_to": ["player"]},
            # No detection_range specified
        )
        world.add_entity(npc)

        # Add a hostile target at distance 5 (default range)
        player_pos = Position(x=5, y=0, location_id="test")
        player = Entity(id="player_006", position=player_pos, properties={"type": "player"})
        world.add_entity(player)

        action = attack_on_sight_behavior(npc, world)

        # Should detect with default range of 5
        assert action.action_type == "attack"

    def test_attack_on_sight_uses_default_hostile_list(self):
        """Test that attack-on-sight uses default hostile list if not specified."""
        world = WorldState()
        npc_pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="npc_attack_008",
            position=npc_pos,
            properties={"detection_range": 5},
            # No hostile_to specified
        )
        world.add_entity(npc)

        # Add a player (default hostile type)
        player_pos = Position(x=3, y=0, location_id="test")
        player = Entity(id="player_007", position=player_pos, properties={"type": "player"})
        world.add_entity(player)

        action = attack_on_sight_behavior(npc, world)

        # Should detect player with default hostile list
        assert action.action_type == "attack"


class TestApplyAction:
    """Tests for the apply_action helper function."""

    def test_apply_move_action_toward_target(self):
        """Test that apply_action moves NPC one step toward target."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(id="npc_move_001", position=pos)
        target = Position(x=5, y=3, location_id="test")
        action = Action(action_type="move", target_position=target)

        apply_action(action, npc, world)

        # Should move one step toward target
        assert npc.position.x == 1
        assert npc.position.y == 1

    def test_apply_move_action_single_axis(self):
        """Test that apply_action can move along a single axis."""
        world = WorldState()
        pos = Position(x=0, y=5, location_id="test")
        npc = Entity(id="npc_move_002", position=pos)
        target = Position(x=10, y=5, location_id="test")
        action = Action(action_type="move", target_position=target)

        apply_action(action, npc, world)

        # Should move only in x direction
        assert npc.position.x == 1
        assert npc.position.y == 5

    def test_apply_move_action_backward(self):
        """Test that apply_action can move backward (negative direction)."""
        world = WorldState()
        pos = Position(x=10, y=10, location_id="test")
        npc = Entity(id="npc_move_003", position=pos)
        target = Position(x=5, y=3, location_id="test")
        action = Action(action_type="move", target_position=target)

        apply_action(action, npc, world)

        # Should move one step toward target (both negative)
        assert npc.position.x == 9
        assert npc.position.y == 9

    def test_apply_move_action_at_target_no_movement(self):
        """Test that apply_action does not move when already at target."""
        world = WorldState()
        pos = Position(x=5, y=5, location_id="test")
        npc = Entity(id="npc_move_004", position=pos)
        target = Position(x=5, y=5, location_id="test")
        action = Action(action_type="move", target_position=target)

        apply_action(action, npc, world)

        # Should not move
        assert npc.position.x == 5
        assert npc.position.y == 5

    def test_apply_idle_action_does_nothing(self):
        """Test that apply_action does nothing for idle actions."""
        world = WorldState()
        pos = Position(x=3, y=7, location_id="test")
        npc = Entity(id="npc_idle_001", position=pos)
        action = Action(action_type="idle")

        original_x = npc.position.x
        original_y = npc.position.y

        apply_action(action, npc, world)

        # Position should not change
        assert npc.position.x == original_x
        assert npc.position.y == original_y

    def test_apply_attack_action_does_not_move_npc(self):
        """Test that apply_action does not move NPC for attack actions."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(id="npc_attack_001", position=pos)
        action = Action(action_type="attack", target_entity_id="enemy_001")

        original_x = npc.position.x
        original_y = npc.position.y

        apply_action(action, npc, world)

        # Position should not change for attack
        assert npc.position.x == original_x
        assert npc.position.y == original_y


class TestBehaviorDecoupling:
    """Tests to verify behaviors are decoupled from UI and can run headless."""

    def test_behaviors_only_use_entity_and_worldstate(self):
        """Test that all behaviors only depend on Entity and WorldState."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(id="npc_decoupled", position=pos, properties={"waypoints": []})

        # Should be able to call all behaviors with just Entity and WorldState
        idle_action = idle_behavior(npc, world)
        patrol_action = patrol_behavior(npc, world)
        attack_action = attack_on_sight_behavior(npc, world)

        assert idle_action is not None
        assert patrol_action is not None
        assert attack_action is not None

    def test_behaviors_return_action_objects(self):
        """Test that all behaviors return Action objects."""
        world = WorldState()
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(id="npc_action", position=pos)

        idle_action = idle_behavior(npc, world)
        patrol_action = patrol_behavior(npc, world)
        attack_action = attack_on_sight_behavior(npc, world)

        assert isinstance(idle_action, Action)
        assert isinstance(patrol_action, Action)
        assert isinstance(attack_action, Action)

    def test_simulation_can_run_headless(self):
        """Test that a simple simulation can run without UI."""
        world = WorldState()

        # Create an NPC with patrol behavior
        waypoint1 = Position(x=2, y=0, location_id="test")
        waypoint2 = Position(x=0, y=0, location_id="test")
        pos = Position(x=0, y=0, location_id="test")
        npc = Entity(
            id="patrol_npc",
            position=pos,
            properties={"waypoints": [waypoint1, waypoint2], "current_waypoint_index": 0},
        )
        world.add_entity(npc)

        # Simulate several ticks
        for i in range(5):
            world.tick()
            action = patrol_behavior(npc, world)
            apply_action(action, npc, world)

        # NPC should have moved
        assert npc.position.x > 0 or npc.properties["current_waypoint_index"] > 0
