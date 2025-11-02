"""Generic repository interfaces for Domain-Driven Design.

This module provides a generic repository interface that is parameterized
by the aggregate root type and its ID type, providing both flexibility
and type safety.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

TAggregateRoot = TypeVar("TAggregateRoot")
TId = TypeVar("TId")


class SyncRepository(ABC, Generic[TAggregateRoot, TId]):
    """Generic sync repository interface for aggregate roots.

    This interface is parameterized by both the aggregate root type and its ID type,
    providing type safety while maintaining flexibility and reusability.

    Each concrete repository implementation will specify exactly which aggregate
    and ID type it handles, making the contract explicit and type-safe.

    Example:
        >>> from uuid import UUID
        >>> from building_blocks.domain.aggregate_root import AggregateRoot
        >>>
        >>> class Order(AggregateRoot[UUID]):
        ...     def __init__(self, id: UUID, customer_id: UUID):
        ...         super().__init__(id)
        ...         self._customer_id = customer_id
        >>>
        >>> class OrderRepository(SyncRepository[Order, UUID]):
        ...     def find_by_id(self, id: UUID) -> Optional[Order]:
        ...         # Implementation returns Order or None
        ...         pass
        ...
        ...     def save(self, order: Order) -> None:
        ...         # Implementation accepts Order specifically
        ...         pass
        ...
        ...     def delete_by_id(self, id: UUID) -> None:
        ...         # Implementation accepts Order specifically
        ...         pass
        ...
        ...     def find_all(self) -> List[Order]:
        ...         # Implementation returns List of Orders
        ...         pass
        ...
        ...     # Add aggregate-specific methods with full type safety
        ...     def find_by_customer_id(self, id: UUID) -> List[Order]:
        ...         # Aggregate-specific query - still type safe!
        ...         pass
    """

    @abstractmethod
    def find_by_id(self, id: TId) -> Optional[TAggregateRoot]:
        """Find an aggregate by its unique identifier.

        Returns None if the aggregate is not found, rather than raising
        an exception. This follows the "Tell, Don't Ask" principle and
        allows the domain to handle missing aggregates appropriately.

        Args:
            id: The unique identifier of the aggregate

        Returns:
            The aggregate if found, None otherwise
        """

    @abstractmethod
    def save(self, aggregate: TAggregateRoot) -> None:
        """Save an aggregate to the repository.

        This method handles both create and update operations.
        The repository implementation should:
        - Persist the aggregate state
        - Handle optimistic concurrency control (using version)
        - Publish domain events after successful persistence

        Args:
            aggregate: The aggregate to save

        Raises:
            ConcurrencyException: If optimistic locking fails
            RepositoryException: If persistence fails
        """

    @abstractmethod
    def delete_by_id(self, id: TId) -> None:
        """Attempts to delete an aggregate using its id.

        Args:
            id: (TId) The primary key of the aggregate to delete.
        """

    @abstractmethod
    def find_all(self) -> List[TAggregateRoot]:
        """Find all aggregates in the repository.

        Note: Use with caution in production systems with large datasets.
        Consider pagination or specific query methods instead.

        Returns:
            All aggregates in the repository
        """


class AsyncRepository(ABC, Generic[TAggregateRoot, TId]):
    """Generic async repository interface for aggregate roots.

    This interface is parameterized by both the aggregate root type and its ID type,
    providing type safety while maintaining flexibility and reusability.

    Each concrete repository implementation will specify exactly which aggregate
    and ID type it handles, making the contract explicit and type-safe.

    Example:
        >>> from uuid import UUID
        >>> from building_blocks.domain.aggregate_root import AggregateRoot
        >>>
        >>> class Order(AggregateRoot[UUID]):
        ...     def __init__(self, order_id_: UUID, customer_id: UUID):
        ...         super().__init__(order_id)
        ...         self._customer_id = customer_id
        >>>
        >>> class OrderRepository(AsyncRepository[Order, UUID]):
        ...     def find_by_id(self, id: UUID) -> Optional[Order]:
        ...         # Implementation returns Order or None
        ...         pass
        ...
        ...     async def save(self, order: Order) -> None:
        ...         # Implementation accepts Order specifically
        ...         pass
        ...
        ...     async def delete_by_id(self, id: UUID) -> None:
        ...         # Implementation accepts Order id
        ...         pass
        ...
        ...     async def find_all(self) -> List[Order]:
        ...         # Implementation returns List of Orders
        ...         pass
        ...
        ...     # Add aggregate-specific methods with full type safety
        ...     async def find_by_customer_id(self, customer_id_: UUID) -> List[Order]:
        ...         # Aggregate-specific query - still type safe!
        ...         pass
    """

    @abstractmethod
    async def find_by_id(self, id: TId) -> Optional[TAggregateRoot]:
        """Find an aggregate by its unique identifier.

        Returns None if the aggregate is not found, rather than raising
        an exception. This follows the "Tell, Don't Ask" principle and
        allows the domain to handle missing aggregates appropriately.

        Args:
            id: The unique identifier of the aggregate

        Returns:
            The aggregate if found, None otherwise
        """

    @abstractmethod
    async def save(self, aggregate: TAggregateRoot) -> None:
        """Save an aggregate to the repository.

        This method handles both create and update operations.
        The repository implementation should:
        - Persist the aggregate state
        - Handle optimistic concurrency control (using version)
        - Publish domain events after successful persistence

        Args:
            aggregate: The aggregate to save

        Raises:
            ConcurrencyException: If optimistic locking fails
            RepositoryException: If persistence fails
        """

    @abstractmethod
    async def delete_by_id(self, id: TId) -> None:
        """Attempts to delete an aggregate using its id.

        Args:
            id: (TId) The primary key of the aggregate to delete.
        """

    @abstractmethod
    async def find_all(self) -> List[TAggregateRoot]:
        """Find all aggregates in the repository.

        Note: Use with caution in production systems with large datasets.
        Consider pagination or specific query methods instead.

        Returns:
            All aggregates in the repository
        """
