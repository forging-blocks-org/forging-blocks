"""Module defining the DraftEntityIsNotHashableError exception."""

from typing import Self

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class DraftEntityIsNotHashableError(Error[dict[str, object]]):
    """Raised because draft entities are not hashable."""

    @classmethod
    def from_class_name(cls, class_name: str) -> Self:
        """Create DraftEntityIsNotHashableError from class name."""
        error_text = f"Unhashable {class_name}: draft entities (id=None) are not hashable"
        error_message = ErrorMessage(error_text)

        return cls(error_message)
