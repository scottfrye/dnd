"""Action handler for processing game actions.

This module provides the ActionHandler class that defines a protocol for
processing actions (move, attack, etc.) and integrating with WorldState.
"""

import logging

from src.entities.entity import Entity
from src.simulation.npc_ai import Action
from src.world.world_state import WorldState

logger = logging.getLogger(__name__)


class ActionHandler:
    """Handler for processing and applying game actions.

    ActionHandler defines a protocol for actions like move and attack,
    and applies them to the WorldState. It serves as the bridge between
    action requests and world state modifications.

    Attributes:
        world: The WorldState instance to apply actions to.
    """

    def __init__(self, world: WorldState) -> None:
        """Initialize the action handler.

        Args:
            world: The WorldState instance to manage.
        """
        self.world = world
        logger.debug("ActionHandler initialized")

    def handle_action(self, action: Action, entity_id: str) -> bool:
        """Handle an action for a given entity.

        Processes the action and applies it to the world state.

        Args:
            action: The action to process.
            entity_id: The ID of the entity performing the action.

        Returns:
            True if the action was handled successfully, False otherwise.
        """
        entity = self.world.get_entity(entity_id)
        if entity is None:
            logger.warning("Cannot handle action: entity '%s' not found", entity_id)
            return False

        if action.action_type == "move":
            return self._handle_move(action, entity)
        elif action.action_type == "attack":
            return self._handle_attack(action, entity)
        elif action.action_type == "idle":
            return self._handle_idle(action, entity)
        else:
            logger.warning("Unknown action type: %s", action.action_type)
            return False

    def _handle_move(self, action: Action, entity: Entity) -> bool:
        """Handle a move action.

        Moves the entity one step toward the target position.

        Args:
            action: The move action with target_position.
            entity: The entity to move.

        Returns:
            True if the move was successful, False otherwise.
        """
        if action.target_position is None:
            logger.warning("Move action has no target position")
            return False

        target = action.target_position

        # Calculate movement direction
        dx = 0
        dy = 0

        if entity.position.x < target.x:
            dx = 1
        elif entity.position.x > target.x:
            dx = -1

        if entity.position.y < target.y:
            dy = 1
        elif entity.position.y > target.y:
            dy = -1

        # Apply movement (one step at a time)
        old_x, old_y = entity.position.x, entity.position.y
        entity.position.x += dx
        entity.position.y += dy

        logger.debug(
            "Entity '%s' moved from (%d, %d) to (%d, %d)",
            entity.id,
            old_x,
            old_y,
            entity.position.x,
            entity.position.y,
        )

        return True

    def _handle_attack(self, action: Action, entity: Entity) -> bool:
        """Handle an attack action.

        Processes an attack against a target entity. The actual combat
        resolution would be handled by the combat system.

        Args:
            action: The attack action with target_entity_id.
            entity: The entity performing the attack.

        Returns:
            True if the attack was initiated successfully, False otherwise.
        """
        if action.target_entity_id is None:
            logger.warning("Attack action has no target entity")
            return False

        target = self.world.get_entity(action.target_entity_id)
        if target is None:
            logger.warning(
                "Attack action target '%s' not found",
                action.target_entity_id,
            )
            return False

        # Check if entities are in the same location
        if entity.position.location_id != target.position.location_id:
            logger.warning(
                "Entity '%s' cannot attack '%s': different locations",
                entity.id,
                target.id,
            )
            return False

        logger.info(
            "Entity '%s' attacks '%s'",
            entity.id,
            target.id,
        )

        # Actual combat resolution would be handled by the combat system
        # For now, we just log the attack and return success
        logger.debug("Combat resolution not yet implemented")
        return True

    def _handle_idle(self, action: Action, entity: Entity) -> bool:
        """Handle an idle action.

        Idle actions do nothing, which is valid behavior.

        Args:
            action: The idle action.
            entity: The entity that is idle.

        Returns:
            Always returns True.
        """
        logger.debug("Entity '%s' is idle", entity.id)
        return True

    def apply_actions_for_tick(self) -> None:
        """Apply any scheduled actions for the current tick.

        This is a placeholder for future functionality where actions
        might be queued and processed at specific ticks.
        """
        # Future enhancement: process queued actions
        pass
