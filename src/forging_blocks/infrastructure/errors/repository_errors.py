"""RepositoryPort error classes for the infrastructure layer.

Provides structured error types for repository operations such as
save failures, deletion of non-existent aggregates, and retrieval errors.
"""

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class RepositoryError(Error[dict[str, object]]):
    """Generic error raised when a repository operation fails.

    This is the base error for all repository-level failures. Concrete
    implementations may raise this or more specific subclasses.
    """


class RepositoryNotFoundError(RepositoryError):
    """Error raised when attempting to delete or retrieve an aggregate that does not exist."""

    @classmethod
    def for_id(cls, entity_id: object) -> RepositoryNotFoundError:
        """Create an error for a specific missing aggregate ID.

        Args:
            entity_id: The identifier that was not found.

        Returns:
            A RepositoryNotFoundError with a descriptive message.
        """
        return cls(ErrorMessage(f"Aggregate with id '{entity_id}' not found."))
