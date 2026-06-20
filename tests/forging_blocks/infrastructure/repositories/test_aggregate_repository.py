"""
Tests for the AggregateRepository implementation.
"""

from typing import Self

import pytest

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.domain.aggregate_root.aggregate_version import AggregateVersion
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.infrastructure.in_memory_event_store import InMemoryEventStore
from forging_blocks.infrastructure.repositories.aggregate_repository import AggregateRepository


class FakeEvent(Event[dict[str, object]]):
    """Fake event for testing."""

    def __init__(self, value: str, metadata: MessageMetadata | None = None):
        super().__init__(metadata)
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(value=str(data.get("value", "")), metadata=metadata)


class FakeAggregate(AggregateRoot[str, dict[str, object]]):
    """Fake aggregate for testing."""

    def __init__(self, aggregate_id: str, version: AggregateVersion | None = None):
        super().__init__(aggregate_id, version)
        self._state = ""

    def _handle(self, event: Event[dict[str, object]]) -> None:
        self._state = event.value["value"]

    @property
    def state(self) -> object:
        return self._state


class _FakeAggregateRepository(AggregateRepository[FakeAggregate, str]):
    """Concrete subclass for testing."""


class TestAggregateRepository:
    """Tests for the AggregateRepository implementation."""

    @pytest.fixture
    def event_store(self) -> InMemoryEventStore:
        """Create an in-memory event store."""
        return InMemoryEventStore()

    @pytest.fixture
    def repo(self, event_store: InMemoryEventStore) -> _FakeAggregateRepository:
        """Create an AggregateRepository with the event store."""
        return _FakeAggregateRepository(event_store)

    @pytest.mark.asyncio
    async def test_save_aggregate(self, repo: _FakeAggregateRepository) -> None:
        """Test saving an aggregate."""
        aggregate = FakeAggregate("1")
        aggregate.apply(FakeEvent("initial"))

        await repo.save(aggregate)

        # Check that aggregate is in storage
        retrieved = await repo.get_by_id("1")
        assert retrieved is not None
        assert retrieved.state == "initial"

    @pytest.mark.asyncio
    async def test_save_persists_events(
        self,
        repo: _FakeAggregateRepository,
        event_store: InMemoryEventStore,
    ) -> None:
        """Test that saving an aggregate persists its events to the event store."""
        aggregate = FakeAggregate("1")
        aggregate.apply(FakeEvent("event1"))
        aggregate.apply(FakeEvent("event2"))

        await repo.save(aggregate)
        # Check events in event store
        events: list[dict[str, object]] = await event_store.get_events("1")
        assert len(events) == 2
        payload0 = events[0]["payload"]
        assert isinstance(payload0, dict)
        assert payload0["value"] == "event1"
        payload1 = events[1]["payload"]
        assert isinstance(payload1, dict)
        assert payload1["value"] == "event2"

    @pytest.mark.asyncio
    async def test_save_with_expected_version(
        self,
        repo: _FakeAggregateRepository,
        event_store: InMemoryEventStore,
    ) -> None:
        """Test saving with expected version for concurrency control."""
        aggregate = FakeAggregate("1")
        aggregate.apply(FakeEvent("event1"))
        await repo.save(aggregate)

        # Apply another event to the same aggregate instance
        aggregate.apply(FakeEvent("event2"))

        # This should work since we're using the same aggregate instance
        await repo.save(aggregate)

        # Check events in event store
        events: list[dict[str, object]] = await event_store.get_events("1")
        assert len(events) == 2

    async def test_get_by_id_from_storage(self, repo: _FakeAggregateRepository) -> None:
        """Test getting an aggregate from in-memory storage."""
        aggregate = FakeAggregate("1")
        aggregate.apply(FakeEvent("initial"))
        await repo.save(aggregate)

        retrieved = await repo.get_by_id("1")
        assert retrieved is not None
        assert retrieved.state == "initial"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo: _FakeAggregateRepository) -> None:
        """Test getting a non-existent aggregate."""
        retrieved = await repo.get_by_id("999")
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_delete_aggregate(self, repo: _FakeAggregateRepository) -> None:
        """Test deleting an aggregate."""
        aggregate = FakeAggregate("1")
        aggregate.apply(FakeEvent("initial"))
        await repo.save(aggregate)

        await repo.delete_by_id("1")

        retrieved = await repo.get_by_id("1")
        assert retrieved is None
