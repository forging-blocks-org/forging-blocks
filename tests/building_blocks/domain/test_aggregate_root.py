"""
Unit tests for the AggregateRoot module.

Tests for AggregateRoot class using Vaughn Vernon's approach.
"""

from typing import Any, List, Optional
from uuid import UUID, uuid4

import pytest

from building_blocks.domain.aggregate_root import AggregateRoot, AggregateVersion
from building_blocks.domain.entity import Entity
from building_blocks.domain.messages.event import Event
from building_blocks.domain.messages.message import MessageMetadata


class FakeEvent(Event):
    """A fake event for testing."""

    def __init__(self, data: str, metadata: Optional[MessageMetadata] = None):
        super().__init__(metadata)
        self._data = data

    @property
    def data(self) -> str:
        return self._data

    @property
    def payload(self) -> dict[str, Any]:
        return {"data": self._data}


class FakeAggregateRoot(AggregateRoot[UUID]):
    """A fake aggregate root for testing."""

    def __init__(
        self, aggregate_id: UUID, name: str, version: Optional[AggregateVersion] = None
    ):
        super().__init__(aggregate_id, version)
        if not isinstance(aggregate_id, UUID):
            raise TypeError(f"Expected UUID, got {type(aggregate_id).__name__}")
        self._name = name
        self._actions: List[str] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def actions(self) -> List[str]:
        return self._actions.copy()

    def perform_action(self, action: str) -> None:
        """Perform an action that records a domain event."""

        self._actions.append(action)

        # Record a domain event using Vernon's approach
        event = FakeEvent(f"Action performed: {action}")
        self.record_event(event)

    def change_name(self, new_name: str) -> None:
        """Change the name and increment version."""

        old_name = self._name
        self._name = new_name
        self._increment_version()

        # Record a domain event using Vernon's approach
        event = FakeEvent(f"Name changed from {old_name} to {new_name}")
        self.record_event(event)

    def perform_business_operation(self) -> None:
        """A business operation that records multiple events."""

        self.record_event(FakeEvent("Operation started"))
        self.record_event(FakeEvent("Operation in progress"))
        self.record_event(FakeEvent("Operation completed"))


class TestAggregateVersion:
    """Tests for AggregateVersion class."""

    def test_init_when_value_is_negative_then_raises_value_error(self):
        """Test that initializing with a negative value raises ValueError."""

        with pytest.raises(ValueError, match="Version cannot be negative"):
            AggregateVersion(-1)

    def test_init_when_value_is_not_int_then_raises_type_error(self):
        """Test that initializing with a non-integer value raises TypeError."""

        with pytest.raises(TypeError, match="Expected int, got str"):
            AggregateVersion("invalid_value")  # type: ignore

    def test_increment_increases_version_by_one(self):
        """Test that incrementing the version works correctly."""

        version = AggregateVersion(1)
        new_version = version.increment()
        assert new_version.value == 2


class TestAggregateRoot:
    """Tests for AggregateRoot class using Vernon's approach."""

    _name = "TestAggregateRoot"

    def test_inheritance_when_created_then_is_entity(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, self._name)

        assert isinstance(aggregate, Entity)
        assert isinstance(aggregate, AggregateRoot)
        assert aggregate.id == aggregate_id

    def test_generic_typing_when_created_then_preserves_id_type(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, self._name)

        # The aggregate should maintain the UUID type
        assert isinstance(aggregate.id, UUID)
        assert aggregate.id == aggregate_id

    def test_init_when_no_id_then_raises_type_error(self):
        """Test that initializing without an ID raises ValueError."""

        with pytest.raises(ValueError, match="Entity ID cannot be None"):
            FakeAggregateRoot(None, self._name)  # type: ignore

    def test_init_when_invalid_id_type_then_raises_type_error(self):
        """Test that initializing with an invalid ID type raises TypeError."""

        with pytest.raises(TypeError, match="Expected UUID, got str"):
            FakeAggregateRoot("invalid_id", self._name)  # type: ignore

    def test_init_when_no_version_then_starts_at_zero(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, self._name)

        assert aggregate.version.value == 0
        assert aggregate.uncommitted_changes() == []

    def test_init_when_custom_version_then_uses_provided_version(self):
        aggregate_id = uuid4()
        actual_version_value = 5
        version = AggregateVersion(value=actual_version_value)

        aggregate = FakeAggregateRoot(aggregate_id, self._name, version=version)

        expected_version_value = actual_version_value
        expected_version = AggregateVersion(value=expected_version_value)
        assert aggregate.version.value == expected_version_value
        assert aggregate.version == expected_version
        assert aggregate.uncommitted_changes() == []

    def test_record_event_when_called_then_event_recorded(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, self._name)

        aggregate.perform_action("test_action")

        changes = aggregate.uncommitted_changes()
        assert len(changes) == 1
        assert isinstance(changes[0], FakeEvent)
        fake_event = changes[0]  # Type narrowing for mypy
        assert isinstance(fake_event, FakeEvent)
        assert fake_event.data == "Action performed: test_action"

    def test_uncommitted_changes_when_called_then_returns_copy(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, self._name)

        aggregate.perform_action("test_action")

        changes1 = aggregate.uncommitted_changes()
        changes2 = aggregate.uncommitted_changes()

        # Should be different objects (copies)
        assert changes1 is not changes2
        # But with same content
        assert changes1 == changes2

        # Modifying returned List shouldn't affect aggregate
        changes1.clear()
        assert len(aggregate.uncommitted_changes()) == 1

    def test_mark_changes_as_committed_clears_events_and_increments_version(
        self,
    ):
        aggregate_id = uuid4()
        actual_version = AggregateVersion(value=3)
        aggregate = FakeAggregateRoot(aggregate_id, self._name, version=actual_version)

        # Record some events
        aggregate.perform_business_operation()  # Records 3 events
        assert len(aggregate.uncommitted_changes()) == 3
        assert aggregate.version.value == 3

        # Mark as committed
        aggregate.mark_changes_as_committed()

        # Events should be cleared and version incremented
        expected_version = AggregateVersion(value=4)
        assert len(aggregate.uncommitted_changes()) == 0
        assert aggregate.version == expected_version

    def test_multiple_operations_when_performed_then_events_accumulate(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, self._name)

        aggregate.perform_action("action1")
        aggregate.perform_action("action2")
        aggregate.change_name("new_name")

        changes = aggregate.uncommitted_changes()
        expected_changes_length = 3
        assert len(changes) == expected_changes_length

        # Type narrowing for mypy
        fake_events = [change for change in changes if isinstance(change, FakeEvent)]
        assert len(fake_events) == 3
        assert fake_events[0].data == "Action performed: action1"
        assert fake_events[1].data == "Action performed: action2"
        assert fake_events[2].data == f"Name changed from {self._name} to new_name"

    def test_version_control_scenario_tracks_version_correctly(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        initial_version = aggregate.version
        assert initial_version.value == 0

        # First change
        aggregate.change_name("name1")
        assert aggregate.version.value == 1

        # Second change
        aggregate.change_name("name2")
        assert aggregate.version.value == 2

        # Commit changes (simulating persistence)
        aggregate.mark_changes_as_committed()
        assert aggregate.version.value == 3
        assert len(aggregate.uncommitted_changes()) == 0

        # Another change after commit
        aggregate.change_name("name3")
        assert aggregate.version.value == 4
        assert len(aggregate.uncommitted_changes()) == 1

    def test_equality_when_same_id_then_equal_regardless_of_version(self):
        aggregate_id = uuid4()

        aggregate1_version = AggregateVersion(value=1)
        aggregate1 = FakeAggregateRoot(
            aggregate_id, "test1", version=aggregate1_version
        )
        aggregate2_version = AggregateVersion(value=5)
        aggregate2 = FakeAggregateRoot(
            aggregate_id, "test2", version=aggregate2_version
        )

        # Should be equal because Entity equality is based on ID
        assert aggregate1 == aggregate2
        assert hash(aggregate1) == hash(aggregate2)

    def test_equality_when_different_id_then_not_equal(self):
        """Test that different IDs are not equal."""

        version = AggregateVersion(value=1)
        aggregate1 = FakeAggregateRoot(uuid4(), "test", version=version)
        aggregate2 = FakeAggregateRoot(uuid4(), "test", version=version)

        assert aggregate1 != aggregate2
        assert hash(aggregate1) != hash(aggregate2)

    def test_vernon_naming_convention_integration_full_cycle_works(self):
        """Integration test using Vernon's naming conventions."""

        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "order")

        # 1. Perform business operations (record events)
        aggregate.perform_action("create")
        aggregate.perform_action("validate")
        aggregate.change_name("validated_order")

        # 2. Check uncommitted changes were recorded
        changes = aggregate.uncommitted_changes()
        assert len(changes) == 3
        assert aggregate.version.value == 1  # Only change_name increments version

        # 3. Simulate publishing events (get copy before committing)
        events_to_publish = aggregate.uncommitted_changes()
        assert len(events_to_publish) == 3

        # 4. Mark changes as committed after successful publishing and persistence
        aggregate.mark_changes_as_committed()
        assert aggregate.version.value == 2
        assert len(aggregate.uncommitted_changes()) == 0

        # 5. Continue with more operations
        aggregate.perform_action("ship")
        assert len(aggregate.uncommitted_changes()) == 1
        assert aggregate.version.value == 2  # Version only incremented on commit


class TestDomainEventManagement:
    """Tests focused on domain event management using Vernon's approach."""

    def test_event_ordering_when_multiple_events_then_preserves_order(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        # Events should be recorded in order
        aggregate.perform_action("first")
        aggregate.perform_action("second")
        aggregate.perform_action("third")

        changes = aggregate.uncommitted_changes()
        fake_events = [change for change in changes if isinstance(change, FakeEvent)]
        assert fake_events[0].data == "Action performed: first"
        assert fake_events[1].data == "Action performed: second"
        assert fake_events[2].data == "Action performed: third"

    def test_event_immutability_cannot_modify_internally(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        aggregate.perform_action("test")

        # Get uncommitted changes
        changes = aggregate.uncommitted_changes()
        original_count = len(changes)

        # Try to modify returned List (should not affect aggregate)
        changes.append(FakeEvent("malicious_event"))
        changes.clear()

        # Aggregate's events should be unchanged
        assert len(aggregate.uncommitted_changes()) == original_count
        fake_event = aggregate.uncommitted_changes()[0]
        assert isinstance(fake_event, FakeEvent)
        assert fake_event.data == "Action performed: test"

    def test_event_metadata_when_event_recorded_then_has_proper_metadata(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        aggregate.perform_action("test")

        event = aggregate.uncommitted_changes()[0]
        assert event.event_id is not None
        assert event.occurred_at is not None
        assert event.message_type == "FakeEvent"

    def test_vernon_approach_method_names_follows_conventions(self):
        """Test that we're following Vernon's naming conventions."""

        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        # Vernon's method names should be available
        assert hasattr(aggregate, "record_event")
        assert hasattr(aggregate, "uncommitted_changes")
        assert hasattr(aggregate, "mark_changes_as_committed")

        # Use Vernon's approach
        aggregate.record_event(FakeEvent("direct_event"))
        changes = aggregate.uncommitted_changes()
        assert len(changes) == 1

        aggregate.mark_changes_as_committed()
        assert len(aggregate.uncommitted_changes()) == 0
