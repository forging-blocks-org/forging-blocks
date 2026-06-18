"""Tests for the InMemoryEventStore implementation."""

from uuid import uuid7

import pytest

from forging_blocks.application.ports.outbound.event_store import ConcurrencyError
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.infrastructure.event_stores.in_memory_event_store import (
    InMemoryEventStore,
)


class FakeEvent(Event[dict[str, object]]):
    """A simple domain event for testing."""

    def __init__(self, name: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._name = name

    @property
    def _payload(self) -> dict[str, object]:
        return {"name": self._name}

    @property
    def value(self) -> dict[str, object]:
        return self._payload


@pytest.mark.unit
class TestInMemoryEventStore:
    """InMemoryEventStore append / get / version behaviour."""

    async def test_append_and_get_events(self) -> None:
        """Events appended to a stream can be retrieved in order."""
        store: InMemoryEventStore[dict[str, object]] = InMemoryEventStore()
        agg_id = uuid7()
        events = [FakeEvent("evt1"), FakeEvent("evt2")]

        version = await store.append_events(agg_id, events, expected_version=0)
        assert version.is_ok()
        assert version.unwrap() == 2

        result = await store.get_events(agg_id)
        assert result.is_ok()
        retrieved = result.unwrap()
        assert len(retrieved) == 2
        assert retrieved[0]._name == "evt1"
        assert retrieved[1]._name == "evt2"

    async def test_get_events_empty_stream(self) -> None:
        """Getting events from an unknown aggregate returns an empty list."""
        store: InMemoryEventStore[dict[str, object]] = InMemoryEventStore()
        result = await store.get_events(uuid7())
        assert result.is_ok()
        assert result.unwrap() == []

    async def test_get_current_version_empty(self) -> None:
        """An empty stream has version 0."""
        store: InMemoryEventStore[dict[str, object]] = InMemoryEventStore()
        result = await store.get_current_version(uuid7())
        assert result.is_ok()
        assert result.unwrap() == 0

    async def test_concurrency_error(self) -> None:
        """Appending with a wrong expected_version returns a ConcurrencyError."""
        store: InMemoryEventStore[dict[str, object]] = InMemoryEventStore()
        agg_id = uuid7()
        await store.append_events(agg_id, [FakeEvent("first")], expected_version=0)

        result = await store.append_events(agg_id, [FakeEvent("conflict")], expected_version=0)
        assert result.is_err()
        assert isinstance(result.unwrap_err(), ConcurrencyError)

    async def test_get_events_with_version_range(self) -> None:
        """Events can be retrieved within a version range."""
        store: InMemoryEventStore[dict[str, object]] = InMemoryEventStore()
        agg_id = uuid7()
        events = [FakeEvent(f"evt{i}") for i in range(5)]
        await store.append_events(agg_id, events)

        result = await store.get_events(agg_id, from_version=1, to_version=3)
        assert result.is_ok()
        sliced = result.unwrap()
        assert len(sliced) == 3
        assert sliced[0]._name == "evt1"
        assert sliced[2]._name == "evt3"

    async def test_current_version_after_append(self) -> None:
        """Current version reflects total events appended."""
        store: InMemoryEventStore[dict[str, object]] = InMemoryEventStore()
        agg_id = uuid7()
        assert (await store.get_current_version(agg_id)).unwrap() == 0

        await store.append_events(agg_id, [FakeEvent("a"), FakeEvent("b")])
        assert (await store.get_current_version(agg_id)).unwrap() == 2

        await store.append_events(agg_id, [FakeEvent("c")])
        assert (await store.get_current_version(agg_id)).unwrap() == 3
