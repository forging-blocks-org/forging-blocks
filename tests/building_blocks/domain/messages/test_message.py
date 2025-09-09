"""
Unit tests for the Message module.

Tests for MessageMetadata and Message classes.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import pytest

from building_blocks.domain.messages.message import Message, MessageMetadata


class FakeMessage(Message):
    """A fake message for testing the abstract Message class."""

    def __init__(self, data: str, metadata: MessageMetadata | None = None):
        super().__init__(metadata)
        self._data = data

    @property
    def data(self) -> str:
        return self._data

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}


class TestMessageMetadata:
    """Tests for MessageMetadata class."""

    def test_init_when_no_params_then_generates_id_and_timestamp(self):
        metadata = MessageMetadata()

        assert isinstance(metadata.message_id, UUID)
        assert isinstance(metadata.created_at, datetime)
        assert metadata.created_at.tzinfo == timezone.utc

    def test_init_when_custom_params_then_uses_provided_values(self):
        custom_id = uuid4()
        custom_time = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)

        metadata = MessageMetadata(message_id=custom_id, created_at=custom_time)

        assert metadata.message_id == custom_id
        assert metadata.created_at == custom_time

    def test_init_when_partial_params_then_generates_missing_values(self):
        custom_id = uuid4()

        metadata = MessageMetadata(message_id=custom_id)

        assert metadata.message_id == custom_id
        assert isinstance(metadata.created_at, datetime)
        assert metadata.created_at.tzinfo == timezone.utc

    def test_eq_when_same_id_and_timestamp_then_true(self):
        message_id = uuid4()
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)

        metadata1 = MessageMetadata(message_id=message_id, created_at=created_at)
        metadata2 = MessageMetadata(message_id=message_id, created_at=created_at)

        assert metadata1 == metadata2

    def test_eq_when_different_id_then_false(self):
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)

        metadata1 = MessageMetadata(message_id=uuid4(), created_at=created_at)
        metadata2 = MessageMetadata(message_id=uuid4(), created_at=created_at)

        assert metadata1 != metadata2

    def test_eq_when_different_timestamp_then_false(self):
        message_id = uuid4()

        metadata1 = MessageMetadata(
            message_id=message_id,
            created_at=datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc),
        )
        metadata2 = MessageMetadata(
            message_id=message_id,
            created_at=datetime(2025, 6, 11, 19, 44, 15, tzinfo=timezone.utc),
        )

        assert metadata1 != metadata2

    def test_to_dict_when_called_then_returns_serializable_dict(self):
        message_id = uuid4()
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)

        metadata = MessageMetadata(message_id=message_id, created_at=created_at)
        result = metadata.to_dict()

        expected = {
            "message_id": str(message_id),
            "created_at": "2025-06-11T19:44:14+00:00",
        }
        assert result == expected

    def test_hash_when_same_values_then_same_hash(self):
        message_id = uuid4()
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)

        metadata1 = MessageMetadata(message_id=message_id, created_at=created_at)
        metadata2 = MessageMetadata(message_id=message_id, created_at=created_at)

        assert hash(metadata1) == hash(metadata2)

    def test_hash_when_different_values_then_different_hash(self):
        metadata1 = MessageMetadata()
        metadata2 = MessageMetadata()

        assert hash(metadata1) != hash(metadata2)


class TestMessage:
    """Tests for Message class."""

    def test_init_when_no_metadata_then_creates_default_metadata(self):
        message = FakeMessage("test_data")

        assert isinstance(message.metadata, MessageMetadata)
        assert isinstance(message.message_id, UUID)
        assert isinstance(message.created_at, datetime)

    def test_init_when_custom_metadata_then_uses_provided_metadata(self):
        custom_metadata = MessageMetadata(
            message_id=uuid4(),
            created_at=datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc),
        )

        message = FakeMessage("test_data", metadata=custom_metadata)

        assert message.metadata == custom_metadata
        assert message.message_id == custom_metadata.message_id
        assert message.created_at == custom_metadata.created_at

    def test_convenience_properties_when_called_then_delegates_to_metadata(self):
        custom_metadata = MessageMetadata(
            message_id=uuid4(),
            created_at=datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc),
        )

        message = FakeMessage("test_data", metadata=custom_metadata)

        assert message.message_id == custom_metadata.message_id
        assert message.created_at == custom_metadata.created_at

    def test_message_type_when_called_then_returns_class_name(self):
        message = FakeMessage("test_data")

        assert message.message_type == "FakeMessage"

    def test_eq_when_same_message_id_then_true(self):
        metadata = MessageMetadata()

        message1 = FakeMessage("data1", metadata=metadata)
        message2 = FakeMessage(
            "data2", metadata=metadata
        )  # Different data, same metadata

        assert message1 == message2

    def test_eq_when_different_message_id_then_false(self):
        message1 = FakeMessage("same_data")
        message2 = FakeMessage("same_data")

        assert message1 != message2

    def test_to_dict_when_called_then_includes_metadata_type_and_payload(self):
        message_id = uuid4()
        created_at = datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc)
        metadata = MessageMetadata(message_id=message_id, created_at=created_at)

        message = FakeMessage("test_data", metadata=metadata)
        result = message.to_dict()

        expected = {
            "message_id": str(message_id),
            "created_at": "2025-06-11T19:44:14+00:00",
            "message_type": "FakeMessage",
            "payload": {"data": "test_data"},
        }
        assert result == expected

    def test_hash_when_same_message_id_then_same_hash(self):
        metadata = MessageMetadata()

        message1 = FakeMessage("data1", metadata=metadata)
        message2 = FakeMessage("data2", metadata=metadata)

        assert hash(message1) == hash(message2)

    def test_hash_when_different_message_id_then_different_hash(self):
        message1 = FakeMessage("same_data")
        message2 = FakeMessage("same_data")

        assert hash(message1) != hash(message2)

    def test_cannot_instantiate_abstract_message_directly(self):
        with pytest.raises(TypeError, match="abstract"):
            # This should raise TypeError because Message is abstract an payload is
            # abstract
            Message()  # type: ignore[abstract]
