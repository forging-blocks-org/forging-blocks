"""Fundamental error class for the Building Blocks framework.

Defines the base Error type that all structured errors inherit from.
"""

from typing import Any

from forging_blocks.foundation.debuggable import Debuggable
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


class Error(Exception, Debuggable):
    """Base class for all structured errors that can be raised like standard Exceptions."""

    def __init__(self, message: ErrorMessage, metadata: ErrorMetadata | None = None) -> None:
        super().__init__(message.value)
        self._message = message
        self._metadata = metadata or ErrorMetadata(context={})

    def __str__(self) -> str:
        context_str = f" | Context: {self._metadata.context}" if self._metadata.context else ""
        return f"{self.__class__.__name__}: {self._message.value}{context_str}"

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} message={self._message.value!r} "
            f"context={self._metadata.context!r}>"
        )

    @property
    def message(self) -> ErrorMessage:
        """Structured error message."""
        return self._message

    @property
    def metadata(self) -> ErrorMetadata:
        """Structured metadata with additional context."""
        return self._metadata

    @property
    def context(self) -> dict[str, Any]:
        """Shortcut for accessing the metadata context."""
        return self._metadata.context

    def as_debug_string(self) -> str:
        """Return a detailed, multi-line string for debugging."""
        return (
            f"{self.__class__.__name__}(\n"
            f"  message={repr(self._message)},\n"
            f"  metadata={repr(self._metadata)}\n"
            ")"
        )
