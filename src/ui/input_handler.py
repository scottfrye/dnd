"""Terminal input handler implementation using blessed.

This module provides a terminal-based implementation of the InputHandler
interface using the blessed library for keyboard input.
"""

from typing import Optional

from blessed import Terminal

from src.ui.input import InputAction, InputHandler


class TerminalInputHandler(InputHandler):
    """Terminal-based input handler using blessed.
    
    This class implements the InputHandler interface for terminal keyboard input,
    supporting multiple key mapping schemes (vi-keys, arrow keys, numpad).
    """

    # Default key mappings for different input schemes
    # Vi-keys and arrow keys for movement
    DEFAULT_KEY_MAPPINGS = {
        # Vi-keys (classic roguelike)
        'h': InputAction.MOVE_WEST,
        'j': InputAction.MOVE_SOUTH,
        'k': InputAction.MOVE_NORTH,
        'l': InputAction.MOVE_EAST,
        'y': InputAction.MOVE_NORTHWEST,
        'u': InputAction.MOVE_NORTHEAST,
        'b': InputAction.MOVE_SOUTHWEST,
        'n': InputAction.MOVE_SOUTHEAST,
        
        # Arrow keys
        'KEY_LEFT': InputAction.MOVE_WEST,
        'KEY_RIGHT': InputAction.MOVE_EAST,
        'KEY_UP': InputAction.MOVE_NORTH,
        'KEY_DOWN': InputAction.MOVE_SOUTH,
        
        # Numpad
        '4': InputAction.MOVE_WEST,
        '6': InputAction.MOVE_EAST,
        '8': InputAction.MOVE_NORTH,
        '2': InputAction.MOVE_SOUTH,
        '7': InputAction.MOVE_NORTHWEST,
        '9': InputAction.MOVE_NORTHEAST,
        '1': InputAction.MOVE_SOUTHWEST,
        '3': InputAction.MOVE_SOUTHEAST,
        '5': InputAction.WAIT,
        
        # Game actions
        '.': InputAction.WAIT,
        ',': InputAction.PICKUP,
        'g': InputAction.PICKUP,  # Alternative pickup
        'i': InputAction.INVENTORY,
        'a': InputAction.USE,
        'd': InputAction.DROP,
        'c': InputAction.CAST_SPELL,
        ';': InputAction.LOOK,
        
        # UI actions
        '?': InputAction.HELP,
        'q': InputAction.QUIT,
        'Q': InputAction.QUIT,
        'S': InputAction.SAVE,
    }

    def __init__(self, terminal: Optional[Terminal] = None):
        """Initialize the terminal input handler.
        
        Args:
            terminal: Optional blessed Terminal instance. If not provided,
                     a new Terminal will be created.
        """
        self.term = terminal or Terminal()
        self._initialized = False
        # Create instance-level copy of key mappings to avoid cross-instance pollution
        self.key_mappings = self.DEFAULT_KEY_MAPPINGS.copy()

    def initialize(self) -> None:
        """Initialize the input handler."""
        self._initialized = True
        # blessed Terminal handles initialization automatically

    def cleanup(self) -> None:
        """Clean up and release input handler resources."""
        if self._initialized:
            # Nothing specific to clean up for blessed
            self._initialized = False

    def get_input(self, timeout: Optional[float] = None) -> Optional[InputAction]:
        """Get the next input action from the user.
        
        Args:
            timeout: Optional timeout in seconds. If None, blocks until input.
                    If 0, returns immediately with None if no input available.
                    
        Returns:
            The InputAction corresponding to the user's input, or None if timeout
        """
        key = self.get_key(timeout)
        
        if key is None:
            return None
        
        # Look up the key in the mapping
        action = self.key_mappings.get(key, InputAction.UNKNOWN)
        return action

    def get_key(self, timeout: Optional[float] = None) -> Optional[str]:
        """Get the next raw key press from the user.
        
        Args:
            timeout: Optional timeout in seconds. If None, blocks until input.
                    
        Returns:
            String representation of the key pressed, or None if timeout
        """
        with self.term.cbreak():
            # Read a key with optional timeout
            key = self.term.inkey(timeout=timeout)
            
            if not key:
                return None
            
            # Return the key's name if it's a special key, otherwise the character
            return key.name if key.is_sequence else str(key)

    def add_key_mapping(self, key: str, action: InputAction) -> None:
        """Add or update a key mapping.
        
        This allows for runtime customization of key bindings.
        
        Args:
            key: The key string to map
            action: The InputAction to associate with the key
        """
        self.key_mappings[key] = action

    def remove_key_mapping(self, key: str) -> None:
        """Remove a key mapping.
        
        Args:
            key: The key string to remove from mappings
        """
        if key in self.key_mappings:
            del self.key_mappings[key]

    def get_key_mapping(self, key: str) -> Optional[InputAction]:
        """Get the action mapped to a key.
        
        Args:
            key: The key string to look up
            
        Returns:
            The InputAction mapped to the key, or None if not mapped
        """
        return self.key_mappings.get(key)
