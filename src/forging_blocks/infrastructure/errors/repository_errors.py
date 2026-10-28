"""Error classes for repository-level storage operations.

Provides structured error types for save failures, deletion of
non-existent aggregates, and retrieval errors.
"""

from typing import cast

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage


class RepositoryError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Generic error raised when a repository operation fails.

    This is the base error for all repository-level failures. Concrete
    implementations may raise this or more specific subclasses.

    Example:
        ```python
        class ErrorMessage:
            def __init__(self, value: str) -> None:
                self.value = value


        error = RepositoryError(ErrorMessage("Save failed"))
        ```
    """


class RepositoryNotFoundError[MetadataValueType = object](RepositoryError[MetadataValueType]):
    """Error raised when attempting to delete or retrieve an aggregate that does not exist.

    Example:
        ```python
        try:
            raise RepositoryNotFoundError.for_id("user-42")
        except RepositoryNotFoundError as exc:
            print(exc.message)
        ```

    """

    @classmethod
    def for_id(cls, entity_id: object) -> "RepositoryNotFoundError[MetadataValueType]":
        """Create an error for a specific missing aggregate ID.

        Args:
            entity_id: The identifier that was not found.

        Returns:
            A RepositoryNotFoundError with a descriptive message.

        """
        return cast(
            RepositoryNotFoundError[MetadataValueType],
            cls(ErrorMessage(f"Aggregate with id '{entity_id}' not found.")),
        )
