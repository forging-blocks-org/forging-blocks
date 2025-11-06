"""Module defining a protocol for debuggable objects."""

from typing import Protocol


class Debuggable(Protocol):
    """Protocol for objects that can provide detailed debug string representations."""

    def as_debug_string(self) -> str:
        """Return a detailed, multi-line string describing this object for debugging."""
        ...
