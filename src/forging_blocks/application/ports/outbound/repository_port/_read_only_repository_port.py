"""Read-only repository abstraction for query-side operations."""

from abc import abstractmethod
from collections.abc import Sequence

from forging_blocks.foundation.ports import OutboundPort


class ReadOnlyRepositoryPort[TReadAggregateRoot, TId](OutboundPort):
    """Read-only repository abstraction for query operations.

    This interface is optimized for query-side usage in CQRS architectures.
    It provides type-safe retrieval of aggregates or read models.
    """

    @abstractmethod
    async def get_by_id(self, id: TId) -> TReadAggregateRoot | None:
        """Retrieve an aggregate or read model by ID.

        Args:
            id: Unique identifier of the resource.

        Returns:
            The retrieved instance or None if not found.

        Notes:
            Implementations may read from:
                - read replicas,
                - projections,
                - cached read models.

        """
        ...

    @abstractmethod
    async def list_all(self) -> Sequence[TReadAggregateRoot]:
        """Retrieve all resources.

        Returns:
            A sequence of all stored instances.

        """
        ...
