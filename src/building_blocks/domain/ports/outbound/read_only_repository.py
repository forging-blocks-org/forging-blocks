"""Read-only repository interface for CQRS query scenarios.

This module provides read-only repository contracts with full type safety,
useful for CQRS implementations where you separate command and query responsibilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

TAggregateRoot = TypeVar("TAggregateRoot")
TId = TypeVar("TId")


class AsyncReadOnlyRepository(ABC, Generic[TAggregateRoot, TId]):
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
        ...     async def find_by_id(self, id: UUID) -> Order | None:
        ...         # Query implementation - read from optimized read model
        ...         pass
        ...
        ...     async def find_all(self) -> List[Order]:
        ...         # Query implementation
        ...         pass
        ...
        ...     # Add query-specific methods
        ...     async def find_by_customer_id(self, customer_id: str) -> List[Order]:
        ...         # Optimized for queries
        ...         pass
        ...
        ...     async def get_order_statistics(self) -> Dict[str, int]:
        ...         # Complex query operations
        ...         pass
    """

    @abstractmethod
    async def find_by_id(self, id: TId) -> Optional[TAggregateRoot]:
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

    @abstractmethod
    async def find_all(self) -> List[TAggregateRoot]:
        """Find all aggregates in the repository.

        Note: In CQRS scenarios, this might be reading from optimized
        read models rather than the authoritative command store.

        Returns:
            All aggregates in the repository
        """


class SyncReadOnlyRepository(ABC, Generic[TAggregateRoot, TId]):
    """Read-only sync repository interface for CQRS query scenarios.

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
        >>> class OrderQueryRepository(SyncReadOnlyRepository[Order, UUID]):
        ...     def find_by_id(self, id: UUID) -> Order | None:
        ...         # Query implementation - read from optimized read model
        ...         pass
        ...
        ...     def find_all(self) -> List[Order]:
        ...         # Query implementation
        ...         pass
        ...
        ...     # Add query-specific methods
        ...     def find_by_customer_id(self, customer_id: str) -> List[Order]:
        ...         # Optimized for queries
        ...         pass
        ...
        ...     def get_order_statistics(self) -> dict[str, int]:
        ...         # Complex query operations
        ...         pass
    """

    @abstractmethod
    def find_by_id(self, id: TId) -> Optional[TAggregateRoot]:
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

    @abstractmethod
    def find_all(self) -> List[TAggregateRoot]:
        """Find all aggregates in the repository.

        Note: In CQRS scenarios, this might be reading from optimized
        read models rather than the authoritative command store.

        Returns:
            All aggregates in the repository
        """
