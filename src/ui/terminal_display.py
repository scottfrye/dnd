"""Terminal display implementation using the blessed library.

This module provides a terminal-based implementation of the Display interface
using the blessed library for terminal manipulation.
"""

import sys
from typing import Any, Optional

from blessed import Terminal

from src.ui.display import Display


class TerminalDisplay(Display):
    """Terminal-based display implementation using blessed.
    
    This class implements the Display interface for terminal rendering,
    providing ASCII-based map display and status areas.
    """

    def __init__(self, terminal: Optional[Terminal] = None):
        """Initialize the terminal display.
        
        Args:
            terminal: Optional blessed Terminal instance. If not provided,
                     a new Terminal will be created.
        """
        self.term = terminal or Terminal()
        self._initialized = False
        
        # Display area layout (can be adjusted)
        self.map_area_height = 20
        self.map_area_width = 60
        self.status_area_width = 30
        self.message_area_height = 5

    def initialize(self) -> None:
        """Initialize the display system."""
        self._initialized = True
        # blessed Terminal handles initialization automatically
        # We just need to clear the screen
        self.clear()

    def cleanup(self) -> None:
        """Clean up and release display resources."""
        if self._initialized:
            # Show cursor and return to normal mode
            print(self.term.normal_cursor)
            print(self.term.normal)
            self._initialized = False

    def clear(self) -> None:
        """Clear the entire display."""
        print(self.term.clear)

    def render_map(self, map_data: list[list[str]], player_x: int, player_y: int) -> None:
        """Render the game map in ASCII.
        
        Args:
            map_data: 2D list of strings representing the map tiles
            player_x: Player's x coordinate
            player_y: Player's y coordinate
        """
        # Position cursor at top-left for map area
        with self.term.location(0, 0):
            print(self.term.bold("=== MAP ==="))
        
        # Render the map starting from line 1
        for y, row in enumerate(map_data):
            if y >= self.map_area_height - 1:  # Leave room for header
                break
            
            with self.term.location(0, y + 1):
                line = ""
                for x, tile in enumerate(row):
                    if x >= self.map_area_width:
                        break
                    
                    # Highlight player position
                    if x == player_x and y == player_y:
                        line += self.term.bold_green("@")
                    else:
                        line += tile
                
                print(line)

    def render_status(self, status_data: dict[str, Any]) -> None:
        """Render the status area showing character information.
        
        Args:
            status_data: Dictionary containing character stats and status info
        """
        # Position cursor at the right side for status area
        start_x = self.map_area_width + 2
        start_y = 0
        
        with self.term.location(start_x, start_y):
            print(self.term.bold("=== STATUS ==="))
        
        # Render status fields
        y_offset = 1
        for key, value in status_data.items():
            with self.term.location(start_x, start_y + y_offset):
                print(f"{key.capitalize()}: {value}")
            y_offset += 1

    def render_messages(self, messages: list[str]) -> None:
        """Render the message log.
        
        Args:
            messages: List of recent message strings to display
        """
        # Position messages at the bottom of the screen
        start_y = self.map_area_height + 1
        
        with self.term.location(0, start_y):
            print(self.term.bold("=== MESSAGES ==="))
        
        # Render the most recent messages
        for i, message in enumerate(messages[-self.message_area_height:]):
            with self.term.location(0, start_y + 1 + i):
                # Clear the line first
                print(self.term.clear_eol + message)

    def refresh(self) -> None:
        """Refresh the display to show all rendered content.
        
        blessed writes directly, so we just need to flush stdout.
        """
        sys.stdout.flush()

    def get_dimensions(self) -> tuple[int, int]:
        """Get the display dimensions.
        
        Returns:
            Tuple of (width, height) in character cells
        """
        return (self.term.width, self.term.height)
