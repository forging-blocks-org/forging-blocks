"""Unit tests for the Message base class."""

from datetime import datetime, timezone
from typing import Any, Self
from uuid import UUID, uuid7

import pytest

from forging_blocks.foundation.messages import Message, MessageMetadata


class FakeMessage(Message[str]):
    """A fake message for testing the abstract Message class."""

    def __init__(self, data: str, metadata: MessageMetadata | None = None):
        super().__init__(metadata)
        self._data = data

    @property
    def value(self) -> str:
        return self._data

    @property
    def _payload(self) -> dict[str, Any]:
        return {"data": self._data}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(data=str(data.get("data", "")), metadata=metadata)


@pytest.mark.unit
class TestMessage:
    """Tests for Message class."""

    def test_init_when_no_metadata_then_creates_default_metadata(self):
        message = FakeMessage("test_data")

        assert isinstance(message.metadata, MessageMetadata)
        assert isinstance(message.message_id, UUID)
        assert isinstance(message.created_at, datetime)

    def test_init_when_custom_metadata_then_uses_provided_metadata(self):
        custom_metadata = MessageMetadata(
            message_type="CustomType",
            message_id=uuid7(),
            created_at=datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc),
        )

        message = FakeMessage("test_data", metadata=custom_metadata)

        assert message.metadata == custom_metadata
        assert message.message_id == custom_metadata.message_id
        assert message.created_at == custom_metadata.created_at

    def test_convenience_properties_when_called_then_delegates_to_metadata(self):
        custom_metadata = MessageMetadata(
            message_type="CustomType",
            message_id=uuid7(),
            created_at=datetime(2025, 6, 11, 19, 44, 14, tzinfo=timezone.utc),
        )

        message = FakeMessage("test_data", metadata=custom_metadata)

        assert message.message_id == custom_metadata.message_id
        assert message.created_at == custom_metadata.created_at

    def test_message_type_when_called_then_returns_class_name(self):
        message = FakeMessage("test_data")

        assert message.metadata.message_type == "FakeMessage"

    def test_eq_when_same_message_id_then_true(self):
        metadata = MessageMetadata(message_type="CustomType")
        message1 = FakeMessage("data1", metadata=metadata)
        message2 = FakeMessage("data2", metadata=metadata)

        assert message1 == message2

    def test_eq_when_different_message_id_then_false(self):
        message1 = FakeMessage("same_data")
        message2 = FakeMessage("same_data")

        assert message1 != message2

    def test_eq_when_type_different_than_message_then_false(self) -> None:
        metadata = MessageMetadata(message_type="CustomType")
        message = FakeMessage("data", metadata=metadata)
        another_type_instance = 5

        assert message != another_type_instance

    def test_hash_when_same_message_id_then_same_hash(self):
        metadata = MessageMetadata("FakeMessage", message_id=uuid7())

        message1 = FakeMessage("data1", metadata=metadata)
        message2 = FakeMessage("data2", metadata=metadata)

        assert hash(message1) == hash(message2)

    def test_hash_when_different_message_id_then_different_hash(self):
        message1 = FakeMessage("same_data")
        message2 = FakeMessage("same_data")

        assert hash(message1) != hash(message2)

    def test_cannot_instantiate_abstract_message_directly(self):
        with pytest.raises(TypeError, match="abstract"):
            type.__call__(Message)

    def test_metadata_property_when_called_then_returns_stored_metadata(self) -> None:
        metadata = MessageMetadata(message_type="FakeMessage")

        message = FakeMessage("test_data", metadata=metadata)

        assert message.metadata is metadata

    def test_eq_when_same_instance_then_true(self) -> None:
        message = FakeMessage("test_data")

        assert message == message

    def test_eq_when_different_message_type_then_false(self) -> None:
        class _(Message[str]):
            def __init__(self, data: str, metadata: MessageMetadata | None = None):
                super().__init__(metadata)
                self._data = data

            @property
            def value(self) -> str:
                return self._data

            @property
            def _payload(self) -> str:
                return self._data

            @classmethod
            def from_payload_fields(
                cls, data: dict[str, object], metadata: MessageMetadata
            ) -> Self:
                return cls(str(data.get("data", "")), metadata=metadata)

        fake = FakeMessage("data")
        other = _("data")

        assert fake != other
