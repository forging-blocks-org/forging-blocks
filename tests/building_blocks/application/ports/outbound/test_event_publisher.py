from unittest.mock import AsyncMock, MagicMock

from pytest import fixture

from building_blocks.application.ports.outbound.event_publisher import EventPublisher
from building_blocks.application.ports.outbound.message_bus import MessageBus
from building_blocks.domain.messages.event import Event


class FakeEvent(Event):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, str]:
        return {"foo": "bar"}


class TestEventPublisher:
    @fixture
    def message_bus(self) -> MagicMock:
        bus = MagicMock(spec=MessageBus)
        bus.dispatch = AsyncMock()

        return bus

    def test_init_when_called_then_set_message_bus(self, message_bus: MagicMock) -> None:
        publisher = EventPublisher(message_bus)

        assert publisher._message_bus == message_bus

    async def test_publish_when_called_then_call_message_bus_dispatch_with_given_event(
        self, message_bus: MagicMock
    ) -> None:
        publisher = EventPublisher(message_bus)
        event = FakeEvent()

        await publisher.publish(event)

        message_bus.dispatch.assert_awaited_with(event)
