"""Admin commands module for game administration and debugging.

This module provides a command dispatch system and core admin commands
for inspecting, debugging, and manipulating the game world.
"""

from src.admin.commands import AdminCommandRegistry, execute_command, get_registry

__all__ = ["AdminCommandRegistry", "execute_command", "get_registry"]
