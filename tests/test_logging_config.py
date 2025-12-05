"""Unit tests for the logging configuration module.

These tests verify that the logging configuration module correctly:
- Sets the logger level based on configuration
- Creates a log file when specified
- Supports both console and file handlers
"""

import logging
import os
import tempfile

from src.logging_config import setup_logging


def _cleanup_handlers(logger: logging.Logger) -> None:
    """Close and remove all handlers from a logger.
    
    This is necessary on Windows where file handlers keep files open,
    preventing temporary directory cleanup.
    
    Args:
        logger: The logger whose handlers should be cleaned up.
    """
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def test_setup_logging_sets_logger_level():
    """Test that setup_logging sets the correct logger level."""
    config = {"logging": {"level": "DEBUG"}}

    root_logger = setup_logging(config)

    assert root_logger.level == logging.DEBUG


def test_setup_logging_creates_log_file_in_temp_directory():
    """Test that setup_logging creates a log file in a temp directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = os.path.join(temp_dir, "test.log")
        config = {"logging": {"level": "INFO", "file": log_file}}

        root_logger = setup_logging(config)

        # Write a log message to trigger file creation
        test_logger = logging.getLogger("test_logger")
        test_logger.info("Test log message")

        # Verify the log file exists
        assert os.path.exists(log_file)

        # Verify the log file contains the message
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Test log message" in content

        # Clean up handlers to release file handles (important for Windows)
        _cleanup_handlers(root_logger)


def test_setup_logging_with_default_level():
    """Test that setup_logging uses INFO as default level."""
    config = {"logging": {}}

    root_logger = setup_logging(config)

    assert root_logger.level == logging.INFO


def test_setup_logging_with_empty_config():
    """Test that setup_logging handles empty config gracefully."""
    config = {}

    root_logger = setup_logging(config)

    assert root_logger.level == logging.INFO


def test_setup_logging_creates_console_handler():
    """Test that setup_logging creates a console handler."""
    config = {"logging": {"level": "WARNING"}}

    root_logger = setup_logging(config)

    # Check that there's exactly one StreamHandler (console handler)
    stream_handlers = [
        h
        for h in root_logger.handlers
        if isinstance(h, logging.StreamHandler)
        and not isinstance(h, logging.FileHandler)
    ]
    assert len(stream_handlers) == 1


def test_setup_logging_creates_file_handler_when_file_specified():
    """Test that setup_logging creates a file handler when file is specified."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = os.path.join(temp_dir, "test.log")
        config = {"logging": {"level": "INFO", "file": log_file}}

        root_logger = setup_logging(config)

        # Check that there's a FileHandler
        file_handlers = [
            h for h in root_logger.handlers if isinstance(h, logging.FileHandler)
        ]
        assert len(file_handlers) == 1

        # Clean up handlers to release file handles (important for Windows)
        _cleanup_handlers(root_logger)


def test_setup_logging_creates_nested_directories():
    """Test that setup_logging creates nested directories for log file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = os.path.join(temp_dir, "nested", "dir", "test.log")
        config = {"logging": {"level": "INFO", "file": log_file}}

        root_logger = setup_logging(config)

        # Write a log message to trigger file creation
        test_logger = logging.getLogger("nested_test")
        test_logger.info("Nested directory test")

        assert os.path.exists(log_file)

        # Clean up handlers to release file handles (important for Windows)
        _cleanup_handlers(root_logger)
