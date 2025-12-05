"""Unit tests for the Display abstract base class.

These tests verify that the Display ABC is properly defined and that
concrete implementations can be created following the interface.
"""

import pytest

from src.ui.display import Display


class MockDisplay(Display):
    """Mock implementation of Display for testing."""

    def __init__(self):
        self.initialized = False
        self.cleaned_up = False
        self.cleared = False
        self.map_rendered = False
        self.status_rendered = False
        self.messages_rendered = False
        self.refreshed = False

    def initialize(self) -> None:
        self.initialized = True

    def cleanup(self) -> None:
        self.cleaned_up = True

    def clear(self) -> None:
        self.cleared = True

    def render_map(self, map_data, player_x, player_y) -> None:
        self.map_rendered = True

    def render_status(self, status_data) -> None:
        self.status_rendered = True

    def render_messages(self, messages) -> None:
        self.messages_rendered = True

    def refresh(self) -> None:
        self.refreshed = True

    def get_dimensions(self):
        return (80, 24)


class TestDisplayAbstractClass:
    """Tests for the Display abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that Display cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Display()

    def test_mock_display_implements_interface(self):
        """Test that a concrete implementation can be created."""
        display = MockDisplay()
        assert isinstance(display, Display)

    def test_context_manager_calls_initialize_and_cleanup(self):
        """Test that using Display as context manager calls initialize and cleanup."""
        display = MockDisplay()

        assert not display.initialized
        assert not display.cleaned_up

        with display:
            assert display.initialized
            assert not display.cleaned_up

        assert display.cleaned_up

    def test_all_abstract_methods_must_be_implemented(self):
        """Test that all abstract methods must be implemented."""

        # Create a class that doesn't implement all methods
        class IncompleteDisplay(Display):
            def initialize(self):
                pass

            # Missing other required methods

        with pytest.raises(TypeError):
            IncompleteDisplay()


class TestMockDisplay:
    """Tests for the MockDisplay implementation."""

    def test_initialize_sets_flag(self):
        """Test that initialize sets the initialized flag."""
        display = MockDisplay()
        assert not display.initialized
        display.initialize()
        assert display.initialized

    def test_cleanup_sets_flag(self):
        """Test that cleanup sets the cleaned_up flag."""
        display = MockDisplay()
        assert not display.cleaned_up
        display.cleanup()
        assert display.cleaned_up

    def test_clear_sets_flag(self):
        """Test that clear sets the cleared flag."""
        display = MockDisplay()
        assert not display.cleared
        display.clear()
        assert display.cleared

    def test_render_map_sets_flag(self):
        """Test that render_map sets the map_rendered flag."""
        display = MockDisplay()
        assert not display.map_rendered
        display.render_map([], 0, 0)
        assert display.map_rendered

    def test_render_status_sets_flag(self):
        """Test that render_status sets the status_rendered flag."""
        display = MockDisplay()
        assert not display.status_rendered
        display.render_status({})
        assert display.status_rendered

    def test_render_messages_sets_flag(self):
        """Test that render_messages sets the messages_rendered flag."""
        display = MockDisplay()
        assert not display.messages_rendered
        display.render_messages([])
        assert display.messages_rendered

    def test_refresh_sets_flag(self):
        """Test that refresh sets the refreshed flag."""
        display = MockDisplay()
        assert not display.refreshed
        display.refresh()
        assert display.refreshed

    def test_get_dimensions_returns_tuple(self):
        """Test that get_dimensions returns a tuple."""
        display = MockDisplay()
        dimensions = display.get_dimensions()
        assert isinstance(dimensions, tuple)
        assert len(dimensions) == 2
        assert dimensions == (80, 24)
