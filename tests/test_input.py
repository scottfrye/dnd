"""Unit tests for the InputHandler abstract base class.

These tests verify that the InputHandler ABC is properly defined and that
the InputAction enumeration works correctly.
"""

import pytest

from src.ui.input import InputAction, InputHandler


class MockInputHandler(InputHandler):
    """Mock implementation of InputHandler for testing."""

    def __init__(self):
        self.initialized = False
        self.cleaned_up = False
        self.next_action = InputAction.WAIT
        self.next_key = "k"

    def initialize(self) -> None:
        self.initialized = True

    def cleanup(self) -> None:
        self.cleaned_up = True

    def get_input(self, timeout=None):
        return self.next_action

    def get_key(self, timeout=None):
        return self.next_key


class TestInputAction:
    """Tests for the InputAction enumeration."""

    def test_movement_actions_exist(self):
        """Test that all movement actions are defined."""
        assert InputAction.MOVE_NORTH
        assert InputAction.MOVE_SOUTH
        assert InputAction.MOVE_EAST
        assert InputAction.MOVE_WEST
        assert InputAction.MOVE_NORTHEAST
        assert InputAction.MOVE_NORTHWEST
        assert InputAction.MOVE_SOUTHEAST
        assert InputAction.MOVE_SOUTHWEST

    def test_game_actions_exist(self):
        """Test that game actions are defined."""
        assert InputAction.WAIT
        assert InputAction.PICKUP
        assert InputAction.INVENTORY
        assert InputAction.USE
        assert InputAction.DROP
        assert InputAction.CAST_SPELL
        assert InputAction.LOOK

    def test_ui_actions_exist(self):
        """Test that UI actions are defined."""
        assert InputAction.HELP
        assert InputAction.QUIT
        assert InputAction.SAVE

    def test_unknown_action_exists(self):
        """Test that UNKNOWN action exists for unmapped input."""
        assert InputAction.UNKNOWN

    def test_action_values_are_strings(self):
        """Test that action values are strings."""
        assert isinstance(InputAction.MOVE_NORTH.value, str)
        assert InputAction.MOVE_NORTH.value == "move_north"


class TestInputHandlerAbstractClass:
    """Tests for the InputHandler abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that InputHandler cannot be instantiated directly."""
        with pytest.raises(TypeError):
            InputHandler()

    def test_mock_input_handler_implements_interface(self):
        """Test that a concrete implementation can be created."""
        handler = MockInputHandler()
        assert isinstance(handler, InputHandler)

    def test_context_manager_calls_initialize_and_cleanup(self):
        """Test that using InputHandler as context manager calls initialize and cleanup."""
        handler = MockInputHandler()

        assert not handler.initialized
        assert not handler.cleaned_up

        with handler:
            assert handler.initialized
            assert not handler.cleaned_up

        assert handler.cleaned_up

    def test_all_abstract_methods_must_be_implemented(self):
        """Test that all abstract methods must be implemented."""

        # Create a class that doesn't implement all methods
        class IncompleteInputHandler(InputHandler):
            def initialize(self):
                pass

            # Missing other required methods

        with pytest.raises(TypeError):
            IncompleteInputHandler()


class TestMockInputHandler:
    """Tests for the MockInputHandler implementation."""

    def test_initialize_sets_flag(self):
        """Test that initialize sets the initialized flag."""
        handler = MockInputHandler()
        assert not handler.initialized
        handler.initialize()
        assert handler.initialized

    def test_cleanup_sets_flag(self):
        """Test that cleanup sets the cleaned_up flag."""
        handler = MockInputHandler()
        assert not handler.cleaned_up
        handler.cleanup()
        assert handler.cleaned_up

    def test_get_input_returns_action(self):
        """Test that get_input returns an InputAction."""
        handler = MockInputHandler()
        action = handler.get_input()
        assert isinstance(action, InputAction)
        assert action == InputAction.WAIT

    def test_get_key_returns_string(self):
        """Test that get_key returns a string."""
        handler = MockInputHandler()
        key = handler.get_key()
        assert isinstance(key, str)
        assert key == "k"

    def test_get_input_can_return_different_actions(self):
        """Test that get_input can return different actions."""
        handler = MockInputHandler()
        handler.next_action = InputAction.MOVE_NORTH
        assert handler.get_input() == InputAction.MOVE_NORTH

        handler.next_action = InputAction.QUIT
        assert handler.get_input() == InputAction.QUIT
