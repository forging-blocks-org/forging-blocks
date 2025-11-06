"""Module defining the DraftEntityIsNotHashableError exception."""

from __future__ import annotations

from building_blocks.foundation.errors.base import Error
from building_blocks.foundation.errors.core import ErrorMessage


class DraftEntityIsNotHashableError(Error):
    """Raised because draft entities are not hashable."""

    @classmethod
    def from_class_name(cls, class_name: str) -> DraftEntityIsNotHashableError:
        """Create DraftEntityIsNotHashableError from class name."""
        error_text = f"{class_name} is not hashable."
        error_text = f"Unhashable {class_name}: draft entities (id=None) are not hashable"
        error_message = ErrorMessage(error_text)

        return cls(error_message)
