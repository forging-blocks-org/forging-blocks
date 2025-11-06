"""Module defining the EntityIdNotNoneNotAllowedError."""

from building_blocks.foundation.errors.base import NoneNotAllowedError
from building_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


class EntityIdNoneError(NoneNotAllowedError):
    """Raised when an entity ID is None but should not be."""

    def __init__(self, entity_class_name: str) -> None:
        message = ErrorMessage(f"Entity ID have to be defined for '{entity_class_name}'.")
        metadata = ErrorMetadata(
            context={
                "entity_class_name": entity_class_name,
            }
        )
        super().__init__(message=message, metadata=metadata)
