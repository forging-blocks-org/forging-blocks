"""Tests for the Serializable protocol and message serialisation support."""

import dataclasses
from datetime import datetime, timezone
from typing import Any, cast
from uuid import uuid7

import pytest

from forging_blocks.foundation.messages.decorators import (
    command_dataclass,
    event_dataclass,
    query_dataclass,
)
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata


class SimpleEvent(Event[dict[str, object]]):
    """Simple event dummy for testing."""

    @property
    def _payload(self) -> dict[str, object]:
        return {"key": "value"}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def _from_payload_fields(
        cls, data: dict[str, object], metadata: MessageMetadata
    ) -> "SimpleEvent":
        return cls()


class EventWithoutFromPayloadFields(Event[dict[str, object]]):
    """Event dummy without _from_payload_fields for testing."""

    @property
    def _payload(self) -> dict[str, object]:
        return {}

    @property
    def value(self) -> dict[str, object]:
        return self._payload


class CustomEvent(Event[dict[str, object]]):
    """Event dummy with custom _from_payload_fields for testing."""

    def __init__(self, value: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._value = value

    @property
    def _payload(self) -> dict[str, object]:
        return {"value": self._value}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def _from_payload_fields(
        cls, data: dict[str, object], metadata: MessageMetadata
    ) -> "CustomEvent":
        return cls(value=str(data["value"]), metadata=metadata)


class TestMessageMetadataSerialization:
    """MessageMetadata.from_dict() round-trip."""

    def test_from_dict_round_trip(self) -> None:
        """A MessageMetadata serialised to dict and back should be equivalent."""
        original = MessageMetadata(message_type="TestEvent")
        data = original.to_dict()
        restored = MessageMetadata.from_dict(data)
        assert restored.message_id == original.message_id
        assert restored.created_at == original.created_at
        assert restored.correlation_id == original.correlation_id
        assert restored.causation_id == original.causation_id
        assert restored.message_type == original.message_type

    def test_from_dict_with_explicit_values(self) -> None:
        """from_dict() handles explicit, non-None values correctly."""
        mid = uuid7()
        ts = datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc)
        cid = uuid7()
        caid = uuid7()
        data: dict[str, object] = {
            "message_type": "CustomEvent",
            "message_id": str(mid),
            "created_at": ts.isoformat(),
            "correlation_id": str(cid),
            "causation_id": str(caid),
        }
        meta = MessageMetadata.from_dict(data)
        assert meta.message_id == mid
        assert meta.created_at == ts
        assert meta.correlation_id == cid
        assert meta.causation_id == caid
        assert meta.message_type == "CustomEvent"


class TestMessageSerialization:
    """Message.from_dict() and get_domain_data()."""

    def test_get_domain_data_delegates_to_payload(self) -> None:
        """Default get_domain_data() returns the same as _payload."""
        event = SimpleEvent()
        assert event.get_domain_data() == event.value

    def test_to_dict_includes_data_key(self) -> None:
        """to_dict() includes both 'payload' and 'data' keys."""
        event = SimpleEvent()
        d = event.to_dict()
        assert "payload" in d
        assert "data" in d
        assert d["payload"] == d["data"]

    def test_from_dict_calls_from_domain_data(self) -> None:
        """from_dict() on the base Message class raises NotImplementedError."""
        meta_dict = {
            "message_type": "EventWithoutFromPayloadFields",
            "message_id": str(uuid7()),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with pytest.raises(NotImplementedError):
            EventWithoutFromPayloadFields.from_dict({"metadata": meta_dict, "payload": {}})

    def test_from_dict_with_custom_from_domain_data(self) -> None:
        """A subclass that overrides _from_payload_fields can round-trip."""
        _uuid = uuid7()
        _ts = datetime.now(timezone.utc)
        meta_dict = {
            "message_type": "CustomEvent",
            "message_id": str(_uuid),
            "created_at": _ts.isoformat(),
            "correlation_id": str(uuid7()),
            "causation_id": str(uuid7()),
        }
        restored = CustomEvent.from_dict({"metadata": meta_dict, "payload": {"value": "hello"}})
        assert isinstance(restored, CustomEvent)
        assert restored.value["value"] == "hello"
        assert restored.metadata.message_id == _uuid


class TestMessageDataclassDecorator:
    """@event_dataclass, @command_dataclass, @query_dataclass."""

    def test_event_dataclass_get_domain_data(self) -> None:
        """Decorated event returns domain data from its fields."""

        @event_dataclass
        class OrderCreated(Event[dict[str, object]]):
            order_id: str
            customer_id: str
            total: float

            def __init__(
                self,
                order_id: str,
                customer_id: str,
                total: float,
                metadata: MessageMetadata | None = None,
            ) -> None:
                super().__init__(metadata)
                object.__setattr__(self, "order_id", order_id)
                object.__setattr__(self, "customer_id", customer_id)
                object.__setattr__(self, "total", total)

            @property
            def _payload(self) -> dict[str, object]:
                return {
                    "order_id": self.order_id,
                    "customer_id": self.customer_id,
                    "total": self.total,
                }

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        event = OrderCreated(order_id="O1", customer_id="C1", total=99.95)
        data = event.get_domain_data()
        assert data == {"order_id": "O1", "customer_id": "C1", "total": 99.95}

    def test_event_dataclass_to_dict_contains_data(self) -> None:
        """to_dict() on a decorated event includes both keys."""

        @event_dataclass
        class OrderCreated(Event[dict[str, object]]):
            order_id: str

            def __init__(self, order_id: str, metadata: MessageMetadata | None = None) -> None:
                super().__init__(metadata)
                object.__setattr__(self, "order_id", order_id)

            @property
            def _payload(self) -> dict[str, object]:
                return {"order_id": self.order_id}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        event = OrderCreated(order_id="O1")
        d = event.to_dict()
        assert "payload" in d
        assert "data" in d
        assert d["data"] == {"order_id": "O1"}

    def test_event_dataclass_from_dict_round_trip(self) -> None:
        """A decorated event round-trips through from_dict()."""

        @event_dataclass
        class OrderCreated(Event[dict[str, object]]):
            order_id: str
            total: float

            def __init__(
                self, order_id: str, total: float, metadata: MessageMetadata | None = None
            ) -> None:
                super().__init__(metadata)
                object.__setattr__(self, "order_id", order_id)
                object.__setattr__(self, "total", total)

            @property
            def _payload(self) -> dict[str, object]:
                return {"order_id": self.order_id, "total": self.total}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        original = OrderCreated(order_id="O1", total=99.95)
        d = original.to_dict()
        restored = cast(OrderCreated, OrderCreated.from_dict(d))
        assert isinstance(restored, OrderCreated)
        assert restored.order_id == "O1"
        assert restored.total == 99.95
        assert restored.metadata.message_id == original.metadata.message_id

    def test_event_dataclass_from_dict_without_payload(self) -> None:
        """from_dict() falls back to 'data' key when 'payload' is absent."""

        @event_dataclass
        class OrderCreated(Event[dict[str, object]]):
            order_id: str

            def __init__(self, order_id: str, metadata: MessageMetadata | None = None) -> None:
                super().__init__(metadata)
                object.__setattr__(self, "order_id", order_id)

            @property
            def _payload(self) -> dict[str, object]:
                return {"order_id": self.order_id}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        original = OrderCreated(order_id="O1")
        d = original.to_dict()
        del d["payload"]
        restored = cast(OrderCreated, OrderCreated.from_dict(d))
        assert restored.order_id == "O1"

    def test_command_dataclass_alias(self) -> None:
        """@command_dataclass is an alias for @message_dataclass."""

        @command_dataclass
        class CreateOrder(Event[dict[str, object]]):
            product: str
            quantity: int

            def __init__(
                self, product: str, quantity: int, metadata: MessageMetadata | None = None
            ) -> None:
                super().__init__(metadata)
                object.__setattr__(self, "product", product)
                object.__setattr__(self, "quantity", quantity)

            @property
            def _payload(self) -> dict[str, object]:
                return {"product": self.product, "quantity": self.quantity}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        cmd = CreateOrder(product="Widget", quantity=3)
        assert cmd.get_domain_data() == {"product": "Widget", "quantity": 3}

    def test_query_dataclass_alias(self) -> None:
        """@query_dataclass is an alias for @message_dataclass."""

        @query_dataclass
        class GetOrder(Event[dict[str, object]]):
            order_id: str

            def __init__(self, order_id: str, metadata: MessageMetadata | None = None) -> None:
                super().__init__(metadata)
                object.__setattr__(self, "order_id", order_id)

            @property
            def _payload(self) -> dict[str, object]:
                return {"order_id": self.order_id}

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        q = GetOrder(order_id="O1")
        assert q.get_domain_data() == {"order_id": "O1"}

    def test_metadata_excluded_from_domain_data(self) -> None:
        """Private and reserved fields are excluded from get_domain_data()."""

        @event_dataclass
        class OrderEvent(Event[dict[str, object]]):
            order_id: str

        evt: Event[dict[str, object]] = cast(Any, OrderEvent)(order_id="O1")
        data: dict[str, object] = evt.get_domain_data()
        assert data == {"order_id": "O1"}

    def test_decorated_instance_is_frozen_after_init(self) -> None:
        """Assigning to a field after construction raises FrozenInstanceError."""

        @event_dataclass
        class OrderEvent(Event[dict[str, object]]):
            order_id: str

        evt: Event[dict[str, object]] = cast(Any, OrderEvent)(order_id="O1")
        assert evt.get_domain_data() == {"order_id": "O1"}

        with pytest.raises(dataclasses.FrozenInstanceError):
            evt.order_id = "mutated"


class TestSerializableProtocol:
    """Verify structural protocol conformance for message types."""

    def test_message_metadata_is_serializable(self) -> None:
        """MessageMetadata satisfies the Serializable protocol structurally."""
        meta = MessageMetadata(message_type="Test")
        assert isinstance(meta.to_dict(), dict)
        assert hasattr(MessageMetadata, "from_dict")
