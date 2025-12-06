"""Save/load management for game state persistence.

This module provides functions to serialize and deserialize WorldState
objects to and from YAML and JSON formats.
"""

import json
import logging
from pathlib import Path

import yaml

from src.world.world_state import WorldState

logger = logging.getLogger(__name__)


def save(world_state: WorldState, path: str | Path, format: str = "yaml") -> None:
    """Save a WorldState to a file.

    Args:
        world_state: The WorldState instance to serialize.
        path: Path to the file where the state should be saved.
        format: File format, either "yaml" or "json". Defaults to "yaml".

    Raises:
        ValueError: If an unsupported format is specified.
        IOError: If the file cannot be written.
    """
    path = Path(path)
    data = world_state.to_dict()

    try:
        if format.lower() == "yaml":
            with open(path, "w") as f:
                yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
            logger.info("Saved WorldState to %s (YAML format)", path)
        elif format.lower() == "json":
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved WorldState to %s (JSON format)", path)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'yaml' or 'json'.")
    except Exception as e:
        logger.error("Failed to save WorldState to %s: %s", path, e)
        raise


def load(path: str | Path) -> WorldState:
    """Load a WorldState from a file.

    The format (YAML or JSON) is automatically detected based on file extension.
    If the extension is not recognized, YAML is attempted first, then JSON.

    Args:
        path: Path to the file to load.

    Returns:
        A WorldState instance restored from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be parsed or contains invalid data.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        # Detect format by extension
        ext = path.suffix.lower()
        if ext in [".yaml", ".yml"]:
            with open(path) as f:
                data = yaml.safe_load(f)
            logger.info("Loaded WorldState from %s (YAML format)", path)
        elif ext == ".json":
            with open(path) as f:
                data = json.load(f)
            logger.info("Loaded WorldState from %s (JSON format)", path)
        else:
            # Try YAML first, then JSON if that fails
            try:
                with open(path) as f:
                    data = yaml.safe_load(f)
                logger.info("Loaded WorldState from %s (auto-detected YAML)", path)
            except yaml.YAMLError:
                with open(path) as f:
                    data = json.load(f)
                logger.info("Loaded WorldState from %s (auto-detected JSON)", path)

        return WorldState.from_dict(data)
    except Exception as e:
        logger.error("Failed to load WorldState from %s: %s", path, e)
        raise
