# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any
from unittest.mock import AsyncMock

import pytest
from pytest import fixture

from forging_blocks.application import EventPublisher, UnitOfWorkError
from forging_blocks.domain.aggregate_root import AggregateRoot
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.unit_of_work.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)


class FakeEvent(Event[str]):
    """A fake domain event for testing."""

    def __init__(self, data: str) -> None:
        super().__init__()
        self._data = data

    @property
    def value(self) -> str:
        return self._data

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}


class FakeAggregate(AggregateRoot[str, str]):
    """A fake aggregate root for testing."""

    def __init__(self, aggregate_id: str) -> None:
        super().__init__(aggregate_id)
        self.name = "test"

    def _handle(self, event: Event) -> None:
        pass


@pytest.mark.unit
class TestInMemoryUnitOfWork:
    @fixture
    def event_publisher(self) -> AsyncMock:
        publisher = AsyncMock(spec=EventPublisher)
        return publisher

    @fixture
    def aggregate(self) -> FakeAggregate:
        return FakeAggregate("agg-1")

    async def test_commit_when_modified_aggregate_has_events_then_publishes_them(
        self, event_publisher: AsyncMock, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork(event_publisher)
        event = FakeEvent("something happened")
        aggregate.record_event(event)

        uow.register_modified(aggregate)
        await uow.commit()

        event_publisher.publish.assert_called_once()

    async def test_commit_when_no_modified_aggregates_then_does_not_publish(
        self, event_publisher: AsyncMock
    ) -> None:
        uow = InMemoryUnitOfWork(event_publisher)

        await uow.commit()

        event_publisher.publish.assert_not_called()

    async def test_commit_when_no_event_publisher_then_completes_without_error(
        self, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork()
        event = FakeEvent("data")
        aggregate.record_event(event)

        uow.register_modified(aggregate)
        await uow.commit()

        assert uow.committed is True
        assert uow.rolled_back is False
        assert len(uow._modified_aggregates) == 0

    async def test_commit_when_event_publisher_raises_then_wraps_error(
        self, event_publisher: AsyncMock, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork(event_publisher)
        event = FakeEvent("data")
        aggregate.record_event(event)
        event_publisher.publish.side_effect = RuntimeError("Publish failed")

        uow.register_modified(aggregate)

        with pytest.raises(UnitOfWorkError):
            await uow.commit()

    async def test_rollback_when_modified_aggregates_then_clears_tracking(
        self, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork()
        event = FakeEvent("data")
        aggregate.record_event(event)

        uow.register_modified(aggregate)
        await uow.rollback()

        assert uow.rolled_back is True
        assert uow.committed is False
        assert len(uow._modified_aggregates) == 0
        assert len(aggregate.uncommitted_changes) == 0

    async def test_register_modified_when_called_then_tracks_aggregate(
        self, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork()

        uow.register_modified(aggregate)

        assert len(uow._modified_aggregates) == 1
        assert uow._modified_aggregates[aggregate.id] is aggregate

    async def test_commit_after_rollback_resets_rolled_back(self, aggregate: FakeAggregate) -> None:
        uow = InMemoryUnitOfWork()
        uow.register_modified(aggregate)

        await uow.rollback()
        assert uow.rolled_back is True
        assert uow.committed is False

        uow.register_modified(aggregate)
        await uow.commit()
        assert uow.committed is True
        assert uow.rolled_back is False

    async def test_rollback_after_commit_resets_committed(self, aggregate: FakeAggregate) -> None:
        uow = InMemoryUnitOfWork()
        uow.register_modified(aggregate)

        await uow.commit()
        assert uow.committed is True
        assert uow.rolled_back is False

        uow.register_modified(aggregate)
        await uow.rollback()
        assert uow.rolled_back is True
        assert uow.committed is False
