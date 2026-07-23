"""Unit tests for DictMessageCodec round-trip encoding/decoding."""

import pytest

from forging_blocks.domain.messages import (
    MessageMetadata,
    command_dataclass,
    event_dataclass,
    query_dataclass,
)
from forging_blocks.domain.messages.command import Command
from forging_blocks.domain.messages.event import Event
from forging_blocks.domain.messages.query import Query
from forging_blocks.infrastructure.serialization import DictMessageCodec

PAYLOAD_MSG: dict[str, object] = {"_name": "write_in", "_value": 42}


@event_dataclass
class SimpleEvent(Event[dict[str, object]]):
    name: str


@command_dataclass
class SimpleCommand(Command[dict[str, object]]):
    action: str
    target: str


@query_dataclass
class SimpleQuery(Query[dict[str, object]]):
    resource: str
    filters: dict[str, object]


@pytest.mark.unit
class TestDictMessageCodecRoundTrip:
    """Round-trip encode/decode for message types."""

    codec: DictMessageCodec[SimpleEvent] = DictMessageCodec()
    generic_codec: DictMessageCodec = DictMessageCodec()

    def test_encode_event_returns_dict_with_metadata_and_payload(self) -> None:
        event = SimpleEvent(name="test_event")

        result = self.codec.encode(event)

        assert "metadata" in result
        assert "payload" in result
        assert result["payload"]["name"] == "test_event"

    def test_decode_event_from_dict_restores_fields(self) -> None:
        original = SimpleEvent(name="test_event")
        encoded = self.codec.encode(original)

        decoded = self.codec.decode(encoded, SimpleEvent)

        assert decoded.name == original.name
        assert decoded.metadata.message_type == original.metadata.message_type

    def test_encode_decode_round_trip_preserves_message_metadata(self) -> None:
        """Metadata values survive round-trip."""
        original = SimpleEvent(name="meta_check")
        encoded = self.codec.encode(original)

        decoded = self.codec.decode(encoded, SimpleEvent)

        assert decoded.metadata.message_id == original.metadata.message_id
        assert decoded.metadata.message_type == original.metadata.message_type
        assert decoded.metadata.correlation_id == original.metadata.correlation_id
        assert decoded.metadata.causation_id == original.metadata.causation_id

    def test_round_trip_with_compound_payload_fields(self) -> None:
        """Message with compound fields (dict) round-trips correctly."""
        original = SimpleQuery(resource="orders", filters={"status": "active"})
        encoded = self.generic_codec.encode(original)

        decoded = self.generic_codec.decode(encoded, SimpleQuery)

        assert decoded.resource == "orders"
        assert decoded.filters == {"status": "active"}

    def test_decode_constructs_metadata_from_raw_dict(self) -> None:
        """Metadata fields are reconstructed from serialized form."""
        encoded = self.codec.encode(SimpleEvent(name="meta"))
        decoded = self.codec.decode(encoded, SimpleEvent)

        assert decoded.metadata is not encoded["metadata"]
        assert isinstance(decoded.metadata, MessageMetadata)

    def test_encode_command_round_trip(self) -> None:
        original = SimpleCommand(action="ship", target="order-42")
        encoded = self.generic_codec.encode(original)

        decoded = self.generic_codec.decode(encoded, SimpleCommand)

        assert decoded.action == "ship"
        assert decoded.target == "order-42"
        assert isinstance(decoded, Command)

    def test_encode_query_round_trip(self) -> None:
        original = SimpleQuery(resource="users", filters={})
        encoded = self.generic_codec.encode(original)

        decoded = self.generic_codec.decode(encoded, SimpleQuery)

        assert decoded.resource == "users"
        assert isinstance(decoded, Query)


@pytest.mark.unit
class TestDictMessageCodecEdgeCases:
    """Edge cases for DictMessageCodec."""

    codec: DictMessageCodec[SimpleEvent] = DictMessageCodec()

    def test_encode_empty_payload_event(self) -> None:
        """Event with no user-defined fields still encodes."""

        @event_dataclass
        class EmptyEvent(Event[dict[str, object]]):
            pass

        event = EmptyEvent()
        e_codec: DictMessageCodec[EmptyEvent] = DictMessageCodec()
        encoded = e_codec.encode(event)

        assert "metadata" in encoded
        assert "payload" in encoded
        assert encoded["payload"] == {}

    def test_decode_preserves_message_type_in_metadata(self) -> None:
        """After round-trip, metadata.message_type matches the original class name."""
        original = SimpleEvent(name="type_check")
        e_codec: DictMessageCodec[SimpleEvent] = DictMessageCodec()
        encoded = e_codec.encode(original)

        decoded = e_codec.decode(encoded, SimpleEvent)

        assert decoded.metadata.message_type == "SimpleEvent"
