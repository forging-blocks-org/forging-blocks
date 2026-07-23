from typing import Self

import pytest

from forging_blocks.domain import (
    AggregateRoot,
    AggregateVersion,
    EntityIdNoneError,
)
from forging_blocks.foundation import Event
from forging_blocks.foundation.messages.message import MessageMetadata

raw_event = dict[str, str]


class DummyEvent(Event[raw_event]):
    def __init__(self, name: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self.name = name

    @property
    def value(self) -> raw_event:
        return {"name": self.name}

    @property
    def _payload(self) -> raw_event:
        return {"name": self.name}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(name=str(data.get("name", "")), metadata=metadata)


class OrderAggregate(AggregateRoot[int, raw_event]):
    def __init__(self, aggregate_id: int, version: AggregateVersion | None = None) -> None:
        super().__init__(aggregate_id, version)

    def _handle(self, _: Event) -> None:
        pass


class StringAggregate(AggregateRoot[str, raw_event]):
    def __init__(self, aggregate_id: str) -> None:
        super().__init__(aggregate_id)

    def _handle(self, _: Event) -> None:
        pass


class BoolAggregate(AggregateRoot[bool, raw_event]):
    def __init__(self, aggregate_id: bool) -> None:
        super().__init__(aggregate_id)

    def _handle(self, _: Event) -> None:
        pass


@pytest.mark.unit
class TestAggregateRoot:
    def test___init___when_id_is_none_then_raises_entity_id_none_error(self) -> None:
        with pytest.raises(EntityIdNoneError):
            OrderAggregate(None)

    def test___init___when_id_is_valid_then_initializes_with_default_version_zero(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)

        assert aggregate.id == 1
        assert aggregate.version.value == 0

    def test___init___when_version_is_provided_then_sets_custom_version(self) -> None:
        custom_version = AggregateVersion(5)

        aggregate = OrderAggregate(1, version=custom_version)

        assert aggregate.version == custom_version

    def test___init___when_id_is_zero_then_initializes_successfully(self) -> None:
        aggregate = OrderAggregate(0)

        assert aggregate.id == 0
        assert aggregate.version.value == 0

    def test___init___when_id_is_empty_string_then_raises_entity_id_none_error(self) -> None:
        with pytest.raises(EntityIdNoneError):
            StringAggregate("")

    def test___init___when_id_is_false_then_raises_entity_id_none_error(self) -> None:
        with pytest.raises(EntityIdNoneError):
            BoolAggregate(False)

    def test___init___when_id_is_true_then_initializes_successfully(self) -> None:
        aggregate = BoolAggregate(True)

        assert aggregate.id is True
        assert aggregate.version.value == 0

    def test_version_property_when_accessed_then_returns_current_version(self) -> None:
        aggregate = OrderAggregate(1)

        result = aggregate.version

        assert isinstance(result, AggregateVersion)
        assert result.value == 0

    def test_uncommitted_changes_when_no_events_recorded_then_returns_empty_list(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)

        result = aggregate.uncommitted_changes

        assert result == []

    def test_record_event_when_event_recorded_then_event_is_stored_in_uncommitted_events(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        event = DummyEvent("created")

        aggregate.record_event(event)

        assert aggregate.uncommitted_changes == [event]

    def test_collect_events_when_called_then_clears_uncommitted_events(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        aggregate.record_event(DummyEvent("x"))

        aggregate.collect_events()

        assert aggregate.uncommitted_changes == []

    def test_collect_events_when_called_then_does_not_increment_version(self) -> None:
        aggregate = OrderAggregate(1)
        aggregate.record_event(DummyEvent("x"))

        aggregate.collect_events()

        assert aggregate.version == AggregateVersion(0)

    def test_discard_events_when_called_then_clears_uncommitted_events_without_version_bump(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        aggregate.record_event(DummyEvent("x"))
        old_version = aggregate.version

        aggregate.discard_events()

        assert aggregate.uncommitted_changes == []
        assert aggregate.version == old_version

    def test_apply_when_called_then_records_event_in_uncommitted(self) -> None:
        aggregate = OrderAggregate(1)
        event = DummyEvent("created")

        aggregate.apply(event)

        assert event in aggregate.uncommitted_changes

    def test_apply_when_called_then_increments_version(self) -> None:
        aggregate = OrderAggregate(1)
        event = DummyEvent("created")

        aggregate.apply(event)

        assert aggregate.version == AggregateVersion(1)

    def test_replay_when_called_then_does_not_record_event_in_uncommitted(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        event = DummyEvent("replayed")

        aggregate.replay(event)

        assert aggregate.uncommitted_changes == []

    def test_replay_when_called_then_increments_version(self) -> None:
        aggregate = OrderAggregate(1)
        event = DummyEvent("replayed")

        aggregate.replay(event)

        assert aggregate.version == AggregateVersion(1)

    def test_reconstitute_when_called_then_creates_aggregate_with_given_id(
        self,
    ) -> None:
        events = [DummyEvent("a")]

        aggregate = OrderAggregate.reconstitute(42, events)

        assert aggregate.id == 42

    def test_reconstitute_when_called_then_replays_all_events_in_order(
        self,
    ) -> None:
        events = [DummyEvent("a"), DummyEvent("b"), DummyEvent("c")]

        aggregate = OrderAggregate.reconstitute(1, events)

        assert aggregate.version.value == 3

    def test_reconstitute_when_called_then_does_not_record_events_as_uncommitted(
        self,
    ) -> None:
        events = [DummyEvent("a")]

        aggregate = OrderAggregate.reconstitute(1, events)

        assert aggregate.uncommitted_changes == []

    def test_reconstitute_when_empty_event_list_then_has_version_zero_and_returns_aggregate(
        self,
    ) -> None:
        aggregate = OrderAggregate.reconstitute(1, [])

        assert aggregate is not None
        assert aggregate.id == 1
        assert aggregate.version.value == 0

    def test_reconstitute_when_handle_raises_then_exception_propagates(self) -> None:
        class _(AggregateRoot[int, raw_event]):
            def __init__(self, aggregate_id: int) -> None:
                super().__init__(aggregate_id)

            def _handle(self, event: Event[raw_event]) -> None:
                msg = "Replay failed"
                raise RuntimeError(msg)

        events = [DummyEvent("boom")]

        with pytest.raises(RuntimeError, match="Replay failed"):
            _.reconstitute(1, events)
