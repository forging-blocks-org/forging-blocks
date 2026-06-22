"""
Tests for the EventStore port and InMemoryEventStore implementation.
"""

import pytest

from forging_blocks.infrastructure.event_store import ConcurrencyError, EventStore
from forging_blocks.infrastructure.in_memory_event_store import InMemoryEventStore


class TestEventStore:
    """Tests for the EventStore port interface."""

    def test_event_store_is_abstract(self):
        """EventStore should be an abstract base class."""
        assert hasattr(EventStore, "__abstractmethods__")
        assert "save_events" in EventStore.__abstractmethods__
        assert "get_events" in EventStore.__abstractmethods__
        assert "get_snapshot" in EventStore.__abstractmethods__
        assert "save_snapshot" in EventStore.__abstractmethods__


class TestInMemoryEventStore:
    """Tests for the InMemoryEventStore implementation."""

    @pytest.fixture
    def event_store(self) -> InMemoryEventStore:
        """Create a fresh InMemoryEventStore for each test."""
        return InMemoryEventStore()

    @pytest.mark.asyncio
    async def test_save_and_get_events(self, event_store: InMemoryEventStore) -> None:
        """Test saving and retrieving events."""
        aggregate_id = "test-aggregate-1"
        events: list[dict[str, object]] = [
            {"type": "Event1", "data": {"value": 1}},
            {"type": "Event2", "data": {"value": 2}},
        ]

        await event_store.save_events(aggregate_id, events)

        retrieved: list[dict[str, object]] = await event_store.get_events(aggregate_id)
        assert len(retrieved) == 2
        assert retrieved[0]["type"] == "Event1"
        assert retrieved[1]["type"] == "Event2"
        assert retrieved[0]["version"] == 1
        assert retrieved[1]["version"] == 2

    @pytest.mark.asyncio
    async def test_concurrency_error(self, event_store: InMemoryEventStore) -> None:
        """Test that concurrency error is raised when expected version doesn't match."""
        aggregate_id = "test-aggregate-2"
        events: list[dict[str, object]] = [{"type": "Event1", "data": {"value": 1}}]

        await event_store.save_events(aggregate_id, events)

        # Try to save with wrong expected version
        with pytest.raises(ConcurrencyError):
            await event_store.save_events(
                aggregate_id, [{"type": "Event2", "data": {"value": 2}}], expected_version=0
            )

    @pytest.mark.asyncio
    async def test_concurrency_success(self, event_store: InMemoryEventStore) -> None:
        """Test that save succeeds when expected version matches."""
        aggregate_id = "test-aggregate-3"
        events: list[dict[str, object]] = [{"type": "Event1", "data": {"value": 1}}]

        await event_store.save_events(aggregate_id, events)

        # Save with correct expected version
        await event_store.save_events(
            aggregate_id, [{"type": "Event2", "data": {"value": 2}}], expected_version=1
        )

        retrieved: list[dict[str, object]] = await event_store.get_events(aggregate_id)
        assert len(retrieved) == 2

    @pytest.mark.asyncio
    async def test_get_events_with_version_range(self, event_store: InMemoryEventStore) -> None:
        """Test retrieving events with version range filters."""
        aggregate_id = "test-aggregate-4"
        events: list[dict[str, object]] = [
            {"type": "Event1", "data": {"value": 1}},
            {"type": "Event2", "data": {"value": 2}},
            {"type": "Event3", "data": {"value": 3}},
        ]

        await event_store.save_events(aggregate_id, events)

        # Get events from version 2
        retrieved: list[dict[str, object]] = await event_store.get_events(
            aggregate_id, from_version=2
        )
        assert len(retrieved) == 2
        assert retrieved[0]["version"] == 2
        assert retrieved[1]["version"] == 3

        # Get events up to version 2
        retrieved = await event_store.get_events(aggregate_id, to_version=2)
        assert len(retrieved) == 2
        assert retrieved[0]["version"] == 1
        assert retrieved[1]["version"] == 2

        # Get events between version 2 and 2
        retrieved = await event_store.get_events(aggregate_id, from_version=2, to_version=2)
        assert len(retrieved) == 1
        assert retrieved[0]["version"] == 2

    @pytest.mark.asyncio
    async def test_get_events_empty_aggregate(self, event_store: InMemoryEventStore) -> None:
        """Test retrieving events for non-existent aggregate."""
        retrieved: list[dict[str, object]] = await event_store.get_events("non-existent")
        assert retrieved == []

    @pytest.mark.asyncio
    async def test_save_and_get_snapshot(self, event_store: InMemoryEventStore) -> None:
        """Test saving and retrieving snapshots."""
        aggregate_id = "test-aggregate-5"
        snapshot: dict[str, object] = {"state": "active", "count": 42}

        await event_store.save_snapshot(aggregate_id, 10, snapshot)

        retrieved: dict[str, object] | None = await event_store.get_snapshot(aggregate_id, 10)
        assert retrieved == snapshot

    @pytest.mark.asyncio
    async def test_get_snapshot_not_found(self, event_store: InMemoryEventStore) -> None:
        """Test retrieving non-existent snapshot."""
        retrieved: dict[str, object] | None = await event_store.get_snapshot("non-existent", 1)
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_multiple_aggregates(self, event_store: InMemoryEventStore) -> None:
        """Test that events are isolated per aggregate."""
        await event_store.save_events("agg-1", [{"type": "E1", "data": {}}])
        await event_store.save_events("agg-2", [{"type": "E2", "data": {}}])

        events_1: list[dict[str, object]] = await event_store.get_events("agg-1")
        events_2: list[dict[str, object]] = await event_store.get_events("agg-2")

        assert len(events_1) == 1
        assert events_1[0]["type"] == "E1"
        assert len(events_2) == 1
        assert events_2[0]["type"] == "E2"
