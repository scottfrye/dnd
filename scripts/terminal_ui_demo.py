#!/usr/bin/env python3
"""Smoke test demonstration for the terminal UI.

This script demonstrates the basic functionality of the terminal display
and input handler implementations.
"""

import time

from src.ui.input import InputAction
from src.ui.input_handler import TerminalInputHandler
from src.ui.terminal_display import TerminalDisplay


def main():
    """Run a simple demonstration of the terminal UI."""
    # Create a simple test map
    test_map = [
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ]

    # Player starting position
    player_x = 5
    player_y = 4

    # Test status data
    status_data = {
        "name": "Hero",
        "level": 1,
        "hp": 10,
        "max_hp": 15,
        "ac": 5,
    }

    # Test messages
    messages = [
        "Welcome to the Temple of Elemental Evil!",
        "Use hjkl or arrow keys to move.",
        "Press ? for help, q to quit.",
    ]

    # Create display and input handler
    display = TerminalDisplay()
    input_handler = TerminalInputHandler()

    try:
        with display, input_handler:
            # Initial render
            display.clear()
            display.render_map(test_map, player_x, player_y)
            display.render_status(status_data)
            display.render_messages(messages)
            display.refresh()

            # Main loop
            running = True
            while running:
                # Get input with a short timeout
                action = input_handler.get_input(timeout=0.1)

                if action is None:
                    continue

                # Process input
                if action == InputAction.QUIT:
                    messages.append("Goodbye!")
                    running = False
                elif action == InputAction.HELP:
                    messages.append("Help: hjkl=move, q=quit, ?=help")
                elif action == InputAction.MOVE_NORTH:
                    if test_map[player_y - 1][player_x] != "#":
                        player_y -= 1
                        messages.append("You move north.")
                    else:
                        messages.append("You can't move there!")
                elif action == InputAction.MOVE_SOUTH:
                    if test_map[player_y + 1][player_x] != "#":
                        player_y += 1
                        messages.append("You move south.")
                    else:
                        messages.append("You can't move there!")
                elif action == InputAction.MOVE_EAST:
                    if test_map[player_y][player_x + 1] != "#":
                        player_x += 1
                        messages.append("You move east.")
                    else:
                        messages.append("You can't move there!")
                elif action == InputAction.MOVE_WEST:
                    if test_map[player_y][player_x - 1] != "#":
                        player_x -= 1
                        messages.append("You move west.")
                    else:
                        messages.append("You can't move there!")
                elif action == InputAction.WAIT:
                    messages.append("You wait.")
                elif action == InputAction.UNKNOWN:
                    messages.append("Unknown command. Press ? for help.")
                else:
                    messages.append(f"Action not implemented: {action.value}")

                # Re-render the display
                display.clear()
                display.render_map(test_map, player_x, player_y)
                display.render_status(status_data)
                display.render_messages(messages)
                display.refresh()

            # Small delay before exit to show final message
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
