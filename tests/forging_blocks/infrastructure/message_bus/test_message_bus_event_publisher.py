# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Self
from unittest.mock import AsyncMock, MagicMock

import pytest

from forging_blocks.application import EventPublisherPort, MessageBusPort
from forging_blocks.foundation.messages import Event, MessageMetadata
from forging_blocks.infrastructure import MessageBusEventPublisher


class FakeEvent(Event):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, str]:
        return {"foo": "bar"}

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.integration
class TestMessageBusEventPublisher:
    """Integration tests for the MessageBusEventPublisher adapter."""

    def test_init_when_called_then_stores_message_bus(self) -> None:
        bus = MagicMock(spec=MessageBusPort)

        publisher = MessageBusEventPublisher(bus)

        assert publisher._message_bus is bus

    async def test_publish_when_called_then_delegates_to_message_bus_dispatch(self) -> None:
        bus = MagicMock(spec=MessageBusPort)
        bus.dispatch = AsyncMock()
        publisher = MessageBusEventPublisher(bus)
        event = FakeEvent()

        await publisher.publish(event)

        bus.dispatch.assert_awaited_once_with(event)

    async def test_implements_event_publisher_port(self) -> None:
        """MessageBusEventPublisher satisfies the EventPublisherPort protocol."""
        bus = MagicMock(spec=MessageBusPort)
        publisher = MessageBusEventPublisher(bus)

        assert isinstance(publisher, EventPublisherPort)
