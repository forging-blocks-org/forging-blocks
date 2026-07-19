"""LoggerPort port for abstract logging.

Defines the ``LoggerPort`` protocol that application code depends on,
decoupling logging from any specific logging library.
"""

from typing import Protocol

from forging_blocks.foundation.ports import OutboundPort


class LoggerPort[MessageType](OutboundPort[MessageType, None], Protocol):
    """Structural protocol for logging.
    Any object with ``debug``, ``info``, ``warning``, and ``error``
    methods that accept a message string plus optional positional
    arguments satisfies this protocol — no inheritance required.
    """

    def debug(self, msg: MessageType, *args: object) -> None:
        """Log a debug message."""
        ...

    def info(self, msg: MessageType, *args: object) -> None:
        """Log an info message."""
        ...

    def warning(self, msg: MessageType, *args: object) -> None:
        """Log a warning message."""
        ...

    def error(self, msg: MessageType, *args: object) -> None:
        """Log an error message."""
        ...
