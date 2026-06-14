"""In-memory read-only repository implementation.

Provides a concrete implementation of ReadOnlyRepository backed by a
dictionary for query-side operations in CQRS architectures.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from forging_blocks.application.ports.outbound.repository import ReadOnlyRepository


class InMemoryReadRepository[TReadAggregateRoot, TId](
    ReadOnlyRepository[TReadAggregateRoot, TId],
):
    """In-memory implementation of ReadOnlyRepository for query operations.

    Stores aggregates in a dictionary keyed by their identifier. Designed
    for query-side usage in CQRS architectures.

    The storage mapping is injected via the constructor and copied on init
    to ensure independence from external mutation.
    """

    __slots__ = ("_storage",)

    def __init__(self, storage: Mapping[TId, TReadAggregateRoot] | None = None) -> None:
        """Initialize the read repository with optional external storage.

        Args:
            storage: An optional mapping to use as backing storage.
                If None, a new empty dictionary is used.
        """
        self._storage: dict[TId, TReadAggregateRoot] = dict(storage) if storage is not None else {}

    async def get_by_id(self, id: TId) -> TReadAggregateRoot | None:  # noqa: A002
        """Retrieve an aggregate or read model by ID.

        Args:
            id: Unique identifier of the resource.

        Returns:
            The retrieved instance or None if not found.
        """
        return self._storage.get(id)

    async def list_all(self) -> Sequence[TReadAggregateRoot]:
        """Retrieve all resources in the repository.

        Returns:
            A sequence of aggregate or read model instances.
        """
        return list(self._storage.values())
