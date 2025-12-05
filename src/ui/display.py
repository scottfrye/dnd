"""Abstract Display API for the game UI.

This module defines the abstract base class for display implementations,
allowing different UI backends (terminal, GUI, etc.) to be plugged in.
"""

from abc import ABC, abstractmethod
from typing import Any


class Display(ABC):
    """Abstract base class for game display implementations.

    This class defines the interface that all display implementations must follow,
    whether terminal-based, graphical, or other formats.
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the display system.

        This should set up any necessary resources, enter appropriate modes,
        and prepare the display for rendering.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up and release display resources.

        This should restore the terminal/screen to its original state and
        release any resources held by the display.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the entire display."""
        pass

    @abstractmethod
    def render_map(
        self, map_data: list[list[str]], player_x: int, player_y: int
    ) -> None:
        """Render the game map.

        Args:
            map_data: 2D list of strings representing the map tiles
            player_x: Player's x coordinate
            player_y: Player's y coordinate
        """
        pass

    @abstractmethod
    def render_status(self, status_data: dict[str, Any]) -> None:
        """Render the status area showing character information.

        Args:
            status_data: Dictionary containing character stats and status info
                Expected keys might include: 'hp', 'max_hp', 'name', 'level', etc.
        """
        pass

    @abstractmethod
    def render_messages(self, messages: list[str]) -> None:
        """Render the message log.

        Args:
            messages: List of recent message strings to display
        """
        pass

    @abstractmethod
    def refresh(self) -> None:
        """Refresh the display to show all rendered content.

        This commits any pending render operations to the screen.
        """
        pass

    @abstractmethod
    def get_dimensions(self) -> tuple[int, int]:
        """Get the display dimensions.

        Returns:
            Tuple of (width, height) in character cells
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
