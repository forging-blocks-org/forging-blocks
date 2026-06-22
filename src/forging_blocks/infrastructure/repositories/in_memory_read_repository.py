"""In-memory read-only repository implementation.

Provides a concrete implementation of ReadOnlyRepository backed by a
dictionary for query-side operations in CQRS architectures.
"""

from collections.abc import Mapping

from forging_blocks.infrastructure.repositories.base_repository import BaseReadRepository


class InMemoryReadRepository[TReadAggregateRoot, TId](
    BaseReadRepository[TReadAggregateRoot, TId],
):
    """In-memory implementation of ReadOnlyRepository for query operations.

    Stores aggregates in a dictionary keyed by their identifier. Designed
    for query-side usage in CQRS architectures.

    The storage mapping is injected via the constructor and copied on init
    to ensure independence from external mutation.
    """

    __slots__ = ()

    def __init__(self, storage: Mapping[TId, TReadAggregateRoot] | None = None) -> None:
        """Initialize the read repository with optional external storage.

        Args:
            storage: An optional mapping to use as backing storage.
                If None, a new empty dictionary is used.
        """
        super().__init__(storage)
