"""Unit tests for the configuration loader module.

These tests verify that the configuration loader correctly:
- Returns default values when the config file is absent
- Reads values from a provided config file
"""

import os
import tempfile

from src.config import DEFAULT_CONFIG, load_config


def test_load_config_returns_defaults_when_file_absent():
    """Test that load_config returns default values when file doesn't exist."""
    # Use a path that definitely doesn't exist
    result = load_config("/nonexistent/path/config.yaml")

    assert result == DEFAULT_CONFIG
    assert result["logging"]["level"] == "INFO"
    assert result["data"]["path"] == "data"
    assert result["save"]["format"] == "json"


def test_load_config_reads_provided_values():
    """Test that load_config reads values from an existing config file."""
    # Create a temporary config file with custom values
    config_content = """
logging:
  level: DEBUG
data:
  path: /custom/data/path
save:
  format: yaml
"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as f:
        f.write(config_content)
        temp_path = f.name

    try:
        result = load_config(temp_path)

        assert result["logging"]["level"] == "DEBUG"
        assert result["data"]["path"] == "/custom/data/path"
        assert result["save"]["format"] == "yaml"
    finally:
        os.unlink(temp_path)


def test_load_config_returns_defaults_for_empty_file():
    """Test that load_config returns defaults for an empty config file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as f:
        f.write("")
        temp_path = f.name

    try:
        result = load_config(temp_path)
        assert result == DEFAULT_CONFIG
    finally:
        os.unlink(temp_path)


def test_load_config_default_returns_copy():
    """Test that load_config returns a copy of defaults, not the original."""
    result = load_config("/nonexistent/path/config.yaml")

    # Modify the returned dict
    result["logging"]["level"] = "MODIFIED"

    # Load again and verify the default was not modified
    result2 = load_config("/nonexistent/path/config.yaml")
    assert result2["logging"]["level"] == "INFO"
