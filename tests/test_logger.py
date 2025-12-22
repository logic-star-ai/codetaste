"""Tests for logger utility."""
import logging
from pathlib import Path

import pytest

from refactoring_benchmark.utils.logger import setup_logging, get_logger


pytestmark = pytest.mark.unit


class TestLogging:
    """Tests for logging functionality."""

    def test_setup_logging(self, temp_dir: Path):
        """Test setup_logging creates log directory."""
        log_dir = temp_dir / "logs"
        assert not log_dir.exists()

        setup_logging(str(log_dir))

        assert log_dir.exists()
        assert log_dir.is_dir()

    def test_get_logger_basic(self, temp_dir: Path):
        """Test getting a basic logger."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        logger = get_logger("test_logger")

        assert logger is not None
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_get_logger_with_file(self, temp_dir: Path):
        """Test logger with file output."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        logger = get_logger("test_file_logger", use_file=True, use_stdout=False)

        # Log a message
        logger.info("Test message")

        # Verify log file was created
        log_file = log_dir / "test_file_logger.log"
        assert log_file.exists()

        # Verify content
        content = log_file.read_text()
        assert "Test message" in content
        assert "INFO" in content

    def test_get_logger_with_stdout(self, temp_dir: Path):
        """Test logger with stdout output."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        logger = get_logger("test_stdout_logger", use_file=False, use_stdout=True)

        # Verify logger has a StreamHandler
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "StreamHandler" in handler_types, "Logger should have a StreamHandler for stdout"

    def test_get_logger_both_outputs(self, temp_dir: Path):
        """Test logger with both file and stdout."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        logger = get_logger("test_both_logger", use_file=True, use_stdout=True)

        # Log a message
        logger.info("Both outputs message")

        # Verify file was created
        log_file = log_dir / "test_both_logger.log"
        assert log_file.exists()
        assert "Both outputs message" in log_file.read_text()

    def test_get_logger_level(self, temp_dir: Path):
        """Test logger respects level parameter."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        logger = get_logger("test_level_logger", use_file=True, level=logging.WARNING)

        # Log at different levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        # Verify only warning and above were logged
        log_file = log_dir / "test_level_logger.log"
        content = log_file.read_text()

        assert "Debug message" not in content
        assert "Info message" not in content
        assert "Warning message" in content
        assert "Error message" in content

    def test_get_logger_no_duplicate_handlers(self, temp_dir: Path):
        """Test that calling get_logger multiple times doesn't add duplicate handlers."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        # Get the same logger multiple times
        logger1 = get_logger("test_dup_logger", use_file=True)
        logger2 = get_logger("test_dup_logger", use_file=True)
        logger3 = get_logger("test_dup_logger", use_file=True)

        # All should be the same instance
        assert logger1 is logger2
        assert logger2 is logger3

        # Handler count should not increase
        # Should have at most 1 file handler and 1 console handler
        handler_types = [type(h).__name__ for h in logger1.handlers]
        file_handlers = handler_types.count("FileHandler")
        stream_handlers = handler_types.count("StreamHandler")

        # Should not have more than 1 of each type
        assert file_handlers <= 1
        assert stream_handlers <= 1

    def test_logger_propagation_disabled(self, temp_dir: Path):
        """Test that logger propagation is disabled."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        logger = get_logger("test_propagation_logger")

        # Propagation should be disabled to avoid duplicate logs
        assert logger.propagate is False

    def test_multiple_loggers_separate_files(self, temp_dir: Path):
        """Test that multiple loggers write to separate files."""
        log_dir = temp_dir / "logs"
        setup_logging(str(log_dir))

        logger1 = get_logger("logger1", use_file=True)
        logger2 = get_logger("logger2", use_file=True)

        logger1.info("Message from logger1")
        logger2.info("Message from logger2")

        # Verify separate log files
        log1 = log_dir / "logger1.log"
        log2 = log_dir / "logger2.log"

        assert log1.exists()
        assert log2.exists()

        content1 = log1.read_text()
        content2 = log2.read_text()

        assert "Message from logger1" in content1
        assert "Message from logger2" not in content1

        assert "Message from logger2" in content2
        assert "Message from logger1" not in content2
