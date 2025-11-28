"""Entity base class for all game objects.

This module provides the base Entity class that serves as the foundation
for all game objects including characters, monsters, items, etc.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Position:
    """Represents a position in the game world.

    Attributes:
        x: The x-coordinate on the map.
        y: The y-coordinate on the map.
        location_id: Identifier for the location/map containing this position.
    """

    x: int
    y: int
    location_id: str


@dataclass
class Entity:
    """Base class for all game entities.

    An Entity represents any object in the game world that has an identity
    and position. This includes characters, monsters, items, and other
    game objects.

    Attributes:
        id: Unique identifier for this entity.
        position: The entity's position in the game world.
        properties: Dictionary of additional entity properties.
    """

    id: str
    position: Position
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the entity to a dictionary.

        Returns:
            A dictionary representation of the entity suitable for
            JSON serialization or persistence.
        """
        return {
            "id": self.id,
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "location_id": self.position.location_id,
            },
            "properties": self.properties.copy(),
        }
