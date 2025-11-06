from typing import Any

import pytest

from building_blocks.domain.messages.event import Event
from building_blocks.domain.messages.message import MessageMetadata


class PayloadNotImplementEvent(Event):
    pass


class FakeEvent(Event):
    def __init__(
        self,
        order_id: str,
        customer_id: str,
        total: float,
        metadata: MessageMetadata | None = None,
    ):
        super().__init__(metadata)
        self._order_id = order_id
        self._customer_id = customer_id
        self._total = total

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def total(self) -> float:
        return self._total

    @property
    def value(self) -> dict[str, Any]:
        return self._payload

    @property
    def _payload(self) -> dict[str, Any]:
        return {
            "order_id": self._order_id,
            "customer_id": self._customer_id,
            "total": self._total,
        }


class TestEvent:
    def test_inheritance_when_instantied_then_is_message(self):
        event = FakeEvent("order_123", "customer_456", 150.0)

        from building_blocks.domain.messages.message import Message

        assert isinstance(event, Message)
        assert isinstance(event, Event)

    def test_occured_at_when_called_then_returns_created_at(self):
        event = FakeEvent("order_123", "customer_456", 150.0)

        occurred_at = event.occurred_at

        assert occurred_at == event.created_at

    def test_constructor_when_not_implemented_then_raises_type_error(self):
        with pytest.raises(TypeError):
            _ = PayloadNotImplementEvent()  # type: ignore
