"""Generic repository interfaces for Domain-Driven Design.

This module defines repository interfaces used to persist and retrieve
aggregate roots. Repositories abstract infrastructure concerns and offer
type-safe contracts for both command-side and query-side data access in
CQRS or traditional architectures.

Responsibilities:
    - Persist and retrieve aggregates.
    - Abstract away storage mechanisms.

Non-Responsibilities:
    - Implement business invariants (aggregate enforces them).
    - Expose ORM models or database APIs directly.
"""

from __future__ import annotations

from typing import Generic, Protocol, Sequence, TypeVar

TAggregateRoot = TypeVar("TAggregateRoot")
TId = TypeVar("TId", contravariant=True)

TReadResult = TypeVar("TReadResult", covariant=True)
TReadAggregateRoot = TypeVar("TReadAggregateRoot", covariant=True)
TReadId = TypeVar("TReadId", contravariant=True)

TWriteAggregateRoot = TypeVar("TWriteAggregateRoot", contravariant=True)
TWriteId = TypeVar("TWriteId", contravariant=True)


class ReadOnlyRepository(Generic[TReadAggregateRoot, TId], Protocol):
    """Read-only repository abstraction for query operations.

    This interface is optimized for query-side usage in CQRS architectures.
    It provides type-safe retrieval of aggregates or read models.
    """

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

    async def list_all(self) -> Sequence[TReadAggregateRoot]:
        """Retrieve all resources.

        Returns:
            A sequence of aggregate or read model instances.

        Notes:
            Data sources may differ from command-side storage.
        """
        ...


class WriteOnlyRepository(Protocol, Generic[TWriteAggregateRoot, TWriteId]):
    """Write-only repository abstraction for command operations.

    This interface supports command-side operations where writes are applied
    independently from read-side storage.
    """

    async def delete_by_id(self, id: TWriteId) -> None:
        """Delete an aggregate by ID.

        Args:
            id: Unique identifier of the aggregate.

        Raises:
            RepositoryError: If deletion fails.
        """
        ...

    async def save(self, aggregate: TWriteAggregateRoot) -> None:
        """Persist an aggregate instance.

        Args:
            aggregate: The aggregate to save.
        """
        ...


class Repository(
    ReadOnlyRepository[TAggregateRoot, TId],
    WriteOnlyRepository[TAggregateRoot, TId],
    Protocol,
):
    """Full CRUD repository abstraction.

    Combines read and write capabilities into a single repository interface.
    Suitable for non-CQRS applications or simplified contexts.
    """

    ...
