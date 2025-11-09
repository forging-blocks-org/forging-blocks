"""Generic repository interfaces for Domain-Driven Design.

This module provides a generic repository interface that is parameterized
by the aggregate root type and its ID type, providing both flexibility
and type safety.
"""

from __future__ import annotations

from typing import Generic, Protocol, Sequence, TypeVar

# For read/write repos (used in both input/output): invariant
TAggregateRoot = TypeVar("TAggregateRoot")
TId = TypeVar("TId", contravariant=True)

# For read-only repos (only output): covariant
TReadResult = TypeVar("TReadResult", covariant=True)
TReadAggregateRoot = TypeVar("TReadAggregateRoot", covariant=True)
TReadId = TypeVar("TReadId", contravariant=True)

# For write-only repos (only output): covariant
TWriteAggregateRoot = TypeVar("TWriteAggregateRoot", contravariant=True)
TWriteId = TypeVar("TWriteId", contravariant=True)


class ReadOnlyRepository(Generic[TReadAggregateRoot, TId], Protocol):
    """Read-only async repository interface for CQRS query scenarios.

    This interface is parameterized by both the aggregate root type and its ID type,
    providing type safety for query-side operations in CQRS architectures.

    Perfect for:
    - CQRS query handlers that only need to read data
    - Read models that are optimized for queries
    - Enforcing read-only access in query contexts
    - Separate query databases or read replicas

    Example:
        >>> from uuid import UUID
        >>> from building_blocks.domain.aggregate_root import AggregateRoot
        >>>
        >>> class Order(AggregateRoot[UUID]):
        ...     def __init__(self, id: UUID, customer_id: str, total: float):
        ...         super().__init__(id)
        ...         self._customer_id = customer_id
        ...         self._total = total
        ...
        ...     @property
        ...     def customer_id(self) -> str:
        ...         return self._customer_id
        ...
        ...     @property
        ...     def total(self) -> float:
        ...         return self._total
        >>>
        >>> class OrderQueryRepository(AsyncReadOnlyRepository[Order, UUID]):
        ...     async def get_by_id(self, id: UUID) -> Order | None:
        ...         # Query implementation - read from optimized read model
        ...         pass
        ...
        ...     async def find_all(self) -> Sequence[Order]:
        ...         # Query implementation
        ...         pass
        ...
        ...     # Add query-specific methods
        ...     async def find_by_customer_id(
        ...         self, customer_id: str
        ...     ) -> Sequence[Order]:
        ...         # Optimized for queries
        ...         pass
        ...
        ...     async def get_order_statistics(self) -> dict[str, int]:
        ...         # Complex query operations
        ...         pass
    """

    async def get_by_id(self, id: TId) -> TReadAggregateRoot | None:
        """Find an aggregate by its unique identifier.

        This is optimized for query performance and may read from:
        - Read replicas
        - Denormalized read models
        - Cached projections
        - Optimized query databases

        Args:
            id: The unique identifier of the aggregate

        Returns:
            The aggregate if found, None otherwise
        """
        ...

    async def list_all(self) -> Sequence[TReadAggregateRoot]:
        """Find all aggregates in the repository.

        Note: In CQRS scenarios, this might be reading from optimized
        read models rather than the authoritative command store.

        Returns:
            All aggregates in the repository
        """
        ...


class WriteOnlyRepository(Protocol, Generic[TWriteAggregateRoot, TWriteId]):
    """Write-only async repository interface for CQRS command scenarios.

    This interface is parameterized by the aggregate root type, providing
    type safety for command-side operations in CQRS architectures.

    Note: Write-only repositories typically don't need the ID type parameter
    since they work with aggregate instances that already contain their IDs.

    Perfect for:
    - CQRS command handlers that only need to persist changes
    - Event sourcing scenarios where writes go to event stores
    - Command-side databases optimized for writes
    - Enforcing write-only access in command contexts

    Example:
        >>> from uuid import UUID
        >>> from building_blocks.domain.aggregate_root import AggregateRoot
        >>>
        >>> class Order(AggregateRoot[UUID]):
        ...     def __init__(self, id: UUID, customer_id: str):
        ...         super().__init__(id)
        ...         self._customer_id = customer_id
        ...         self._status = "pending"
        ...
        ...     def confirm(self) -> None:
        ...         self._status = "confirmed"
        ...         # Record domain event
        ...         self.record_event(OrderConfirmedEvent(self.id))
        >>>
        >>> class OrderWriteRepository(WriteOnlyRepository[Order, UUID]):
        ...     def save(self, order: Order) -> None:
        ...         # Save an Order aggregate
        ...         pass
        ...
        ...     def delete_by_id(self, id: UUID) -> None:
        ...         # Delete an Order aggregate by ID
        ...         pass
    """

    async def delete_by_id(self, id: TWriteId) -> None:
        """Delete an aggregate using its id.

        Args:
            id: The ID of the aggregate to delete.

        Raises:
            RepositoryException: If deletion fails
        """
        ...

    async def save(self, aggregate: TWriteAggregateRoot) -> None:
        """Save an aggregate."""
        ...


class Repository(
    ReadOnlyRepository[TAggregateRoot, TId],
    WriteOnlyRepository[TAggregateRoot, TId],
    Protocol,
):
    """Full CRUD async repository interface.

    This interface combines both read and write operations, providing and end-to-end repository
    contract.

    Perfect for:
    - Standard CRUD operations in non-CQRS scenarios
    - Simple applications without strict read/write separation
    - Prototyping and rapid development
    - When both read and write capabilities are needed.
    """

    ...
