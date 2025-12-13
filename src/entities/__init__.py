"""Entity system package.

This package contains modules for game objects including characters,
monsters, items, and faction management.
"""

from src.entities.character import Character, create_character
from src.entities.entity import Entity, Position

__all__ = ["Character", "create_character", "Entity", "Position"]
