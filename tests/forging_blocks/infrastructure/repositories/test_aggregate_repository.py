"""Tests for the AggregateRepository class."""

from typing import cast
from uuid import UUID, uuid7

import pytest

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.event_stores.in_memory_event_store_base import (
    InMemoryEventStoreBase,
)
from forging_blocks.infrastructure.repositories.aggregate_repository import (
    AggregateRepository,
)


class FakeEvent(Event[object]):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    @property
    def _payload(self) -> dict[str, object]:
        return {"name": self._name}

    @property
    def value(self) -> dict[str, object]:
        return self._payload


class FakeAggregate(AggregateRoot[UUID, object]):
    def __init__(self, aggregate_id: UUID) -> None:
        super().__init__(aggregate_id)
        self.items: list[str] = []

    def add_item(self, name: str) -> None:
        self.apply(FakeEvent(name))

    def _handle(self, event: Event[object]) -> None:
        if isinstance(event, FakeEvent):
            self.items.append(cast(str, event.value["name"]))


@pytest.mark.unit
class TestAggregateRepository:
    async def test_save_and_retrieve_aggregate(self) -> None:
        repo = AggregateRepository[object, FakeAggregate, UUID](
            event_store=InMemoryEventStoreBase[object](),
        )
        aggregate = FakeAggregate(uuid7())

        await repo.save(aggregate)
        retrieved = await repo.get_by_id(cast(UUID, aggregate.id))

        assert retrieved is not None
        assert retrieved.id == aggregate.id

    async def test_save_persists_events_to_event_store(self) -> None:
        event_store = InMemoryEventStoreBase[object]()
        repo = AggregateRepository[object, FakeAggregate, UUID](event_store=event_store)
        aggregate = FakeAggregate(uuid7())
        aggregate.add_item("widget")

        await repo.save(aggregate)

        result = await event_store.get_events(cast(UUID, aggregate.id))
        assert result.is_ok
        assert len(result.value) == 1

    async def test_get_by_id_returns_none_for_unknown_aggregate(self) -> None:
        repo = AggregateRepository[object, FakeAggregate, UUID](
            event_store=InMemoryEventStoreBase[object](),
        )

        retrieved = await repo.get_by_id(uuid7())

        assert retrieved is None

    async def test_save_with_multiple_events_persists_all(self) -> None:
        event_store = InMemoryEventStoreBase[object]()
        repo = AggregateRepository[object, FakeAggregate, UUID](event_store=event_store)
        aggregate = FakeAggregate(uuid7())
        aggregate.add_item("a")
        aggregate.add_item("b")
        aggregate.add_item("c")

        await repo.save(aggregate)

        result = await event_store.get_events(cast(UUID, aggregate.id))
        assert result.is_ok
        assert len(result.value) == 3

    async def test_save_without_events_does_not_append_to_event_store(self) -> None:
        event_store = InMemoryEventStoreBase[object]()
        repo = AggregateRepository[object, FakeAggregate, UUID](event_store=event_store)
        aggregate = FakeAggregate(uuid7())

        await repo.save(aggregate)

        result = await event_store.get_events(cast(UUID, aggregate.id))
        assert result.is_ok
        assert len(result.value) == 0

    async def test_init_with_prefilled_storage_finds_existing(self) -> None:
        aggregate = FakeAggregate(uuid7())
        storage = {cast(UUID, aggregate.id): aggregate}
        repo = AggregateRepository[object, FakeAggregate, UUID](
            event_store=InMemoryEventStoreBase[object](),
            storage=storage,
        )

        retrieved = await repo.get_by_id(cast(UUID, aggregate.id))

        assert retrieved is not None
        assert retrieved.id == aggregate.id

    async def test_get_by_id_returns_none_when_only_event_store_has_events(self) -> None:
        aggregate_id = uuid7()
        event_store = InMemoryEventStoreBase[object]()
        await event_store.append_events(aggregate_id, [FakeEvent("stale")])
        repo = AggregateRepository[object, FakeAggregate, UUID](event_store=event_store)

        retrieved = await repo.get_by_id(aggregate_id)

        assert retrieved is None
