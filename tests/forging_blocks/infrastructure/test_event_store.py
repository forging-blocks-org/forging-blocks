"""Tests for the EventStoreBase base class and InMemoryEventStoreBase implementation."""

from __future__ import annotations

from uuid import uuid7

import pytest

from forging_blocks.application.errors.concurrency_error import ConcurrencyError
from forging_blocks.infrastructure.event_stores.event_store_base import EventStoreBase
from forging_blocks.infrastructure.event_stores.in_memory_event_store_base import (
    InMemoryEventStoreBase,
)
from tests.fixtures.fake_event_with_name import FakeEventWithName


class TestEventStoreBase:
    """Tests for the EventStoreBase base class."""

    def test_event_store_is_abstract(self) -> None:
        assert hasattr(EventStoreBase, "__abstractmethods__")
        assert "append_events" in EventStoreBase.__abstractmethods__
        assert "get_events" in EventStoreBase.__abstractmethods__
        assert "get_current_version" in EventStoreBase.__abstractmethods__


class TestInMemoryEventStoreBase:
    """Tests for the InMemoryEventStoreBase implementation."""

    @pytest.fixture
    def store(self) -> InMemoryEventStoreBase:
        return InMemoryEventStoreBase()

    async def test_append_and_get_events(self, store: InMemoryEventStoreBase) -> None:
        agg_id = uuid7()
        events = [FakeEventWithName("e1"), FakeEventWithName("e2")]

        r = await store.append_events(agg_id, events, expected_version=0)
        assert r.is_ok
        assert r.value == 2

        r = await store.get_events(agg_id)
        assert r.is_ok
        assert len(r.value) == 2

    async def test_get_events_empty(self, store: InMemoryEventStoreBase) -> None:
        r = await store.get_events(uuid7())
        assert r.is_ok
        assert r.value == []

    async def test_get_current_version_empty(self, store: InMemoryEventStoreBase) -> None:
        r = await store.get_current_version(uuid7())
        assert r.is_ok
        assert r.value == 0

    async def test_concurrency_error(self, store: InMemoryEventStoreBase) -> None:
        agg_id = uuid7()
        await store.append_events(agg_id, [FakeEventWithName("first")], expected_version=0)
        r = await store.append_events(agg_id, [FakeEventWithName("x")], expected_version=0)
        assert r.is_err
        assert isinstance(r.error, ConcurrencyError)

    async def test_concurrency_success(self, store: InMemoryEventStoreBase) -> None:
        agg_id = uuid7()
        await store.append_events(agg_id, [FakeEventWithName("a")])
        r = await store.append_events(agg_id, [FakeEventWithName("b")], expected_version=1)
        assert r.is_ok
        assert r.value == 2

    async def test_current_version_tracks_append(self, store: InMemoryEventStoreBase) -> None:
        agg_id = uuid7()
        r = await store.get_current_version(agg_id)
        assert r.is_ok and r.value == 0
        await store.append_events(agg_id, [FakeEventWithName("a"), FakeEventWithName("b")])
        r = await store.get_current_version(agg_id)
        assert r.is_ok and r.value == 2
