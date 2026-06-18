"""
Tests for the QueryService and related components.
"""

import pytest

from forging_blocks.application.ports.outbound.query_fetcher import QueryFetcher
from forging_blocks.application.query_service import (
    CachedQueryService,
    ProjectionService,
    QueryService,
    ReadModel,
    ReadModelRepository,
)
from forging_blocks.foundation.messages.query import Query


class TestQuery(Query[dict[str, object]]):
    """Test query for testing."""

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload


class TestReadModel:
    """Test read model for testing."""

    def __init__(self, id: str, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class TestQueryFetcher(QueryFetcher[dict[str, object], str]):
    """Test query fetcher for testing."""

    def __init__(self, result: str = "test result"):
        self._result = result
        self._fetch_count = 0

    async def fetch(self, query: TestQuery) -> str:
        self._fetch_count += 1
        return self._result

    @property
    def fetch_count(self) -> int:
        return self._fetch_count


class TestQueryService:
    """Tests for QueryService."""

    @pytest.fixture
    def query_fetcher(self):
        """Create a test query fetcher."""
        return TestQueryFetcher("test result")

    @pytest.fixture
    def query_service(self, query_fetcher):
        """Create a test query service."""
        return QueryService[TestQuery, str](query_fetcher)

    @pytest.mark.asyncio
    async def test_execute_query(self, query_service, query_fetcher):
        """Test executing a query."""
        query = TestQuery("test")
        result = await query_service.execute(query)

        assert result == "test result"
        assert query_fetcher.fetch_count == 1

    @pytest.mark.asyncio
    async def test_multiple_queries(self, query_service, query_fetcher):
        """Test executing multiple queries."""
        await query_service.execute(TestQuery("1"))
        await query_service.execute(TestQuery("2"))
        await query_service.execute(TestQuery("3"))

        assert query_fetcher.fetch_count == 3


class TestCachedQueryService:
    """Tests for CachedQueryService."""

    @pytest.fixture
    def query_fetcher(self):
        """Create a test query fetcher."""
        return TestQueryFetcher("test result")

    @pytest.fixture
    def query_service(self, query_fetcher):
        """Create a test query service."""
        return QueryService[TestQuery, str](query_fetcher)

    @pytest.fixture
    def cached_service(self, query_service):
        """Create a cached query service."""
        return CachedQueryService[TestQuery, str](query_service)

    @pytest.mark.asyncio
    async def test_cache_miss(self, cached_service, query_fetcher):
        """Test cache miss executes query."""
        query = TestQuery("test")
        result = await cached_service.execute(query)

        assert result == "test result"
        assert query_fetcher.fetch_count == 1

    @pytest.mark.asyncio
    async def test_cache_hit(self, cached_service, query_fetcher):
        """Test cache hit returns cached result."""
        query = TestQuery("test")

        # First execution - cache miss
        await cached_service.execute(query)
        assert query_fetcher.fetch_count == 1

        # Second execution - cache hit
        result = await cached_service.execute(query)
        assert result == "test result"
        assert query_fetcher.fetch_count == 1  # No additional fetch

    @pytest.mark.asyncio
    async def test_different_queries_not_cached(self, cached_service, query_fetcher):
        """Test different queries are not cached together."""
        await cached_service.execute(TestQuery("1"))
        await cached_service.execute(TestQuery("2"))

        assert query_fetcher.fetch_count == 2

    @pytest.mark.asyncio
    async def test_invalidate(self, cached_service, query_fetcher):
        """Test invalidating a cached query."""
        query = TestQuery("test")

        # First execution
        await cached_service.execute(query)
        assert query_fetcher.fetch_count == 1

        # Invalidate
        cached_service.invalidate(query)

        # Second execution after invalidation
        await cached_service.execute(query)
        assert query_fetcher.fetch_count == 2

    @pytest.mark.asyncio
    async def test_clear_cache(self, cached_service, query_fetcher):
        """Test clearing the entire cache."""
        await cached_service.execute(TestQuery("1"))
        await cached_service.execute(TestQuery("2"))
        assert query_fetcher.fetch_count == 2

        cached_service.clear_cache()

        await cached_service.execute(TestQuery("1"))
        await cached_service.execute(TestQuery("2"))
        assert query_fetcher.fetch_count == 4

    @pytest.mark.asyncio
    async def test_custom_cache_key(self, query_service, query_fetcher):
        """Test custom cache key function."""
        cached_service = CachedQueryService[TestQuery, str](
            query_service, cache_key_fn=lambda q: f"custom:{q._value}"
        )

        await cached_service.execute(TestQuery("test"))
        assert query_fetcher.fetch_count == 1

        await cached_service.execute(TestQuery("test"))
        assert query_fetcher.fetch_count == 1


class TestProjectionService:
    """Tests for ProjectionService."""

    @pytest.fixture
    def repository(self):
        """Create a test read model repository."""

        class TestRepository:
            def __init__(self):
                self._models = {}

            async def get_by_id(self, id):
                return self._models.get(id)

            async def list_all(self):
                return list(self._models.values())

            async def find_matching(self, spec):
                return [m for m in self._models.values() if spec(m)]

            async def count_matching(self, spec):
                return sum(1 for m in self._models.values() if spec(m))

            async def exists_matching(self, spec):
                return any(spec(m) for m in self._models.values())

        return TestRepository()

    @pytest.fixture
    def projection_service(self, repository):
        """Create a test projection service."""
        return ProjectionService[TestReadModel](repository)

    @pytest.mark.asyncio
    async def test_project(self, projection_service):
        """Test projecting an event."""
        # Base implementation does nothing
        await projection_service.project("test event")

    @pytest.mark.asyncio
    async def test_rebuild(self, projection_service):
        """Test rebuilding from events."""
        events = ["event1", "event2", "event3"]
        await projection_service.rebuild(events)


class TestReadModelProtocol:
    """Tests for ReadModel protocol."""

    def test_read_model_has_id(self):
        """Test that read model has id property."""
        model = TestReadModel("1", "Test")
        assert model.id == "1"

    def test_read_model_is_protocol(self):
        """Test that ReadModel is a protocol."""
        assert hasattr(ReadModel, "__protocol_attrs__")


class TestReadModelRepositoryProtocol:
    """Tests for ReadModelRepository protocol."""

    def test_repository_protocol(self):
        """Test that ReadModelRepository is a protocol."""
        assert hasattr(ReadModelRepository, "__protocol_attrs__")
