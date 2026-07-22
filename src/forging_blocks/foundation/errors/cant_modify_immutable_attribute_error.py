"""Module for CantModifyImmutableAttributeError exception."""

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.error import Error


class CantModifyImmutableAttributeError(Error[dict[str, object]]):
    """Raised when there is an attempt to modify an immutable attribute of an object."""

    def __init__(self, class_name: str, attribute_name: str):
        """Initialise the error with the class and attribute that triggered the violation.

        Args:
            class_name: Name of the class whose immutable attribute was targeted.
            attribute_name: Name of the attribute that was being modified.

        """
        message = ErrorMessage(
            f"Cannot modify immutable attribute '{attribute_name}' of class '{class_name}'."
        )
        metadata = ErrorMetadata[dict[str, object]](
            {
                "class_name": class_name,
                "attribute_name": attribute_name,
            }
        )
        super().__init__(message, metadata)
