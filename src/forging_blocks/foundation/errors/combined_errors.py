"""Base class for combining multiple errors into one.

Defines CombinedErrors which aggregates multiple Error instances into one.
"""

from typing import Iterable, Iterator, Sequence

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class CombinedErrors[ErrorType: Error[dict[str, object]]](Error[dict[str, object]]):
    """Base class for combining multiple errors into one."""

    def __init__(self, errors: Iterable[ErrorType]) -> None:
        """Initialise with an iterable of errors to combine.

        Args:
            errors: The errors to aggregate. Stored internally as a
                tuple to preserve the original collection.

        """
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
            f"    {e.as_debug_string().replace(chr(10), chr(10) + '    ')}" for e in self._errors
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
