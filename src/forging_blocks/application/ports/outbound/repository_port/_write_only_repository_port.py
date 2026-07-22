"""Write-only repository abstraction for command-side operations."""

from abc import abstractmethod

from forging_blocks.foundation.ports import OutboundPort


class WriteOnlyRepositoryPort[TWriteAggregateRoot, TWriteId](OutboundPort):
    """Write-only repository abstraction for command operations.

    This interface supports command-side operations where writes are applied
    independently from read-side storage.
    """

    @abstractmethod
    async def delete_by_id(self, id: TWriteId) -> None:
        """Delete an aggregate by ID.

        Args:
            id: Unique identifier of the aggregate.

        Raises:
            RepositoryError: If deletion fails.

        """
        ...

    @abstractmethod
    async def save(self, aggregate: TWriteAggregateRoot) -> None:
        """Persist an aggregate instance.

        Args:
            aggregate: The aggregate to save.

        """
        ...
