"""Outbound port for asynchronously publishing domain events.

This module defines an EventPublisher that sends domain events to an
external message bus or event broker. Infrastructure implementations
determine durability, ordering, and delivery guarantees.

Responsibilities:
    - Publish domain events after domain changes occur.
    - Forward events to a message bus.

Non-Responsibilities:
    - Persist events.
    - Guarantee ordering or durability.
"""

from forging_blocks.application.ports.outbound.message_bus import MessageBus
from forging_blocks.domain.messages.event import Event
from forging_blocks.foundation.ports import OutboundPort


class EventPublisher(OutboundPort[Event, None]):
    """Outbound port for publishing domain events asynchronously.

    An EventPublisher provides an abstraction over event transport. Use cases
    or application services call it to publish domain events after state
    transitions. The underlying MessageBus determines the delivery semantics.
    """

    def __init__(self, message_bus: MessageBus[Event, None]) -> None:
        self._message_bus = message_bus

    async def publish(self, event: Event) -> None:
        """Publish a domain event.

        Args:
            event: The domain event to publish.

        Notes:
            - Asynchronous and fire-and-forget.
            - Delivery reliability depends on the MessageBus implementation.
        """
        await self._message_bus.dispatch(event)
