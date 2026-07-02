"""Tests for the LoggerPort outbound port.

These verify the LoggerPort protocol contract — not implementation-specific behavior.
"""

from typing import Protocol, runtime_checkable

import pytest

from forging_blocks.application.ports.outbound.logger_port import LoggerPort


@runtime_checkable
class _FakeLogger(Protocol):
    def debug(self, msg: str, *args: object) -> None: ...
    def info(self, msg: str, *args: object) -> None: ...
    def warning(self, msg: str, *args: object) -> None: ...
    def error(self, msg: str, *args: object) -> None: ...


class DummyLogger:
    """Fake LoggerPort implementation for structural subtyping tests."""

    def debug(self, msg: str, *args: object) -> None: ...

    def info(self, msg: str, *args: object) -> None: ...

    def warning(self, msg: str, *args: object) -> None: ...

    def error(self, msg: str, *args: object) -> None: ...


@pytest.mark.unit
class TestLoggerPort:
    """Contract tests for the LoggerPort protocol."""

    def test_logger_is_protocol(self) -> None:
        """LoggerPort should be a Protocol (structural subtyping)."""
        from typing import Protocol as _Protocol

        assert isinstance(LoggerPort, type(_Protocol))

    def test_logger_has_required_methods(self) -> None:
        """LoggerPort protocol should define debug, info, warning, error."""
        assert hasattr(LoggerPort, "debug")
        assert hasattr(LoggerPort, "info")
        assert hasattr(LoggerPort, "warning")
        assert hasattr(LoggerPort, "error")

    def test_dummy_logger_satisfies_protocol(self) -> None:
        """Any object with matching methods satisfies LoggerPort protocol."""
        dummy = DummyLogger()
        assert isinstance(dummy, _FakeLogger)

    def test_logger_methods_accept_args(self) -> None:
        """LoggerPort methods should accept message and *args."""
        dummy = DummyLogger()
        dummy.debug("test %s", "arg")
        dummy.info("test %s %d", "arg", 42)
        dummy.warning("test")
        dummy.error("test %s", "error_arg")
