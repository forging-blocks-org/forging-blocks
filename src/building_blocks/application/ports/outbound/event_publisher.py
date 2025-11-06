"""Outbound port for publishing domain events asynchronously."""

from building_blocks.application.ports.outbound.message_bus import MessageBus
from building_blocks.domain.messages.event import Event


class EventPublisher:
    """Asynchronous outbound port for publishing events.

    This interface defines the contract for publishing domain events in a
    CQRS architecture. It is designed to be implemented by event bus or
    message broker services, allowing for asynchronous event handling and
    decoupling of components.
    Perfect for:
    - Event-driven architectures
    - Decoupling domain logic from event handling
    - Implementing event sourcing patterns
    - Integrating with message brokers or event buses.
    """

    def __init__(self, message_bus: MessageBus) -> None:
        self._message_bus = message_bus

    async def publish(self, event: Event) -> None:
        """Publish an event synchronously.

        Args:
            event: The domain event to be published.
        """
        await self._message_bus.dispatch(event)
