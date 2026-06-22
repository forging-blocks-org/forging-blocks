"""Standard library logging implementation of the Logger port."""

import logging

from forging_blocks.application.ports.outbound.logger import Logger


class StdlibLogger(Logger):
    """Logger implementation backed by Python's standard ``logging`` module.

    Args:
        name: Logger name (default ``"forging_blocks"``).
    """

    __slots__ = ("_logger",)

    def __init__(self, name: str = "forging_blocks") -> None:
        self._logger = logging.getLogger(name)

    def debug(self, msg: str, *args: object) -> None:
        """Log a debug message."""
        self._logger.debug(msg, *args)

    def info(self, msg: str, *args: object) -> None:
        """Log an info message."""
        self._logger.info(msg, *args)

    def warning(self, msg: str, *args: object) -> None:
        """Log a warning message."""
        self._logger.warning(msg, *args)

    def error(self, msg: str, *args: object) -> None:
        """Log an error message."""
        self._logger.error(msg, *args)
