"""Write-only repository interface for CQRS command scenarios.

This module provides write-only repository contracts with full type safety,
useful for CQRS implementations where you separate command and query responsibilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

AggregateRootType = TypeVar("AggregateRootType")
IdType = TypeVar("IdType")


class AsyncWriteOnlyRepository(ABC, Generic[AggregateRootType, IdType]):
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

    @abstractmethod
    async def save(self, aggregate: AggregateRootType) -> None:
        """Save an aggregate."""

    @abstractmethod
    async def delete_by_id(self, id: IdType) -> None:
        """Delete an aggregate using its id.

        Args:
            id: The ID of the aggregate to delete.

        Raises:
            RepositoryException: If deletion fails
        """


class SyncWriteOnlyRepository(ABC, Generic[AggregateRootType, IdType]):
    """Write-only repository interface for CQRS command scenarios.

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
        ...     def __init__(self, order_id: UUID, customer_id: str):
        ...         super().__init__(order_id)
        ...         self._customer_id = customer_id
        ...         self._status = "pending"
        ...
        ...     def confirm(self) -> None:
        ...         self._status = "confirmed"
        ...         # Record domain event
        ...         self.record_event(OrderConfirmedEvent(self.id))
        >>>
        >>> class OrderCommandRepository(WriteOnlyRepository[Order, UUID]):
        ...     def save(self, order: Order) -> None:
        ...         # Command implementation - save to event store
        ...         # Publish domain events
        ...         pass
        ...
        ...     def delete_by_id(self, id: UUID) -> None:
        ...         # Command implementation - mark as deleted
        ...         pass
    """

    @abstractmethod
    def save(self, aggregate: AggregateRootType) -> None:
        """Save an aggregate to the command store.

        In CQRS scenarios, this typically involves:
        - Persisting to the authoritative command database
        - Storing events in an event store
        - Publishing domain events for read model updates
        - Handling optimistic concurrency control

        Args:
            aggregate: The aggregate to save

        Raises:
            ConcurrencyException: If optimistic locking fails
            RepositoryException: If persistence fails
        """

    @abstractmethod
    def delete_by_id(self, id: IdType) -> None:
        """Delete an aggregate from the command store.

        In CQRS scenarios, this might involve:
        - Soft deletion with domain events
        - Hard deletion from command store
        - Publishing deletion events for read model cleanup

        Args:
            id: The identifier of the aggregate to delete.

        Raises:
            RepositoryException: If deletion fails
        """
