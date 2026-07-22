"""Base class for errors associated with a specific field.

Defines FieldErrors which represents validation or constraint errors
associated with a single field.
"""

from typing import Iterable, Iterator, Sequence

from forging_blocks.foundation.errors.core import ErrorMessage, FieldReference
from forging_blocks.foundation.errors.error import Error


class FieldErrors[ContainedErrorType: Error[dict[str, object]]](Error[dict[str, object]]):
    """Base class for errors associated with a specific field."""

    def __init__(self, field: FieldReference, errors: Iterable[ContainedErrorType]) -> None:
        """Initialise with a field reference and the errors associated with it.

        Args:
            field: Reference to the field these errors belong to.
            errors: The errors associated with *field*. Must be non-empty.

        Raises:
            ValueError: If *errors* is empty or *field* is falsy.

        """
        self._field = field
        self._errors: Sequence[ContainedErrorType] = tuple(errors)

        if not errors or not field:
            raise ValueError("FieldErrors must contain at least one error and field defined.")

        message = ErrorMessage(f"{len(self._errors)} error(s) for field '{field}'.")

        super().__init__(message=message)

    def __repr__(self) -> str:
        """Return a concise string representation of the field errors."""
        return (
            f"<{self._get_title_prefix()} field={self._field.value!r} errors={len(self._errors)}>"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of the field errors."""
        error_messages = "\n".join(f" - {str(error)}" for error in self._errors)
        return f"{self._get_title_prefix()} for field '{self._field.value}':\n{error_messages}"

    def __iter__(self) -> Iterator[ContainedErrorType]:
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
    def errors(self) -> Sequence[ContainedErrorType]:
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
