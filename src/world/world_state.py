"""World state management module.

This module provides the WorldState class which serves as a central registry
for game entities and manages the game's time system.
"""

import logging

from src.entities.entity import Entity

logger = logging.getLogger(__name__)


class WorldState:
    """Central registry for entities and time management.

    WorldState maintains a collection of game entities and provides methods
    for adding, removing, and querying entities. It also manages an internal
    time counter that can be advanced via the tick() method.

    Attributes:
        time: The current game time as an integer tick count.
    """

    def __init__(self) -> None:
        """Initialize a new WorldState with empty entity registry and time at 0."""
        self._entities: dict[str, Entity] = {}
        self._time: int = 0

    @property
    def time(self) -> int:
        """Get the current game time.

        Returns:
            The current tick count.
        """
        return self._time

    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the world.

        Args:
            entity: The entity to add to the world.

        Raises:
            ValueError: If an entity with the same id already exists.
        """
        if entity.id in self._entities:
            raise ValueError(f"Entity with id '{entity.id}' already exists")
        self._entities[entity.id] = entity
        logger.debug("Added entity: %s", entity.id)

    def remove_entity(self, entity_id: str) -> bool:
        """Remove an entity from the world.

        Args:
            entity_id: The id of the entity to remove.

        Returns:
            True if the entity was removed, False if it didn't exist.
        """
        if entity_id in self._entities:
            del self._entities[entity_id]
            logger.debug("Removed entity: %s", entity_id)
            return True
        return False

    def get_entity(self, entity_id: str) -> Entity | None:
        """Get an entity by its id.

        Args:
            entity_id: The id of the entity to retrieve.

        Returns:
            The entity if found, None otherwise.
        """
        return self._entities.get(entity_id)

    def get_all_entity_ids(self) -> list[str]:
        """Get a list of all entity IDs in the world.

        Returns:
            A list of entity IDs currently registered in the world.
        """
        return list(self._entities.keys())

    def tick(self) -> int:
        """Advance the game time by one tick.

        Increments the internal time counter and emits a logged event.

        Returns:
            The new time value after the tick.
        """
        self._time += 1
        logger.info("World tick: time is now %d", self._time)
        return self._time

    def to_dict(self) -> dict:
        """Serialize the world state to a dictionary.

        Returns:
            A dictionary representation of the world state containing
            the current time and all entities.
        """
        return {
            "time": self._time,
            "entities": [entity.to_dict() for entity in self._entities.values()],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorldState":
        """Deserialize a world state from a dictionary.

        Args:
            data: Dictionary representation of the world state.

        Returns:
            A new WorldState instance created from the dictionary data.
        """
        world = cls()
        world._time = data.get("time", 0)
        for entity_data in data.get("entities", []):
            entity = Entity.from_dict(entity_data)
            world.add_entity(entity)
        return world
