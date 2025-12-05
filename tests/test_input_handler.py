"""Unit tests for the TerminalInputHandler implementation.

These tests verify that the TerminalInputHandler correctly implements the
InputHandler interface using the blessed library.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from src.ui.input import InputAction, InputHandler
from src.ui.input_handler import TerminalInputHandler


class TestTerminalInputHandler:
    """Tests for the TerminalInputHandler implementation."""

    def test_is_input_handler_implementation(self):
        """Test that TerminalInputHandler implements the InputHandler interface."""
        with patch("src.ui.input_handler.Terminal"):
            handler = TerminalInputHandler()
            assert isinstance(handler, InputHandler)

    def test_initialization_with_default_terminal(self):
        """Test that TerminalInputHandler can be created with default Terminal."""
        with patch("src.ui.input_handler.Terminal") as mock_terminal:
            handler = TerminalInputHandler()
            assert handler.term is not None
            mock_terminal.assert_called_once()

    def test_initialization_with_provided_terminal(self):
        """Test that TerminalInputHandler can be created with a provided Terminal."""
        mock_term = MagicMock()
        handler = TerminalInputHandler(terminal=mock_term)
        assert handler.term is mock_term

    def test_vi_keys_mapped_to_movement(self):
        """Test that vi-keys are mapped to movement actions."""
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["h"] == InputAction.MOVE_WEST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["j"] == InputAction.MOVE_SOUTH
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["k"] == InputAction.MOVE_NORTH
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["l"] == InputAction.MOVE_EAST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["y"] == InputAction.MOVE_NORTHWEST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["u"] == InputAction.MOVE_NORTHEAST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["b"] == InputAction.MOVE_SOUTHWEST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["n"] == InputAction.MOVE_SOUTHEAST

    def test_arrow_keys_mapped_to_movement(self):
        """Test that arrow keys are mapped to movement actions."""
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["KEY_LEFT"] == InputAction.MOVE_WEST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["KEY_RIGHT"] == InputAction.MOVE_EAST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["KEY_UP"] == InputAction.MOVE_NORTH
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["KEY_DOWN"] == InputAction.MOVE_SOUTH

    def test_numpad_keys_mapped_to_movement(self):
        """Test that numpad keys are mapped to movement actions."""
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["4"] == InputAction.MOVE_WEST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["6"] == InputAction.MOVE_EAST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["8"] == InputAction.MOVE_NORTH
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["2"] == InputAction.MOVE_SOUTH
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["7"] == InputAction.MOVE_NORTHWEST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["9"] == InputAction.MOVE_NORTHEAST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["1"] == InputAction.MOVE_SOUTHWEST
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["3"] == InputAction.MOVE_SOUTHEAST

    def test_game_action_keys_mapped(self):
        """Test that game action keys are mapped correctly."""
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["."] == InputAction.WAIT
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["5"] == InputAction.WAIT
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS[","] == InputAction.PICKUP
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["g"] == InputAction.PICKUP
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["i"] == InputAction.INVENTORY
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["a"] == InputAction.USE
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["d"] == InputAction.DROP
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["c"] == InputAction.CAST_SPELL
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS[";"] == InputAction.LOOK

    def test_ui_action_keys_mapped(self):
        """Test that UI action keys are mapped correctly."""
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["?"] == InputAction.HELP
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["q"] == InputAction.QUIT
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["Q"] == InputAction.QUIT
        assert TerminalInputHandler.DEFAULT_KEY_MAPPINGS["S"] == InputAction.SAVE

    def test_get_input_returns_mapped_action(self):
        """Test that get_input returns the correct InputAction for a key."""
        mock_term = MagicMock()
        mock_key = Mock()
        mock_key.is_sequence = False
        mock_key.__str__ = Mock(return_value="k")
        mock_key.__bool__ = Mock(return_value=True)
        mock_term.inkey.return_value = mock_key
        mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

        handler = TerminalInputHandler(terminal=mock_term)
        action = handler.get_input()

        assert action == InputAction.MOVE_NORTH

    def test_get_input_returns_unknown_for_unmapped_key(self):
        """Test that get_input returns UNKNOWN for unmapped keys."""
        mock_term = MagicMock()
        mock_key = Mock()
        mock_key.is_sequence = False
        mock_key.__str__ = Mock(return_value="x")
        mock_key.__bool__ = Mock(return_value=True)
        mock_term.inkey.return_value = mock_key
        mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

        handler = TerminalInputHandler(terminal=mock_term)
        action = handler.get_input()

        assert action == InputAction.UNKNOWN

    def test_get_key_returns_character_for_normal_key(self):
        """Test that get_key returns the character for normal keys."""
        mock_term = MagicMock()
        mock_key = Mock()
        mock_key.is_sequence = False
        mock_key.__str__ = Mock(return_value="a")
        mock_key.__bool__ = Mock(return_value=True)
        mock_term.inkey.return_value = mock_key
        mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

        handler = TerminalInputHandler(terminal=mock_term)
        key = handler.get_key()

        assert key == "a"

    def test_get_key_returns_name_for_special_key(self):
        """Test that get_key returns the name for special keys."""
        mock_term = MagicMock()
        mock_key = Mock()
        mock_key.is_sequence = True
        mock_key.name = "KEY_LEFT"
        mock_key.__bool__ = Mock(return_value=True)
        mock_term.inkey.return_value = mock_key
        mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

        handler = TerminalInputHandler(terminal=mock_term)
        key = handler.get_key()

        assert key == "KEY_LEFT"

    def test_get_key_returns_none_on_timeout(self):
        """Test that get_key returns None when timeout occurs."""
        mock_term = MagicMock()
        mock_term.inkey.return_value = ""  # Empty string indicates timeout
        mock_term.cbreak.return_value.__enter__ = Mock(return_value=None)
        mock_term.cbreak.return_value.__exit__ = Mock(return_value=None)

        handler = TerminalInputHandler(terminal=mock_term)
        key = handler.get_key(timeout=0.1)

        assert key is None

    def test_add_key_mapping(self):
        """Test that key mappings can be added dynamically."""
        mock_term = MagicMock()
        handler = TerminalInputHandler(terminal=mock_term)

        handler.add_key_mapping("z", InputAction.SAVE)
        assert handler.get_key_mapping("z") == InputAction.SAVE

    def test_remove_key_mapping(self):
        """Test that key mappings can be removed."""
        mock_term = MagicMock()
        handler = TerminalInputHandler(terminal=mock_term)

        handler.add_key_mapping("z", InputAction.SAVE)
        assert handler.get_key_mapping("z") == InputAction.SAVE

        handler.remove_key_mapping("z")
        assert handler.get_key_mapping("z") is None

    def test_get_key_mapping_returns_none_for_unmapped(self):
        """Test that get_key_mapping returns None for unmapped keys."""
        mock_term = MagicMock()
        handler = TerminalInputHandler(terminal=mock_term)

        assert handler.get_key_mapping("unmapped_key") is None

    def test_context_manager_initializes_and_cleans_up(self):
        """Test that using TerminalInputHandler as context manager works."""
        mock_term = MagicMock()

        with TerminalInputHandler(terminal=mock_term) as handler:
            assert handler._initialized

        assert not handler._initialized

    def test_instance_level_key_mappings_do_not_affect_other_instances(self):
        """Test that modifying key mappings in one instance doesn't affect others."""
        mock_term1 = MagicMock()
        mock_term2 = MagicMock()

        handler1 = TerminalInputHandler(terminal=mock_term1)
        handler2 = TerminalInputHandler(terminal=mock_term2)

        # Add a custom mapping to handler1
        handler1.add_key_mapping("z", InputAction.SAVE)

        # Verify handler1 has the mapping
        assert handler1.get_key_mapping("z") == InputAction.SAVE

        # Verify handler2 doesn't have the mapping
        assert handler2.get_key_mapping("z") is None

        # Verify both handlers still have the default mappings
        assert handler1.get_key_mapping("k") == InputAction.MOVE_NORTH
        assert handler2.get_key_mapping("k") == InputAction.MOVE_NORTH
