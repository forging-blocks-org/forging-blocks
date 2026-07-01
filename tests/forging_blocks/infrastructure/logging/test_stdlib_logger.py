"""
Tests for the StdlibLogger implementation.
"""

import logging
from typing import Any, Protocol, runtime_checkable

import pytest

from forging_blocks.infrastructure.logging.stdlib_logger import StdlibLogger


@runtime_checkable
class _LoggerProto(Protocol):
    def debug(self, msg: str, *args: object) -> None: ...

    def info(self, msg: str, *args: object) -> None: ...

    def warning(self, msg: str, *args: object) -> None: ...

    def error(self, msg: str, *args: object) -> None: ...


class TestLoggerPort:
    """Tests for the LoggerPort protocol."""

    def test_logger_is_protocol(self) -> None:
        """Test that LoggerPort is a protocol."""
        assert isinstance(StdlibLogger(), _LoggerProto)

    def test_logger_methods(self) -> None:
        """Test that LoggerPort has required methods."""
        logger: Any = StdlibLogger()
        assert callable(logger.debug)
        assert callable(logger.info)
        assert callable(logger.warning)
        assert callable(logger.error)


class TestStdlibLogger:
    """Tests for the StdlibLogger implementation."""

    def test_creation_with_default_name(self) -> None:
        """Test creating logger with default name."""
        logger: Any = StdlibLogger()
        assert logger._logger.name == "forging_blocks"

    def test_creation_with_custom_name(self) -> None:
        """Test creating logger with custom name."""
        logger: Any = StdlibLogger("custom.name")
        assert logger._logger.name == "custom.name"

    def test_debug_logs(self, caplog: pytest.LogCaptureFixture):
        """Test debug logging."""
        logger = StdlibLogger("test.debug")
        with caplog.at_level(logging.DEBUG, logger="test.debug"):
            logger.debug("Debug message: %s", "value")
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "DEBUG"
        assert caplog.records[0].message == "Debug message: value"

    def test_info_logs(self, caplog: pytest.LogCaptureFixture):
        """Test info logging."""
        logger = StdlibLogger("test.info")
        with caplog.at_level(logging.INFO, logger="test.info"):
            logger.info("Info message: %s", "value")
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "INFO"
        assert caplog.records[0].message == "Info message: value"

    def test_warning_logs(self, caplog: pytest.LogCaptureFixture):
        """Test warning logging."""
        logger = StdlibLogger("test.warning")
        with caplog.at_level(logging.WARNING, logger="test.warning"):
            logger.warning("Warning message: %s", "value")
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "WARNING"
        assert caplog.records[0].message == "Warning message: value"

    def test_error_logs(self, caplog: pytest.LogCaptureFixture):
        """Test error logging."""
        logger = StdlibLogger("test.error")
        with caplog.at_level(logging.ERROR, logger="test.error"):
            logger.error("Error message: %s", "value")
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "ERROR"
        assert caplog.records[0].message == "Error message: value"

    def test_multiple_args(self, caplog: pytest.LogCaptureFixture):
        """Test logging with multiple arguments."""
        logger = StdlibLogger("test.multi")
        with caplog.at_level(logging.INFO, logger="test.multi"):
            logger.info("Message: %s, %d, %s", "string", 42, "another")
        assert len(caplog.records) == 1
        assert caplog.records[0].message == "Message: string, 42, another"

    def test_no_args(self, caplog: pytest.LogCaptureFixture):
        """Test logging without format arguments."""
        logger = StdlibLogger("test.noargs")
        with caplog.at_level(logging.INFO, logger="test.noargs"):
            logger.info("Simple message")
        assert len(caplog.records) == 1
        assert caplog.records[0].message == "Simple message"
