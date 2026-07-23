"""Tests for message decorators and frozen instance behavior."""

import dataclasses
from typing import Any, cast

import pytest

from forging_blocks.foundation.messages.decorators import (
    command_dataclass,
    event_dataclass,
    query_dataclass,
)
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.message import MessageMetadata


class TestMessageDataclassDecorator:
    """@event_dataclass, @command_dataclass, @query_dataclass."""

    def test_event_dataclass_produces_payload_from_fields(self) -> None:
        """Decorated event _payload reflects its fields."""

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
        assert event._payload == {
            "order_id": "O1",
            "customer_id": "C1",
            "total": 99.95,
        }

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
        assert cmd._payload == {"product": "Widget", "quantity": 3}

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
        assert q._payload == {"order_id": "O1"}

    def test_metadata_excluded_from_payload(self) -> None:
        """Private and reserved fields are excluded from decorator-generated payload."""

        @event_dataclass
        class OrderEvent(Event[dict[str, object]]):
            order_id: str

        evt: Event[dict[str, object]] = cast(Any, OrderEvent)(order_id="O1")
        assert evt._payload == {"order_id": "O1"}

    def test_decorated_instance_is_frozen_after_init(self) -> None:
        """Assigning to a field after construction raises FrozenInstanceError."""

        @event_dataclass
        class OrderEvent(Event[dict[str, object]]):
            order_id: str

        evt: Event[dict[str, object]] = cast(Any, OrderEvent)(order_id="O1")
        assert evt._payload == {"order_id": "O1"}

        with pytest.raises(dataclasses.FrozenInstanceError):
            cast(Any, evt).order_id = "mutated"
