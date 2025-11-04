"""This module defines base classes for error handling in the system.

Defines the Error, FieldErrors, and CombinedErrors classes for structured error management.
"""

from typing import Any, Generic, Iterable, Iterator, Sequence, TypeVar

from building_blocks.foundation.debuggable import Debuggable
from building_blocks.foundation.errors.core import (
    ErrorMessage,
    ErrorMetadata,
    FieldReference,
)

ErrorType = TypeVar("ErrorType", bound=Debuggable)


class Error(Exception):
    """Base class for all errors in the system, with message and metadata."""

    def __init__(self, message: ErrorMessage, metadata: ErrorMetadata | None = None) -> None:
        self._message = message
        self._metadata = metadata or ErrorMetadata(context={})
        super().__init__(message.value)

    def __repr__(self) -> str:
        """Return a concise string representation of the error."""
        return (
            f"<{self._get_title_prefix()} message={self._message.value!r} "
            f"context={self._metadata.context!r}>"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of the error."""
        return f"{self._get_title_prefix()}: {self._message.value}" f"{self._format_context()}"

    @property
    def message(self) -> ErrorMessage:
        """The error message associated with this error."""
        return self._message

    @property
    def context(self) -> dict[str, Any]:
        """The context associated with this error."""
        return self._metadata.context

    @property
    def metadata(self) -> ErrorMetadata:
        """The metadata associated with this error."""
        return self._metadata

    def as_debug_string(self) -> str:
        """Return a detailed, multi-line string describing this error for debugging."""
        return (
            f"{self._get_title_prefix()}(\n"
            f"  message={repr(self._message)},\n"
            f"  metadata={repr(self._metadata)}\n"
            ")"
        )

    def _format_context(self) -> str:
        """Format the context for string representation."""
        if self.metadata.context:
            return f" | Context: {self._metadata.context}"
        return ""

    def _get_title_prefix(self) -> str:
        """Get the title prefix for this error type."""
        return self.__class__.__name__


class FieldErrors:
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

    def __iter__(self) -> Iterator[Error]:
        """Iterate over the errors associated with the field."""
        return iter(self._errors)

    def __len__(self) -> int:
        """Return the number of errors associated with the field."""
        return len(self._errors)

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

    def __iter__(self) -> Iterator[ErrorType]:
        """Iterate over the combined errors."""
        return iter(self._errors)

    def __len__(self) -> int:
        """Return the number of combined errors."""
        return len(self._errors)

    def _get_title_prefix(self) -> str:
        """Get the title prefix for this combined error type."""
        return self.__class__.__name__
