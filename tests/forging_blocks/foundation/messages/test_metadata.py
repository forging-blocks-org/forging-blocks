"""Unit tests for MessageMetadata."""

from datetime import datetime, timezone
from uuid import UUID, uuid7

import pytest

from forging_blocks.foundation import CantModifyImmutableAttributeError
from forging_blocks.foundation.messages import MessageMetadata


@pytest.mark.unit
class TestMessageMetadata:
    """Tests for MessageMetadata value object."""

    causation_id = uuid7()
    created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)
    correlation_id = uuid7()
    message_id = uuid7()
    message_type = "FakeMessage"

    def test_init_when_no_params_then_generates_id_and_timestamp(self) -> None:
        """Only message_type provided; id and timestamp are auto-generated."""
        metadata = MessageMetadata(message_type=self.message_type)

        assert isinstance(metadata.message_id, UUID)
        assert isinstance(metadata.created_at, datetime)
        assert metadata.created_at.tzinfo == timezone.utc

    def test_init_when_custom_params_then_uses_provided_values(self) -> None:
        """All parameters provided explicitly; every field matches input."""
        metadata = MessageMetadata(
            message_type=self.message_type,
            message_id=self.message_id,
            created_at=self.created_at,
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
        )

        assert metadata.message_type == self.message_type
        assert metadata.message_id == self.message_id
        assert metadata.created_at == self.created_at
        assert metadata.correlation_id == self.correlation_id
        assert metadata.causation_id == self.causation_id

    def test_init_when_partial_params_then_generates_missing_values(self) -> None:
        """Only message_type and message_id provided; missing fields auto-generated."""
        metadata = MessageMetadata(message_type=self.message_type, message_id=self.message_id)

        assert metadata.message_id == self.message_id
        assert isinstance(metadata.created_at, datetime)
        assert metadata.created_at.tzinfo == timezone.utc
        assert isinstance(metadata.correlation_id, UUID)
        assert isinstance(metadata.causation_id, UUID)

    def test_init_when_causation_id_provided_then_stores_it(self) -> None:
        """Explicit causation_id is stored rather than auto-generated."""
        explicit_causation = uuid7()

        metadata = MessageMetadata(message_type=self.message_type, causation_id=explicit_causation)

        assert metadata.causation_id == explicit_causation

    def test_causation_id_property_when_called_then_returns_uuid(self) -> None:
        """causation_id always returns a UUID instance."""
        metadata = MessageMetadata(message_type=self.message_type)

        assert isinstance(metadata.causation_id, UUID)

    def test_correlation_id_property_when_called_then_returns_uuid(self) -> None:
        """correlation_id always returns a UUID instance."""
        metadata = MessageMetadata(message_type=self.message_type)

        assert isinstance(metadata.correlation_id, UUID)

    def test_message_id_property_when_called_then_returns_uuid(self) -> None:
        """message_id always returns a UUID instance."""
        metadata = MessageMetadata(message_type=self.message_type)

        assert isinstance(metadata.message_id, UUID)

    def test_created_at_property_when_default_then_has_utc_timezone(self) -> None:
        """Auto-generated created_at carries UTC timezone info."""
        metadata = MessageMetadata(message_type=self.message_type)

        assert metadata.created_at.tzinfo == timezone.utc

    def test_created_at_when_provided_without_timezone_then_preserves_value(self) -> None:
        """Naive datetime passed as-is — no timezone coercion applied."""
        naive = datetime(2025, 6, 11, 19, 44, 14)

        metadata = MessageMetadata(message_type=self.message_type, created_at=naive)

        assert metadata.created_at == naive
        assert metadata.created_at.tzinfo is None

    def test_eq_when_all_fields_equal_then_true(self) -> None:
        """Two instances with identical values for all fields are equal."""
        metadata1 = MessageMetadata(
            message_type=self.message_type,
            message_id=self.message_id,
            created_at=self.created_at,
            causation_id=self.causation_id,
            correlation_id=self.correlation_id,
        )
        metadata2 = MessageMetadata(
            message_type=self.message_type,
            message_id=self.message_id,
            created_at=self.created_at,
            causation_id=self.causation_id,
            correlation_id=self.correlation_id,
        )

        assert metadata1 == metadata2

    def test_eq_when_different_id_then_false(self) -> None:
        """Same timestamp, different message_id — not equal."""
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)

        metadata1 = MessageMetadata(
            message_type=self.message_type,
            message_id=uuid7(),
            created_at=created_at,
        )
        metadata2 = MessageMetadata(
            message_type=self.message_type,
            message_id=uuid7(),
            created_at=created_at,
        )

        assert metadata1 != metadata2

    def test_eq_when_different_timestamp_then_false(self) -> None:
        """Same message_id, different created_at — not equal."""
        message_id = uuid7()

        metadata1 = MessageMetadata(
            message_type=self.message_type,
            message_id=message_id,
            created_at=datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc),
        )
        metadata2 = MessageMetadata(
            message_type=self.message_type,
            message_id=message_id,
            created_at=datetime(2025, 6, 11, 19, 44, 15, tzinfo=timezone.utc),
        )

        assert metadata1 != metadata2

    def test_eq_when_different_type_then_false(self) -> None:
        """A MessageMetadata is never equal to a non-ValueObject instance."""
        metadata = MessageMetadata(message_type=self.message_type)

        assert metadata != "not metadata"
        assert metadata != 42

    def test_hash_when_all_fields_equal_then_same_hash(self) -> None:
        """Equal instances (all fields match) produce identical hashes."""
        message_id = uuid7()
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)
        causation_id = uuid7()
        correlation_id = uuid7()

        metadata1 = MessageMetadata(
            message_type=self.message_type,
            message_id=message_id,
            created_at=created_at,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )
        metadata2 = MessageMetadata(
            message_type=self.message_type,
            message_id=message_id,
            created_at=created_at,
            causation_id=causation_id,
            correlation_id=correlation_id,
        )

        assert hash(metadata1) == hash(metadata2)

    def test_hash_when_different_values_then_different_hash(self) -> None:
        """Instances with different ids produce different hashes."""
        metadata1 = MessageMetadata(message_type="Message")
        metadata2 = MessageMetadata(message_type="AnotherMessage")

        assert hash(metadata1) != hash(metadata2)

    def test_hash_consistency_when_same_instance_then_same_hash(self) -> None:
        """Hash called multiple times on the same instance returns same value."""
        metadata = MessageMetadata(message_type=self.message_type)

        assert hash(metadata) == hash(metadata)

    def test_value_property_when_called_then_returns_all_fields(self) -> None:
        """value dict contains every metadata field with correct serialized values."""
        message_id = uuid7()
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)

        metadata = MessageMetadata(
            message_type=self.message_type,
            message_id=message_id,
            created_at=created_at,
        )
        value = metadata.value

        assert value["message_type"] == self.message_type
        assert value["message_id"] == str(message_id)
        assert value["created_at"] == "2025-06-11T19:44:14+00:00"
        UUID(str(value["correlation_id"]))
        UUID(str(value["causation_id"]))

    def test_modification_when_setting_attribute_then_raises(self) -> None:
        """MessageMetadata is immutable — attribute assignment raises."""
        metadata = MessageMetadata(message_type=self.message_type)

        with pytest.raises(CantModifyImmutableAttributeError):
            metadata._message_id = uuid7()  # type: ignore[reportAttributeAccessIssue]
