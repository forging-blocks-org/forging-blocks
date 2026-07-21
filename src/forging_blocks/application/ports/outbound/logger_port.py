"""LoggerPort port for abstract logging.

Defines the ``LoggerPort`` protocol that application code depends on,
decoupling logging from any specific logging library.
"""

from abc import abstractmethod

from forging_blocks.foundation.ports import OutboundPort


class LoggerPort(OutboundPort[str, None]):
    """Structural protocol for logging.

    Any object with ``debug``, ``info``, ``warning``, and ``error``
    methods that accept a ``str`` message plus optional positional
    ``str`` arguments satisfies this protocol —
    no inheritance required.

    Implementations MAY accept wider types for ``*args`` (e.g.
    ``*args: object``) — the port contract only constrains callers,
    not implementors.
    """

    @abstractmethod
    def debug(self, msg: str, *args: str) -> None:
        """Log a debug message."""
        ...

    @abstractmethod
    def info(self, msg: str, *args: str) -> None:
        """Log an info message."""
        ...

    @abstractmethod
    def warning(self, msg: str, *args: str) -> None:
        """Log a warning message."""
        ...

    @abstractmethod
    def error(self, msg: str, *args: str) -> None:
        """Log an error message."""
        ...
