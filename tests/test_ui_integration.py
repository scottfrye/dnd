"""Integration tests for the UI system.

These tests verify that the Display and InputHandler implementations
work together correctly in typical game scenarios.
"""

from unittest.mock import MagicMock, Mock, patch

from src.ui.display import Display
from src.ui.input import InputAction, InputHandler
from src.ui.input_handler import TerminalInputHandler
from src.ui.terminal_display import TerminalDisplay


class TestUIIntegration:
    """Integration tests for Display and InputHandler working together."""

    def test_terminal_display_and_input_handler_initialization(self):
        """Test that TerminalDisplay and TerminalInputHandler can be initialized together."""
        with (
            patch("src.ui.terminal_display.Terminal"),
            patch("src.ui.input_handler.Terminal"),
        ):
            display = TerminalDisplay()
            input_handler = TerminalInputHandler()

            assert isinstance(display, Display)
            assert isinstance(input_handler, InputHandler)

    def test_terminal_ui_context_managers_together(self):
        """Test that both UI components can be used as context managers together."""
        mock_term_display = MagicMock()
        mock_term_display.clear = "CLEAR"
        mock_term_display.normal_cursor = "CURSOR"
        mock_term_display.normal = "NORMAL"

        mock_term_input = MagicMock()

        with patch("builtins.print"):
            with (
                TerminalDisplay(terminal=mock_term_display) as display,
                TerminalInputHandler(terminal=mock_term_input) as input_handler,
            ):
                assert display._initialized
                assert input_handler._initialized

            assert not display._initialized
            assert not input_handler._initialized

    def test_complete_render_cycle(self):
        """Test a complete render cycle with all display elements."""
        mock_term = MagicMock()
        mock_term.clear = "CLEAR"
        mock_term.bold.return_value = "BOLD"
        mock_term.bold_green.return_value = "@"
        mock_term.clear_eol = "EOL"
        mock_term.width = 100
        mock_term.height = 40
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        # Test data
        map_data = [
            ["#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#"],
        ]
        status_data = {"hp": 10, "max_hp": 15, "ac": 5, "level": 1}
        messages = ["You enter the dungeon.", "You see a goblin ahead!"]

        with patch("builtins.print"), patch("sys.stdout"):
            display.initialize()
            display.clear()
            display.render_map(map_data, player_x=2, player_y=2)
            display.render_status(status_data)
            display.render_messages(messages)
            display.refresh()

            # Verify all rendering methods were called
            mock_term.bold.assert_called()
            mock_term.bold_green.assert_called()

    def test_input_to_movement_workflow(self):
        """Test workflow from key press to movement action."""
        mock_term = MagicMock()
        input_handler = TerminalInputHandler(terminal=mock_term)

        # Simulate different key presses
        test_cases = [
            ("k", InputAction.MOVE_NORTH),
            ("j", InputAction.MOVE_SOUTH),
            ("h", InputAction.MOVE_WEST),
            ("l", InputAction.MOVE_EAST),
            ("KEY_UP", InputAction.MOVE_NORTH),
            ("KEY_DOWN", InputAction.MOVE_SOUTH),
            ("KEY_LEFT", InputAction.MOVE_WEST),
            ("KEY_RIGHT", InputAction.MOVE_EAST),
        ]

        for key_input, expected_action in test_cases:
            mock_key = Mock()
            mock_key.is_sequence = key_input.startswith("KEY_")
            if mock_key.is_sequence:
                mock_key.name = key_input
            else:
                mock_key.__str__ = Mock(return_value=key_input)
            mock_key.__bool__ = Mock(return_value=True)

            mock_term.inkey.return_value = mock_key
            mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
            mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

            action = input_handler.get_input()
            assert (
                action == expected_action
            ), f"Key {key_input} should map to {expected_action}"

    def test_game_action_workflow(self):
        """Test workflow for various game actions."""
        mock_term = MagicMock()
        input_handler = TerminalInputHandler(terminal=mock_term)

        test_cases = [
            (".", InputAction.WAIT),
            (",", InputAction.PICKUP),
            ("i", InputAction.INVENTORY),
            ("?", InputAction.HELP),
            ("q", InputAction.QUIT),
        ]

        for key_input, expected_action in test_cases:
            mock_key = Mock()
            mock_key.is_sequence = False
            mock_key.__str__ = Mock(return_value=key_input)
            mock_key.__bool__ = Mock(return_value=True)

            mock_term.inkey.return_value = mock_key
            mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
            mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

            action = input_handler.get_input()
            assert (
                action == expected_action
            ), f"Key {key_input} should map to {expected_action}"

    def test_multiple_render_and_input_cycles(self):
        """Test multiple complete render and input cycles."""
        mock_term_display = MagicMock()
        mock_term_display.clear = "CLEAR"
        mock_term_display.bold.return_value = "BOLD"
        mock_term_display.bold_green.return_value = "@"
        mock_term_display.clear_eol = "EOL"
        mock_term_display.location.return_value.__enter__ = Mock(return_value=None)
        mock_term_display.location.return_value.__exit__ = Mock(return_value=None)

        mock_term_input = MagicMock()

        display = TerminalDisplay(terminal=mock_term_display)
        input_handler = TerminalInputHandler(terminal=mock_term_input)

        map_data = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        player_x, player_y = 1, 1

        with patch("builtins.print"), patch("sys.stdout"):
            display.initialize()

            # Simulate multiple game loop iterations
            for i in range(5):
                # Render
                display.clear()
                display.render_map(map_data, player_x, player_y)
                display.render_status({"hp": 10 - i})
                display.render_messages([f"Turn {i}"])
                display.refresh()

                # Simulate input
                mock_key = Mock()
                mock_key.is_sequence = False
                mock_key.__str__ = Mock(return_value=".")
                mock_key.__bool__ = Mock(return_value=True)
                mock_term_input.inkey.return_value = mock_key
                mock_term_input.cbreak.return_value.__enter__ = Mock(return_value=None)
                mock_term_input.cbreak.return_value.__exit__ = Mock(return_value=None)

                action = input_handler.get_input()
                assert action == InputAction.WAIT

            display.cleanup()

    def test_timeout_handling_in_game_loop(self):
        """Test that timeout handling works correctly in a game loop scenario."""
        mock_term = MagicMock()
        mock_term.inkey.return_value = ""  # Simulate no input
        mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

        input_handler = TerminalInputHandler(terminal=mock_term)

        # Test with short timeout (non-blocking check)
        action = input_handler.get_input(timeout=0.1)
        assert action is None

        # Verify inkey was called with timeout
        mock_term.inkey.assert_called_with(timeout=0.1)

    def test_unknown_input_handling(self):
        """Test that unknown inputs are handled gracefully."""
        mock_term = MagicMock()
        input_handler = TerminalInputHandler(terminal=mock_term)

        # Simulate unmapped key press
        mock_key = Mock()
        mock_key.is_sequence = False
        mock_key.__str__ = Mock(return_value="~")  # Unmapped key
        mock_key.__bool__ = Mock(return_value=True)

        mock_term.inkey.return_value = mock_key
        mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

        action = input_handler.get_input()
        assert action == InputAction.UNKNOWN

    def test_display_dimensions_for_layout(self):
        """Test that display dimensions can be used for layout calculations."""
        mock_term = MagicMock()
        mock_term.width = 100
        mock_term.height = 30

        display = TerminalDisplay(terminal=mock_term)

        width, height = display.get_dimensions()
        assert width == 100
        assert height == 30

        # Verify layout areas fit within dimensions
        total_width = display.map_area_width + display.status_area_width
        total_height = display.map_area_height + display.message_area_height

        assert total_width <= width
        assert total_height <= height


class TestUIErrorHandling:
    """Test error handling and edge cases in UI integration."""

    def test_render_with_empty_map(self):
        """Test rendering with an empty map."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        with patch("builtins.print"):
            display.render_map([], player_x=0, player_y=0)

    def test_render_with_empty_status(self):
        """Test rendering with an empty status dictionary."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        with patch("builtins.print"):
            display.render_status({})

    def test_render_with_empty_messages(self):
        """Test rendering with an empty message list."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.clear_eol = "EOL"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        with patch("builtins.print"):
            display.render_messages([])

    def test_render_with_oversized_map(self):
        """Test rendering with a map larger than display area."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.bold_green.return_value = "@"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        # Create a map larger than the display area
        large_map = [["." for _ in range(100)] for _ in range(100)]

        with patch("builtins.print"):
            # Should not raise an error, should clip to display area
            display.render_map(large_map, player_x=50, player_y=50)

    def test_render_with_many_messages(self):
        """Test rendering with more messages than display area can hold."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.clear_eol = "EOL"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        # Create more messages than can fit
        many_messages = [f"Message {i}" for i in range(100)]

        with patch("builtins.print"):
            # Should not raise an error, should show most recent messages
            display.render_messages(many_messages)

    def test_multiple_handlers_independent(self):
        """Test that multiple input handlers maintain independent state."""
        mock_term1 = MagicMock()
        mock_term2 = MagicMock()

        handler1 = TerminalInputHandler(terminal=mock_term1)
        handler2 = TerminalInputHandler(terminal=mock_term2)

        # Add custom mapping to handler1
        handler1.add_key_mapping("x", InputAction.SAVE)

        # Verify independence
        assert handler1.get_key_mapping("x") == InputAction.SAVE
        assert handler2.get_key_mapping("x") is None

        # Verify both have default mappings
        assert handler1.get_key_mapping("k") == InputAction.MOVE_NORTH
        assert handler2.get_key_mapping("k") == InputAction.MOVE_NORTH


class TestUIWorkflowScenarios:
    """Test complete UI workflow scenarios."""

    def test_player_movement_scenario(self):
        """Test a complete player movement scenario with rendering updates."""
        mock_term_display = MagicMock()
        mock_term_display.clear = "CLEAR"
        mock_term_display.bold.return_value = "BOLD"
        mock_term_display.bold_green.return_value = "@"
        mock_term_display.clear_eol = "EOL"
        mock_term_display.location.return_value.__enter__ = Mock(return_value=None)
        mock_term_display.location.return_value.__exit__ = Mock(return_value=None)

        mock_term_input = MagicMock()

        display = TerminalDisplay(terminal=mock_term_display)
        input_handler = TerminalInputHandler(terminal=mock_term_input)

        # Initial state
        map_data = [
            ["#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#"],
        ]
        player_x, player_y = 2, 2
        messages = ["You are in a room."]

        with patch("builtins.print"), patch("sys.stdout"):
            display.initialize()

            # Initial render
            display.clear()
            display.render_map(map_data, player_x, player_y)
            display.render_status({"hp": 10, "max_hp": 10})
            display.render_messages(messages)
            display.refresh()

            # Player moves north
            mock_key = Mock()
            mock_key.is_sequence = False
            mock_key.__str__ = Mock(return_value="k")
            mock_key.__bool__ = Mock(return_value=True)
            mock_term_input.inkey.return_value = mock_key
            mock_term_input.cbreak.return_value.__enter__ = Mock(return_value=None)
            mock_term_input.cbreak.return_value.__exit__ = Mock(return_value=None)

            action = input_handler.get_input()
            assert action == InputAction.MOVE_NORTH

            # Update position
            player_y -= 1
            messages.append("You move north.")

            # Render updated state
            display.clear()
            display.render_map(map_data, player_x, player_y)
            display.render_status({"hp": 10, "max_hp": 10})
            display.render_messages(messages)
            display.refresh()

            display.cleanup()

    def test_help_and_quit_scenario(self):
        """Test help request followed by quit."""
        mock_term_input = MagicMock()
        input_handler = TerminalInputHandler(terminal=mock_term_input)

        # User presses '?'
        mock_key = Mock()
        mock_key.is_sequence = False
        mock_key.__str__ = Mock(return_value="?")
        mock_key.__bool__ = Mock(return_value=True)
        mock_term_input.inkey.return_value = mock_key
        mock_term_input.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term_input.cbreak.return_value.__exit__ = Mock(return_value=None)

        action = input_handler.get_input()
        assert action == InputAction.HELP

        # User presses 'q'
        mock_key.__str__ = Mock(return_value="q")
        action = input_handler.get_input()
        assert action == InputAction.QUIT

    def test_diagonal_movement_scenario(self):
        """Test diagonal movement using vi-keys."""
        mock_term_input = MagicMock()
        input_handler = TerminalInputHandler(terminal=mock_term_input)

        diagonal_moves = [
            ("y", InputAction.MOVE_NORTHWEST),
            ("u", InputAction.MOVE_NORTHEAST),
            ("b", InputAction.MOVE_SOUTHWEST),
            ("n", InputAction.MOVE_SOUTHEAST),
        ]

        for key_char, expected_action in diagonal_moves:
            mock_key = Mock()
            mock_key.is_sequence = False
            mock_key.__str__ = Mock(return_value=key_char)
            mock_key.__bool__ = Mock(return_value=True)
            mock_term_input.inkey.return_value = mock_key
            mock_term_input.cbreak.return_value.__enter__ = Mock(return_value=None)
            mock_term_input.cbreak.return_value.__exit__ = Mock(return_value=None)

            action = input_handler.get_input()
            assert action == expected_action
