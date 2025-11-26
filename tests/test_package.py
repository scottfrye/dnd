"""Basic package import tests.

These tests verify that all packages can be imported without errors,
which confirms the packaging configuration is correct.
"""


def test_src_package_import():
    """Test that the src package can be imported."""
    import src  # noqa: F401


def test_src_rules_import():
    """Test that the rules subpackage can be imported."""
    import src.rules  # noqa: F401


def test_src_entities_import():
    """Test that the entities subpackage can be imported."""
    import src.entities  # noqa: F401


def test_src_game_import():
    """Test that the game subpackage can be imported."""
    import src.game  # noqa: F401


def test_src_world_import():
    """Test that the world subpackage can be imported."""
    import src.world  # noqa: F401


def test_src_ui_import():
    """Test that the ui subpackage can be imported."""
    import src.ui  # noqa: F401


def test_src_simulation_import():
    """Test that the simulation subpackage can be imported."""
    import src.simulation  # noqa: F401


def test_src_persistence_import():
    """Test that the persistence subpackage can be imported."""
    import src.persistence  # noqa: F401
