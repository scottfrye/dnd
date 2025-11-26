"""Basic package import tests."""

import pytest


def test_src_package_import():
    """Test that the src package can be imported."""
    import src

    assert src is not None


def test_src_rules_import():
    """Test that the rules subpackage can be imported."""
    import src.rules

    assert src.rules is not None


def test_src_entities_import():
    """Test that the entities subpackage can be imported."""
    import src.entities

    assert src.entities is not None


def test_src_game_import():
    """Test that the game subpackage can be imported."""
    import src.game

    assert src.game is not None


def test_src_world_import():
    """Test that the world subpackage can be imported."""
    import src.world

    assert src.world is not None


def test_src_ui_import():
    """Test that the ui subpackage can be imported."""
    import src.ui

    assert src.ui is not None


def test_src_simulation_import():
    """Test that the simulation subpackage can be imported."""
    import src.simulation

    assert src.simulation is not None


def test_src_persistence_import():
    """Test that the persistence subpackage can be imported."""
    import src.persistence

    assert src.persistence is not None
