"""LoggerPort contract for abstract logging.

Defines the ``LoggerPort`` ABC that application code depends on,
decoupling logging from any specific logging library.
"""

from abc import abstractmethod

from forging_blocks.foundation.ports import OutboundPort


class LoggerPort(OutboundPort):
    """ABC for logging.

    Explicit inheritance is required — ``debug``, ``info``,
    ``warning``, and ``error`` are ``@abstractmethod`` stubs
    that subclasses must implement.

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
