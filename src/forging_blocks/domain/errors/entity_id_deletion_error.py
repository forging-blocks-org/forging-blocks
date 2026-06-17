"""Module defining the EntityIdDeletionError exception."""

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.error import Error


class EntityIdDeletionError(Error):
    """Raised when there is an attempt to delete an entity's identifier."""

    def __init__(self, class_name: str) -> None:
        """Initialise the error with the class name.

        Args:
            class_name: Name of the class whose identifier was targeted for deletion.
        """
        message = ErrorMessage(
            f"Cannot delete 'id' of {class_name} as it defines the entity's identity."
        )
        metadata = ErrorMetadata(
            {
                "class_name": class_name,
                "attribute_name": "id",
            }
        )
        super().__init__(message, metadata)
