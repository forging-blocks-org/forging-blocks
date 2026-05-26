"""In-memory write-only repository implementation.

Provides a concrete implementation of WriteOnlyRepository backed by a
dictionary for command-side operations in CQRS architectures.
"""

from __future__ import annotations

from typing import Generic, MutableMapping, TypeVar

from forging_blocks.application.ports.outbound.repository import WriteOnlyRepository
from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.infrastructure.errors.repository_errors import (
    RepositoryError,
    RepositoryNotFoundError,
)

TWriteAggregateRoot = TypeVar("TWriteAggregateRoot")
TWriteId = TypeVar("TWriteId")


class InMemoryWriteRepository(
    Generic[TWriteAggregateRoot, TWriteId],
    WriteOnlyRepository[TWriteAggregateRoot, TWriteId],
):
    """In-memory implementation of WriteOnlyRepository for command operations.

    Stores aggregates in a dictionary keyed by their identifier. Designed
    for command-side usage in CQRS architectures.

    The storage mapping is injected via the constructor and copied on init
    to ensure independence from external mutation.
    """

    __slots__ = ("_storage",)

    def __init__(
        self,
        storage: MutableMapping[TWriteId, TWriteAggregateRoot] | None = None,
    ) -> None:
        """Initialize the write repository with optional external storage.

        Args:
            storage: An optional mutable mapping to use as backing storage.
                If None, a new empty dictionary is used.
        """
        self._storage: dict[TWriteId, TWriteAggregateRoot] = (
            dict(storage) if storage is not None else {}
        )

    async def delete_by_id(self, id: TWriteId) -> None:  # noqa: A002
        """Delete an aggregate by ID.

        Args:
            id: Unique identifier of the aggregate.

        Raises:
            RepositoryNotFoundError: If no aggregate exists with the given ID.
        """
        if id not in self._storage:
            raise RepositoryNotFoundError.for_id(id)
        del self._storage[id]

    async def save(self, aggregate: TWriteAggregateRoot) -> None:
        """Persist an aggregate instance.

        Args:
            aggregate: The aggregate to save.

        Raises:
            RepositoryError: If the aggregate has no ID.
        """
        aggregate_id = getattr(aggregate, "id", None)
        if aggregate_id is None:
            raise RepositoryError(ErrorMessage("Cannot save aggregate without an identifier."))
        self._storage[aggregate_id] = aggregate
