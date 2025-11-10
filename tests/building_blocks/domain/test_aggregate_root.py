import pytest

from building_blocks.domain.aggregate_root import AggregateRoot, AggregateVersion
from building_blocks.domain.errors.entity_id_none_error import EntityIdNoneError
from building_blocks.domain.messages.event import Event

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


class TestAggregateVersion:
    def test___init___when_value_is_not_int_then_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            AggregateVersion("1")  # type: ignore

    def test___init___when_value_is_negative_then_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            AggregateVersion(-1)

    def test_value_when_accessed_then_returns_correct_integer(self) -> None:
        version = AggregateVersion(3)
        result = version.value
        assert result == 3

    def test_increment_when_called_then_returns_new_instance_with_value_incremented(self) -> None:
        version = AggregateVersion(2)
        result = version.increment()
        assert result.value == 3
        assert result is not version

    def test___eq___when_values_are_equal_then_returns_true(self) -> None:
        a = AggregateVersion(1)
        b = AggregateVersion(1)
        assert a == b

    def test___eq___when_values_differ_then_returns_false(self) -> None:
        a = AggregateVersion(1)
        b = AggregateVersion(2)
        assert a != b


class TestAggregateRoot:
    def test___init___when_id_is_none_then_raises_entity_id_none_error(self) -> None:
        with pytest.raises(EntityIdNoneError):
            OrderAggregate(None)  # type: ignore

    def test___init___when_id_is_valid_then_initializes_with_default_version_zero(self) -> None:
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

    def test_uncommitted_changes_when_no_events_recorded_then_returns_empty_list(self) -> None:
        aggregate = OrderAggregate(1)
        result = aggregate.uncommitted_changes()
        assert result == []

    def test_record_event_when_event_recorded_then_event_is_stored_in_uncommitted_events(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        event = DummyEvent("created")
        aggregate.record_event(event)
        result = aggregate.uncommitted_changes()
        assert result == [event]

    def test_collect_events_when_called_then_clears_uncommitted_events_and_increments_version(
        self,
    ) -> None:
        aggregate = OrderAggregate(1)
        aggregate.record_event(DummyEvent("x"))
        old_version = aggregate.version

        aggregate.collect_events()

        assert aggregate.uncommitted_changes() == []
        assert aggregate.version.value == old_version.value + 1

    def test__increment_version_when_called_then_increments_version_by_one(self) -> None:
        aggregate = OrderAggregate(1)
        old_version = aggregate.version.value
        aggregate._increment_version()
        assert aggregate.version.value == old_version + 1
