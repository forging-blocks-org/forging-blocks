"""
Tests for the AggregateRepository implementation.
"""

import pytest

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.domain.aggregate_root.aggregate_version import AggregateVersion
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.in_memory_event_store import InMemoryEventStore
from forging_blocks.infrastructure.repositories.aggregate_repository import AggregateRepository


class TestEvent(Event[dict[str, object]]):
    """Test event for testing."""

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload


class TestAggregate(AggregateRoot[str, dict[str, object]]):
    """Test aggregate for testing."""

    def __init__(self, aggregate_id: str, version: AggregateVersion | None = None):
        super().__init__(aggregate_id, version)
        self._state = ""

    def _handle(self, event: Event[dict[str, object]]) -> None:
        self._state = event.value["value"]

    @property
    def state(self) -> str:
        return self._state


class TestAggregateRepository:
    """Tests for the AggregateRepository implementation."""

    @pytest.fixture
    def event_store(self):
        """Create an in-memory event store."""
        return InMemoryEventStore()

    @pytest.fixture
    def repo(self, event_store):
        """Create an AggregateRepository with the event store."""
        return AggregateRepository[TestAggregate, str](event_store)

    @pytest.mark.asyncio
    async def test_save_aggregate(self, repo):
        """Test saving an aggregate."""
        aggregate = TestAggregate("1")
        aggregate.apply(TestEvent("initial"))

        await repo.save(aggregate)

        # Check that aggregate is in storage
        retrieved = await repo.get_by_id("1")
        assert retrieved is not None
        assert retrieved.state == "initial"

    @pytest.mark.asyncio
    async def test_save_persists_events(self, repo, event_store):
        """Test that saving an aggregate persists its events to the event store."""
        aggregate = TestAggregate("1")
        aggregate.apply(TestEvent("event1"))
        aggregate.apply(TestEvent("event2"))

        await repo.save(aggregate)
        # Check events in event store
        events = await event_store.get_events("1")
        assert len(events) == 2
        assert events[0]["payload"]["value"] == "event1"
        assert events[1]["payload"]["value"] == "event2"

    @pytest.mark.asyncio
    async def test_save_with_expected_version(self, repo, event_store):
        """Test saving with expected version for concurrency control."""
        aggregate = TestAggregate("1")
        aggregate.apply(TestEvent("event1"))
        await repo.save(aggregate)

        # Apply another event to the same aggregate instance
        aggregate.apply(TestEvent("event2"))

        # This should work since we're using the same aggregate instance
        await repo.save(aggregate)

        # Check events in event store
        events = await event_store.get_events("1")
        assert len(events) == 2

    async def test_get_by_id_from_storage(self, repo):
        """Test getting an aggregate from in-memory storage."""
        aggregate = TestAggregate("1")
        aggregate.apply(TestEvent("initial"))
        await repo.save(aggregate)

        retrieved = await repo.get_by_id("1")
        assert retrieved is not None
        assert retrieved.state == "initial"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo):
        """Test getting a non-existent aggregate."""
        retrieved = await repo.get_by_id("999")
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_delete_aggregate(self, repo):
        """Test deleting an aggregate."""
        aggregate = TestAggregate("1")
        aggregate.apply(TestEvent("initial"))
        await repo.save(aggregate)

        await repo.delete_by_id("1")

        retrieved = await repo.get_by_id("1")
        assert retrieved is None
