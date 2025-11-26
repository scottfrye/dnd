"""Configuration loader module.

This module provides utilities for loading configuration from YAML files
with support for default values when files are missing.
"""

import copy
import os
from typing import Any

import yaml


# Default configuration values
DEFAULT_CONFIG = {
    "logging": {
        "level": "INFO",
    },
    "data": {
        "path": "data",
    },
    "save": {
        "format": "json",
    },
}


def load_config(path: str = "config.yaml") -> dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        path: Path to the YAML configuration file. Defaults to "config.yaml".

    Returns:
        A dictionary containing the configuration values. If the file does not
        exist or cannot be read, returns the default configuration.
    """
    if not os.path.exists(path):
        return copy.deepcopy(DEFAULT_CONFIG)

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if config is None:
                return copy.deepcopy(DEFAULT_CONFIG)
            return copy.deepcopy(config)
    except (yaml.YAMLError, OSError):
        return copy.deepcopy(DEFAULT_CONFIG)
