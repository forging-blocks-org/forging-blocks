"""Module for CantModifyImmutableAttributeError exception."""

from __future__ import annotations

from building_blocks.foundation.errors.base import Error
from building_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


class CantModifyImmutableAttributeError(Error):
    """Raised when there is an attempt to modify an immutable attribute of an object."""

    def __init__(self, class_name: str, attribute_name: str):
        message = ErrorMessage(
            f"Cannot modify immutable attribute '{attribute_name}' of class '{class_name}'."
        )
        metadata = ErrorMetadata(
            {
                "class_name": class_name,
                "attribute_name": attribute_name,
            }
        )
        super().__init__(message, metadata)
