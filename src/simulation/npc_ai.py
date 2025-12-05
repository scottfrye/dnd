"""NPC AI behavior system.

This module provides AI behavior functions for NPCs that can run in headless
simulation mode. Behaviors accept an NPC entity and WorldState and return
actions that can be applied to the world.
"""

from dataclasses import dataclass
from typing import Optional

from src.entities.entity import Entity, Position
from src.world.world_state import WorldState


@dataclass
class Action:
    """Represents an action that an NPC can take.

    Attributes:
        action_type: The type of action (e.g., "move", "attack", "idle").
        target_position: Optional position for movement actions.
        target_entity_id: Optional target entity id for attack actions.
        data: Additional action-specific data.
    """

    action_type: str
    target_position: Optional[Position] = None
    target_entity_id: Optional[str] = None
    data: Optional[dict] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.data is None:
            self.data = {}


def idle_behavior(npc: Entity, world: WorldState) -> Action:
    """Simple idle behavior - NPC does nothing.

    Args:
        npc: The NPC entity to generate behavior for.
        world: The current world state.

    Returns:
        An idle action.
    """
    return Action(action_type="idle")


def patrol_behavior(npc: Entity, world: WorldState) -> Action:
    """Patrol behavior - NPC moves between waypoints.

    The NPC moves between a list of waypoints stored in its properties.
    When it reaches a waypoint, it advances to the next one in the list,
    wrapping around to the beginning when reaching the end.

    Expected NPC properties:
        waypoints: List of Position objects defining the patrol route.
        current_waypoint_index: Integer index of the current target waypoint.

    Args:
        npc: The NPC entity to generate behavior for.
        world: The current world state.

    Returns:
        A move action toward the current waypoint, or idle if no waypoints.
    """
    waypoints = npc.properties.get("waypoints", [])
    if not waypoints:
        return Action(action_type="idle")

    current_index = npc.properties.get("current_waypoint_index", 0)
    target_waypoint = waypoints[current_index]

    # Check if NPC has reached the current waypoint
    if (
        npc.position.x == target_waypoint.x
        and npc.position.y == target_waypoint.y
        and npc.position.location_id == target_waypoint.location_id
    ):
        # Advance to next waypoint
        next_index = (current_index + 1) % len(waypoints)
        npc.properties["current_waypoint_index"] = next_index
        target_waypoint = waypoints[next_index]

    # Move toward the target waypoint
    return Action(
        action_type="move",
        target_position=target_waypoint,
        data={"waypoint_index": npc.properties.get("current_waypoint_index", 0)},
    )


def attack_on_sight_behavior(npc: Entity, world: WorldState) -> Action:
    """Attack-on-sight behavior - NPC attacks nearby hostile targets.

    The NPC scans for entities within detection range and attacks the nearest
    hostile target. If no targets are in range, it idles.

    Expected NPC properties:
        detection_range: Integer representing how far the NPC can detect enemies.
        hostile_to: List of entity type tags that this NPC is hostile toward.

    Args:
        npc: The NPC entity to generate behavior for.
        world: The current world state.

    Returns:
        An attack action if a target is found, otherwise idle.
    """
    detection_range = npc.properties.get("detection_range", 5)
    hostile_to = npc.properties.get("hostile_to", ["player"])

    # Scan for entities within detection range
    closest_target = None
    closest_distance = float("inf")

    for entity_id in world.get_all_entity_ids():
        if entity_id == npc.id:
            continue  # Skip self

        entity = world.get_entity(entity_id)
        if entity is None:
            continue

        # Check if entity is in the same location
        if entity.position.location_id != npc.position.location_id:
            continue

        # Check if entity is hostile
        entity_type = entity.properties.get("type", "")
        if entity_type not in hostile_to:
            continue

        # Calculate distance (simple Manhattan distance)
        distance = abs(entity.position.x - npc.position.x) + abs(
            entity.position.y - npc.position.y
        )

        if distance <= detection_range and distance < closest_distance:
            closest_distance = distance
            closest_target = entity

    if closest_target:
        return Action(
            action_type="attack",
            target_entity_id=closest_target.id,
            data={"distance": closest_distance},
        )

    return Action(action_type="idle")


def apply_action(action: Action, npc: Entity, world: WorldState) -> None:
    """Apply an action to the world state.

    This is a helper function that modifies the world state based on the action.
    It handles movement and other state changes.

    Args:
        action: The action to apply.
        npc: The NPC entity performing the action.
        world: The world state to modify.
    """
    if action.action_type == "move" and action.target_position:
        # Simple movement: move one step toward target
        dx = 0
        dy = 0

        if npc.position.x < action.target_position.x:
            dx = 1
        elif npc.position.x > action.target_position.x:
            dx = -1

        if npc.position.y < action.target_position.y:
            dy = 1
        elif npc.position.y > action.target_position.y:
            dy = -1

        # Update position (move one step at a time)
        npc.position.x += dx
        npc.position.y += dy
