"""Abstract Input Handler API for the game UI.

This module defines the abstract base class for input handling implementations,
allowing different input methods to be plugged in.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class InputAction(Enum):
    """Enumeration of possible input actions in the game."""
    
    # Movement actions
    MOVE_NORTH = "move_north"
    MOVE_SOUTH = "move_south"
    MOVE_EAST = "move_east"
    MOVE_WEST = "move_west"
    MOVE_NORTHEAST = "move_northeast"
    MOVE_NORTHWEST = "move_northwest"
    MOVE_SOUTHEAST = "move_southeast"
    MOVE_SOUTHWEST = "move_southwest"
    
    # Game actions
    WAIT = "wait"
    PICKUP = "pickup"
    INVENTORY = "inventory"
    USE = "use"
    DROP = "drop"
    CAST_SPELL = "cast_spell"
    LOOK = "look"
    
    # UI actions
    HELP = "help"
    QUIT = "quit"
    SAVE = "save"
    
    # Unknown/unmapped input
    UNKNOWN = "unknown"


class InputHandler(ABC):
    """Abstract base class for input handling implementations.
    
    This class defines the interface that all input handlers must follow,
    whether keyboard-based, mouse-based, or network-based.
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the input handler.
        
        This should set up any necessary resources and prepare for input.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up and release input handler resources."""
        pass

    @abstractmethod
    def get_input(self, timeout: Optional[float] = None) -> Optional[InputAction]:
        """Get the next input action from the user.
        
        Args:
            timeout: Optional timeout in seconds. If None, blocks until input.
                    If 0, returns immediately with None if no input available.
                    
        Returns:
            The InputAction corresponding to the user's input, or None if timeout
        """
        pass

    @abstractmethod
    def get_key(self, timeout: Optional[float] = None) -> Optional[str]:
        """Get the next raw key press from the user.
        
        This is useful for prompts that need specific key input rather than
        game actions (e.g., confirmation dialogs).
        
        Args:
            timeout: Optional timeout in seconds. If None, blocks until input.
                    
        Returns:
            String representation of the key pressed, or None if timeout
        """
        pass

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
        return False
