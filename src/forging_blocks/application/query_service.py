"""Query service for CQRS read operations.

Provides a service for executing queries against read models
with support for projections and caching.
"""

from collections.abc import Callable, Sequence
from typing import Generic, Protocol, TypeVar

from forging_blocks.application.ports.outbound.query_fetcher import QueryFetcher
from forging_blocks.foundation.messages.query import Query

TQuery = TypeVar("TQuery", bound=Query[object])
TResult = TypeVar("TResult")
TReadModel = TypeVar("TReadModel")


class ReadModel(Protocol):
    """Protocol for read model objects.

    Read models are denormalized views optimized for querying.
    They should be immutable and serializable.
    """

    @property
    def id(self) -> str | int: ...


class QueryService(Generic[TQuery, TResult]):
    """Service for executing queries.

    Provides a high-level interface for query execution with
    support for caching, projections, and result transformation.
    """

    def __init__(self, query_fetcher: QueryFetcher[object, TResult]) -> None:
        """Initialize the query service.

        Args:
            query_fetcher: The query fetcher for executing queries.
        """
        self._query_fetcher = query_fetcher

    async def execute(self, query: TQuery) -> TResult:
        """Execute a query and return the result.

        Args:
            query: The query to execute.

        Returns:
            The query result.
        """
        return await self._query_fetcher.fetch(query)


class ReadModelRepository(Protocol[TReadModel]):
    """Protocol for read model repositories.

    Provides read-only access to read models with
    specification-based querying.
    """

    async def get_by_id(self, id: str | int) -> TReadModel | None: ...

    async def list_all(self) -> Sequence[TReadModel]: ...

    async def find_matching(self, spec: Callable[[TReadModel], bool]) -> Sequence[TReadModel]: ...

    async def count_matching(self, spec: Callable[[TReadModel], bool]) -> int: ...

    async def exists_matching(self, spec: Callable[[TReadModel], bool]) -> bool: ...


class ProjectionService(Generic[TReadModel]):
    """Service for managing read model projections.

    Handles the creation and updating of read models
    from domain events.
    """

    def __init__(self, repository: ReadModelRepository[TReadModel]) -> None:
        """Initialize the projection service.

        Args:
            repository: The read model repository.
        """
        self._repository = repository

    async def project(self, event: object) -> None:
        """Project a domain event to update read models.

        Args:
            event: The domain event to project.
        """
        # Override in subclasses to implement specific projections
        pass

    async def rebuild(self, events: Sequence[object]) -> None:
        """Rebuild read models from a sequence of events.

        Args:
            events: The sequence of domain events to replay.
        """
        for event in events:
            await self.project(event)


class CachedQueryService(Generic[TQuery, TResult]):
    """Query service with caching support.

    Wraps a query service with an in-memory cache for
    frequently accessed queries.
    """

    def __init__(
        self,
        query_service: QueryService[TQuery, TResult],
        cache: dict[str, TResult] | None = None,
        cache_key_fn: Callable[[TQuery], str] | None = None,
    ) -> None:
        """Initialize the cached query service.

        Args:
            query_service: The underlying query service.
            cache: Optional cache dictionary.
            cache_key_fn: Optional function to generate cache keys from queries.
        """
        self._query_service = query_service
        self._cache: dict[str, TResult] = cache or {}
        self._cache_key_fn = cache_key_fn or (lambda q: str(q))

    async def execute(self, query: TQuery) -> TResult:
        """Execute a query with caching.

        Args:
            query: The query to execute.

        Returns:
            The query result (from cache or fresh execution).
        """
        cache_key = self._cache_key_fn(query)

        if cache_key in self._cache:
            return self._cache[cache_key]

        result = await self._query_service.execute(query)
        self._cache[cache_key] = result
        return result

    def invalidate(self, query: TQuery) -> None:
        """Invalidate a cached query result.

        Args:
            query: The query to invalidate.
        """
        cache_key = self._cache_key_fn(query)
        self._cache.pop(cache_key, None)

    def clear_cache(self) -> None:
        """Clear all cached results."""
        self._cache.clear()
