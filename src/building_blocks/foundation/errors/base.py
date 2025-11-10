"""This module provides the foundational error classes used across the Building Blocks framework.

It defines structured, debuggable, and composable error types that can be raised,
caught, and combined in a uniform way throughout all architectural layers.

Classes
--------

Error:
    Base class for all structured errors in the system. Inherits from
    `Exception` and `Debuggable`, allowing it to be raised and logged like
    a standard exception while carrying structured metadata.

NoneNotAllowedError
    Specialized `Error` indicating that a `None` value was provided where it
    is not allowed.

FieldErrors
    Represents validation or constraint errors associated with a single field.
    Provides iterable access to individual `Error` instances for that field.

CombinedErrors
    Aggregates multiple `Error` (or subclass) instances into one. Useful for
    collecting and raising multiple failures together (e.g., validation errors).

Notes:
-----
- All errors defined here are part of the *foundation* module and can be
  safely reused by higher components present in layer, if you have layer defined.
- Each error supports a detailed `as_debug_string()` method for rich diagnostic output.
"""

from __future__ import annotations

from typing import Any, Generic, Iterable, Iterator, Sequence, TypeVar

from building_blocks.foundation.debuggable import Debuggable
from building_blocks.foundation.errors.core import (
    ErrorMessage,
    ErrorMetadata,
    FieldReference,
)

ErrorType = TypeVar("ErrorType", bound="Error")


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


class NoneNotAllowedError(Error):
    """Error indicating that a None value was provided where it is not allowed."""


class FieldErrors(Error):
    """Base class for errors associated with a specific field."""

    def __init__(self, field: FieldReference, errors: Iterable[Error]) -> None:
        self._field = field
        self._errors: Sequence[Error] = tuple(
            errors,
        )

    def __repr__(self) -> str:
        """Return a concise string representation of the field errors."""
        return (
            f"<{self._get_title_prefix()} field={self._field.value!r} "
            f"errors={len(self._errors)}>"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of the field errors."""
        error_messages = "\n".join(f" - {str(error)}" for error in self._errors)
        return f"{self._get_title_prefix()} for field '{self._field.value}':\n" f"{error_messages}"

    def __iter__(self) -> Iterator[Error]:
        """Iterate over the errors associated with the field."""
        return iter(self._errors)

    def __len__(self) -> int:
        """Return the number of errors associated with the field."""
        return len(self._errors)

    @property
    def field(self) -> FieldReference:
        """The field associated with these errors."""
        return self._field

    @property
    def errors(self) -> Sequence[Error]:
        """The collection of errors associated with the field."""
        return self._errors

    def as_debug_string(self) -> str:
        """Return detailed, multi-line string of this field error collection for debugging."""
        error_strings = [f"    {err.as_debug_string()}" for err in self._errors]
        return (
            f"{self._get_title_prefix()}(\n"
            f"  field={repr(self._field)},\n"
            f"  errors=[\n"
            + ("" if not error_strings else "\n".join(error_strings) + "\n")
            + "  ]\n"
            ")"
        )

    def _get_title_prefix(self) -> str:
        """Get the title prefix for this field error type."""
        return self.__class__.__name__


class CombinedErrors(Error, Generic[ErrorType]):
    """Base class for combining multiple errors into one."""

    def __init__(self, errors: Iterable[ErrorType]) -> None:
        self._errors: Sequence[ErrorType] = tuple(errors)
        combined_message = f"{len(self._errors)} errors occurred."
        super().__init__(message=ErrorMessage(combined_message))

    def __repr__(self) -> str:
        """Return a concise string representation of the combined errors."""
        return f"<{self._get_title_prefix()} errors={len(self._errors)}>"

    def __str__(self) -> str:
        """Return a human-readable string representation of the combined errors."""
        error_details = "\n".join(f"- {str(error)}" for error in self._errors)
        return f"{self._get_title_prefix()}:\n{error_details}"

    def __iter__(self) -> Iterator[ErrorType]:
        """Iterate over the combined errors."""
        return iter(self._errors)

    def __len__(self) -> int:
        """Return the number of combined errors."""
        return len(self._errors)

    @property
    def errors(self) -> Sequence[ErrorType]:
        """The collection of combined errors."""
        return self._errors

    def as_debug_string(self) -> str:
        """Return a detailed, multi-line string for debugging, showing all contained errors."""
        error_strings = [
            f"    {e.as_debug_string().replace(chr(10), chr(10)+'    ')}" for e in self._errors
        ]
        return (
            f"{self._get_title_prefix()}(\n"
            f"  errors=[\n"
            + ("" if not error_strings else "\n".join(error_strings) + "\n")
            + "  ]\n"
            ")"
        )

    def _get_title_prefix(self) -> str:
        """Get the title prefix for this combined error type."""
        return self.__class__.__name__
