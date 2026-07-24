# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
from typing import Self

import pytest

from forging_blocks.domain.messages import Event, MessageMetadata
from forging_blocks.infrastructure import MessageBusEventPublisher
from tests.fixtures.fake_message_bus import FakeMessageBus


class FakeEvent(Event):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, str]:
        return {"foo": "bar"}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.integration
class TestMessageBusEventPublisher:
    """Integration tests for the MessageBusEventPublisher adapter."""

    @pytest.fixture
    def fake_bus(self) -> FakeMessageBus:
        return FakeMessageBus()

    @pytest.fixture
    def publisher(self, fake_bus: FakeMessageBus) -> MessageBusEventPublisher:
        return MessageBusEventPublisher(fake_bus)

    @pytest.fixture
    def event(self) -> FakeEvent:
        return FakeEvent()

    def test_init_when_called_then_stores_message_bus(self, fake_bus: FakeMessageBus) -> None:
        publisher = MessageBusEventPublisher(fake_bus)

        assert publisher._message_bus is fake_bus

    async def test_publish_when_called_then_delegates_to_message_bus_dispatch(
        self, publisher: MessageBusEventPublisher, event: FakeEvent, fake_bus: FakeMessageBus
    ) -> None:
        await publisher.publish(event)

        assert len(fake_bus.dispatched_messages) == 1
        assert fake_bus.dispatched_messages[0] is event

    def test_implements_event_publisher_port(self) -> None:
        """MessageBusEventPublisher satisfies the EventPublisherPort protocol."""
        assert hasattr(MessageBusEventPublisher, "publish")
