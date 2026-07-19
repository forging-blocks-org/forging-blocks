"""LoggerPort port for abstract logging.

Defines the ``LoggerPort`` protocol that application code depends on,
decoupling logging from any specific logging library.
"""

from typing import Protocol

from forging_blocks.foundation.ports import OutboundPort


class LoggerPort(OutboundPort[str, None], Protocol):
    """Structural protocol for logging.

    Any object with ``debug``, ``info``, ``warning``, and ``error``
    methods that accept a ``str`` message plus optional positional
    ``str`` arguments satisfies this protocol —
    no inheritance required.

    Implementations MAY accept wider types for ``*args`` (e.g.
    ``*args: object``) — the port contract only constrains callers,
    not implementors.
    """

    def debug(self, msg: str, *args: str) -> None:
        """Log a debug message."""
        ...

    def info(self, msg: str, *args: str) -> None:
        """Log an info message."""
        ...

    def warning(self, msg: str, *args: str) -> None:
        """Log a warning message."""
        ...

    def error(self, msg: str, *args: str) -> None:
        """Log an error message."""
        ...
