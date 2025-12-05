"""Game engine for managing the main game loop.

This module provides the GameEngine class that can run in two modes:
- Player mode: advances the game state one step at a time based on player actions
- Headless mode: automatically advances world ticks for simulation
"""

import logging
from enum import Enum

from src.simulation.npc_ai import Action
from src.world.world_state import WorldState

logger = logging.getLogger(__name__)


class GameMode(Enum):
    """Enumeration of game modes."""

    PLAYER = "player"
    HEADLESS = "headless"


class GameEngine:
    """Main game engine for managing the game loop.

    The GameEngine can run in two modes:
    - PLAYER mode: The game advances one step at a time when the player
      provides an action. World state ticks are advanced manually.
    - HEADLESS mode: The game automatically advances world ticks for
      autonomous simulation without player input.

    Attributes:
        world: The WorldState instance managed by this engine.
        mode: The current game mode (PLAYER or HEADLESS).
    """

    def __init__(
        self, world: WorldState | None = None, mode: GameMode = GameMode.PLAYER
    ) -> None:
        """Initialize the game engine.

        Args:
            world: Optional WorldState instance. If not provided, creates a new one.
            mode: The game mode to start in (default: PLAYER).
        """
        self.world = world if world is not None else WorldState()
        self.mode = mode
        self._running = False
        logger.info("GameEngine initialized in %s mode", mode.value)

    def step(self, action: Action | None = None) -> int:
        """Advance the game by one step.

        In PLAYER mode, this processes the given action (if any) and advances
        the world by one tick.

        In HEADLESS mode, this advances the world by one tick regardless of
        the action parameter.

        Args:
            action: Optional action to process before advancing the tick.
                   Only used in PLAYER mode.

        Returns:
            The current world time after the step.
        """
        if self.mode == GameMode.PLAYER:
            if action is not None:
                logger.debug("Processing action: %s", action.action_type)
                # Action processing would be handled by ActionHandler
                # For now, we just log it

        # Advance world time by one tick
        current_time = self.world.tick()
        logger.debug("Game step completed, world time: %d", current_time)

        return current_time

    def run_headless(self, ticks: int) -> int:
        """Run the game in headless mode for a specified number of ticks.

        This is used for autonomous simulation without player input.
        Advances the world state by the specified number of ticks.

        Args:
            ticks: The number of ticks to advance.

        Returns:
            The final world time after running.

        Raises:
            ValueError: If ticks is negative.
        """
        if ticks < 0:
            raise ValueError("Number of ticks must be non-negative")

        logger.info("Running headless simulation for %d ticks", ticks)

        for i in range(ticks):
            self.world.tick()
            logger.debug("Headless tick %d/%d completed", i + 1, ticks)

        final_time = self.world.time
        logger.info("Headless simulation completed, final time: %d", final_time)

        return final_time

    def set_mode(self, mode: GameMode) -> None:
        """Change the game mode.

        Args:
            mode: The new game mode to set.
        """
        if self.mode != mode:
            logger.info("Changing game mode from %s to %s", self.mode.value, mode.value)
            self.mode = mode

    def get_current_time(self) -> int:
        """Get the current game time.

        Returns:
            The current world time in ticks.
        """
        return self.world.time
