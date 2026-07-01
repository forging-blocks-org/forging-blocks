"""Outbound port for asynchronously publishing domain events.

This module defines an EventPublisherPort that sends domain events to an
external message bus or event broker. Infrastructure implementations
determine durability, ordering, and delivery guarantees.

Responsibilities:
    - Publish domain events after domain changes occur.
    - Forward events to a message bus.

Non-Responsibilities:
    - Persist events.
    - Guarantee ordering or durability.
"""

from forging_blocks.application.ports.outbound.message_bus import MessageBusPort
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.ports import OutboundPort


class EventPublisherPort[EventPayloadType](OutboundPort[Event[EventPayloadType], None]):
    """Outbound port for publishing domain events asynchronously.

    An EventPublisherPort provides an abstraction over event transport. Use cases
    or application services call it to publish domain events after state
    transitions. The underlying MessageBusPort determines the delivery semantics.
    """

    def __init__(self, message_bus: MessageBusPort[Event[EventPayloadType], None]) -> None:
        self._message_bus = message_bus

    async def publish(self, event: Event[EventPayloadType]) -> None:
        """Publish a domain event.

        Args:
            event: The domain event to publish.

        Notes:
            - Asynchronous and fire-and-forget.
            - Delivery reliability depends on the MessageBusPort implementation.
        """
        await self._message_bus.dispatch(event)
