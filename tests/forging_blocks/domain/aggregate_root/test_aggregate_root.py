# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.domain import (
    AggregateRoot,
    AggregateVersion,
    EntityIdNoneError,
)
from forging_blocks.foundation import Event

raw_event = dict[str, str]


class DummyEvent(Event[raw_event]):
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def value(self) -> raw_event:
        return {"name": self.name}

    @property
    def _payload(self) -> raw_event:
        return {"name": self.name}


class OrderAggregate(AggregateRoot[int]):
    def __init__(self, aggregate_id: int, version: AggregateVersion | None = None) -> None:
        super().__init__(aggregate_id, version)

    def apply(self, event: Event) -> None:
        self.record_event(event)


class StringAggregate(AggregateRoot[str]):
    def __init__(self, aggregate_id: str) -> None:
        super().__init__(aggregate_id)

    def apply(self, event: Event) -> None:
        self.record_event(event)


class BoolAggregate(AggregateRoot[bool]):
    def __init__(self, aggregate_id: bool) -> None:
        super().__init__(aggregate_id)

    def apply(self, event: Event) -> None:
        self.record_event(event)


@pytest.mark.unit
class TestAggregateRoot:
    def test___init___when_id_is_none_then_raises_entity_id_none_error(self) -> None:
        with pytest.raises(EntityIdNoneError):
            OrderAggregate(None)  # type: ignore

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

    def test___init___when_version_is_not_provided_then_sets_version_zero(self) -> None:
        id = 1
        aggregate = OrderAggregate(id)

        expected_version_value = 0

        assert aggregate.version.value == expected_version_value

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
        result = aggregate.uncommitted_changes
        assert result == [event]

    def test_collect_events_when_called_then_clears_uncommitted_events_and_increments_version(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        aggregate.record_event(DummyEvent("x"))
        old_version = aggregate.version

        aggregate.collect_events()

        assert aggregate.uncommitted_changes == []
        assert aggregate.version.value == old_version.value + 1

    def test_discard_events_when_called_then_clears_uncommitted_events_without_version_bump(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        aggregate.record_event(DummyEvent("x"))
        old_version = aggregate.version

        aggregate.discard_events()

        assert aggregate.uncommitted_changes == []
        assert aggregate.version == old_version

    def test_collect_events_when_no_events_then_does_not_increment_version(self) -> None:
        aggregate = OrderAggregate(1)

        aggregate.collect_events()

        assert aggregate.version.value == 0

    def test___init___when_id_is_zero_then_initializes_successfully(self) -> None:
        aggregate = OrderAggregate(0)

        assert aggregate.id == 0
        assert aggregate.version.value == 0

    def test___init___when_id_is_empty_string_then_raises_entity_id_none_error(self) -> None:
        with pytest.raises(EntityIdNoneError):
            StringAggregate("")

    def test_apply_when_called_then_records_event_in_uncommitted(self) -> None:
        aggregate = OrderAggregate(1)
        event = DummyEvent("created")

        aggregate.apply(event)

        assert event in aggregate.uncommitted_changes

    def test_apply_is_abstract_on_aggregate_root(self) -> None:
        assert getattr(AggregateRoot.apply, "__isabstractmethod__", False) is True

    def test___init___when_id_is_false_then_raises_entity_id_none_error(self) -> None:
        with pytest.raises(EntityIdNoneError):
            BoolAggregate(False)

    def test___init___when_id_is_true_then_initializes_successfully(self) -> None:
        aggregate = BoolAggregate(True)

        assert aggregate.id is True
        assert aggregate.version.value == 0
