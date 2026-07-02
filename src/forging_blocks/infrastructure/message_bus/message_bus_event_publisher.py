"""Message-bus-backed EventPublisherPort adapter.

Delegates event publishing to an injected ``MessageBusPort``.
"""

from forging_blocks.application.ports.outbound.event_publisher_port import EventPublisherPort
from forging_blocks.application.ports.outbound.message_bus_port import MessageBusPort
from forging_blocks.foundation.messages.event import Event


class MessageBusEventPublisher[EventPayloadType](EventPublisherPort[EventPayloadType]):
    """Infrastructure adapter that publishes events via a ``MessageBusPort``.

    Implements ``EventPublisherPort`` by delegating ``publish`` to
    ``MessageBusPort.dispatch``.
    """

    def __init__(self, message_bus: MessageBusPort[Event[EventPayloadType], None]) -> None:
        self._message_bus = message_bus

    async def publish(self, event: Event[EventPayloadType]) -> None:
        """Publish a domain event via the message bus."""
        await self._message_bus.dispatch(event)
