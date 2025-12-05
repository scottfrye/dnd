"""Unit tests for the TerminalDisplay implementation.

These tests verify that the TerminalDisplay correctly implements the Display
interface using the blessed library.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from src.ui.display import Display
from src.ui.terminal_display import TerminalDisplay


class TestTerminalDisplay:
    """Tests for the TerminalDisplay implementation."""

    def test_is_display_implementation(self):
        """Test that TerminalDisplay implements the Display interface."""
        with patch("src.ui.terminal_display.Terminal"):
            display = TerminalDisplay()
            assert isinstance(display, Display)

    def test_initialization_with_default_terminal(self):
        """Test that TerminalDisplay can be created with default Terminal."""
        with patch("src.ui.terminal_display.Terminal") as mock_terminal:
            display = TerminalDisplay()
            assert display.term is not None
            mock_terminal.assert_called_once()

    def test_initialization_with_provided_terminal(self):
        """Test that TerminalDisplay can be created with a provided Terminal."""
        mock_term = MagicMock()
        display = TerminalDisplay(terminal=mock_term)
        assert display.term is mock_term

    def test_initialize_clears_screen(self):
        """Test that initialize clears the screen."""
        mock_term = MagicMock()
        mock_term.clear = "CLEAR"
        display = TerminalDisplay(terminal=mock_term)

        with patch("builtins.print") as mock_print:
            display.initialize()
            # Should call print with clear
            assert any("CLEAR" in str(call) for call in mock_print.call_args_list)

    def test_cleanup_restores_terminal(self):
        """Test that cleanup restores terminal state."""
        mock_term = MagicMock()
        mock_term.normal_cursor = "NORMAL_CURSOR"
        mock_term.normal = "NORMAL"
        display = TerminalDisplay(terminal=mock_term)

        with patch("builtins.print") as mock_print:
            display.initialize()
            display.cleanup()
            # Should call print with normal cursor and normal
            print_calls = [str(call) for call in mock_print.call_args_list]
            assert any("NORMAL_CURSOR" in call for call in print_calls)
            assert any("NORMAL" in call for call in print_calls)

    def test_clear_calls_terminal_clear(self):
        """Test that clear calls terminal.clear."""
        mock_term = MagicMock()
        mock_term.clear = "CLEAR_SCREEN"
        display = TerminalDisplay(terminal=mock_term)

        with patch("builtins.print") as mock_print:
            display.clear()
            mock_print.assert_called()

    def test_render_map_displays_grid(self):
        """Test that render_map displays a grid with player position."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.bold_green.return_value = "@"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        map_data = [
            [".", ".", "."],
            [".", ".", "."],
            [".", ".", "."],
        ]

        with patch("builtins.print"):
            display.render_map(map_data, player_x=1, player_y=1)
            # Should have called bold_green for player position
            mock_term.bold_green.assert_called_with("@")

    def test_render_status_displays_character_info(self):
        """Test that render_status displays character information."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        status_data = {"hp": 10, "max_hp": 15, "level": 3}

        with patch("builtins.print") as mock_print:
            display.render_status(status_data)
            # Should have called print with status data
            mock_print.assert_called()

    def test_render_messages_displays_message_list(self):
        """Test that render_messages displays a list of messages."""
        mock_term = MagicMock()
        mock_term.bold.return_value = "BOLD"
        mock_term.clear_eol = "CLEAR_EOL"
        mock_term.location.return_value.__enter__ = Mock(return_value=None)
        mock_term.location.return_value.__exit__ = Mock(return_value=None)

        display = TerminalDisplay(terminal=mock_term)

        messages = ["You hit the goblin!", "The goblin dies.", "You gain 10 XP."]

        with patch("builtins.print") as mock_print:
            display.render_messages(messages)
            # Should have called print with messages
            mock_print.assert_called()

    def test_refresh_flushes_stdout(self):
        """Test that refresh flushes stdout."""
        mock_term = MagicMock()
        display = TerminalDisplay(terminal=mock_term)

        with patch("sys.stdout") as mock_stdout:
            display.refresh()
            mock_stdout.flush.assert_called_once()

    def test_get_dimensions_returns_terminal_size(self):
        """Test that get_dimensions returns terminal width and height."""
        mock_term = MagicMock()
        mock_term.width = 100
        mock_term.height = 40

        display = TerminalDisplay(terminal=mock_term)
        dimensions = display.get_dimensions()

        assert dimensions == (100, 40)

    def test_context_manager_initializes_and_cleans_up(self):
        """Test that using TerminalDisplay as context manager works."""
        mock_term = MagicMock()
        mock_term.clear = "CLEAR"
        mock_term.normal_cursor = "NORMAL_CURSOR"
        mock_term.normal = "NORMAL"

        with patch("builtins.print"):
            with TerminalDisplay(terminal=mock_term) as display:
                assert display._initialized
            # After context, should be cleaned up
            assert not display._initialized
