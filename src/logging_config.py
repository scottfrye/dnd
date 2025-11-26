"""Logging configuration module.

This module provides utilities for setting up logging with support for
console and file handlers.
"""

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def setup_logging(config: dict[str, Any]) -> logging.Logger:
    """Set up logging based on the provided configuration.

    Args:
        config: Configuration dictionary. Expected structure:
            {
                "logging": {
                    "level": "INFO",  # Optional, defaults to INFO
                    "file": "/path/to/logfile.log"  # Optional
                }
            }

    Returns:
        The root logger configured with the specified handlers.
    """
    logging_config = config.get("logging", {})
    level_str = logging_config.get("level", "INFO")
    log_file = logging_config.get("file")

    # Convert level string to logging constant
    level = getattr(logging, level_str.upper(), logging.INFO)

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates when called multiple times
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Add file handler if file path is specified
    if log_file:
        # Ensure the directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    root_logger.debug("Logging configured with level: %s", level_str)

    return root_logger
