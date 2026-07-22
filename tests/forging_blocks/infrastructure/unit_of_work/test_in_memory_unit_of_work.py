# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
from typing import Any, Self

import pytest

from forging_blocks.application import UnitOfWorkError
from forging_blocks.domain.aggregate_root import AggregateRoot
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata
from forging_blocks.infrastructure.unit_of_work.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)
from tests.fixtures.fake_event_publisher import FakeEventPublisher


class FakeEvent(Event[str]):
    """A fake domain event for testing."""

    def __init__(self, data: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._data = data

    @property
    def value(self) -> str:
        return self._data

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(data=str(data.get("data", "")), metadata=metadata)


class FakeAggregate(AggregateRoot[str, str]):
    """A fake aggregate root for testing."""

    def __init__(self, aggregate_id: str) -> None:
        super().__init__(aggregate_id)
        self.name = "test"

    def _handle(self, event: Event) -> None:
        pass


@pytest.mark.integration
class TestInMemoryUnitOfWork:
    @pytest.fixture
    def event_publisher(self) -> FakeEventPublisher:
        return FakeEventPublisher()

    @pytest.fixture
    def failing_publisher(self) -> FakeEventPublisher:
        return FakeEventPublisher(should_raise=RuntimeError("Publish failed"))

    @pytest.fixture
    def aggregate(self) -> FakeAggregate:
        return FakeAggregate("agg-1")

    @pytest.fixture
    def draft_aggregate(self) -> FakeAggregate:
        """Return a FakeAggregate with _id set to None via object.__setattr__.

        This simulates a draft entity that has not yet been persisted.
        Using object.__setattr__ bypasses both the Entity.__setattr__ guard
        and the auto_freeze mechanism.
        """
        agg = FakeAggregate("temp-id")
        object.__setattr__(agg, "_id", None)
        return agg

    async def test_commit_when_modified_aggregate_has_events_then_publishes_them(
        self, event_publisher: FakeEventPublisher, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork(event_publisher)
        event = FakeEvent("something happened")
        aggregate.record_event(event)

        uow.register_modified(aggregate)
        await uow.commit()

        assert len(event_publisher.published_events) == 1

    async def test_commit_when_no_modified_aggregates_then_does_not_publish(
        self, event_publisher: FakeEventPublisher
    ) -> None:
        uow = InMemoryUnitOfWork(event_publisher)

        await uow.commit()

        assert len(event_publisher.published_events) == 0

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
        self, failing_publisher: FakeEventPublisher, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork(failing_publisher)
        event = FakeEvent("data")
        aggregate.record_event(event)

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

    async def test_context_manager_when_no_exception_then_commits(
        self, event_publisher: FakeEventPublisher, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork(event_publisher)
        event = FakeEvent("data")
        aggregate.record_event(event)

        async with uow:
            uow.register_modified(aggregate)

        assert uow.committed is True
        assert len(event_publisher.published_events) == 1

    async def test_context_manager_when_exception_then_rolls_back(
        self, event_publisher: FakeEventPublisher, aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork(event_publisher)

        with pytest.raises(ValueError, match="boom"):
            async with uow:
                uow.register_modified(aggregate)
                raise ValueError("boom")

        assert uow.rolled_back is True
        assert uow.committed is False

    async def test_register_modified_when_aggregate_id_is_none_then_raises(
        self, draft_aggregate: FakeAggregate
    ) -> None:
        uow = InMemoryUnitOfWork()

        with pytest.raises(ValueError, match="Cannot register aggregate with None id"):
            uow.register_modified(draft_aggregate)
