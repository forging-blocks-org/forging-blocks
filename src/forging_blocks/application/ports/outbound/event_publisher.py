"""Outbound port for asynchronously publishing domain events.

Defines the ``EventPublisherPort`` protocol for publishing domain events
to an external message bus or event broker.  Infrastructure implementations
determine durability, ordering, and delivery guarantees.

Responsibilities:
    - Publish domain events after domain changes occur.

Non-Responsibilities:
    - Persist events.
    - Guarantee ordering or durability.
"""

from typing import Protocol, runtime_checkable

from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.ports import OutboundPort


@runtime_checkable
class EventPublisherPort[EventPayloadType](
    OutboundPort[Event[EventPayloadType], None],
    Protocol,
):
    """Protocol for publishing domain events asynchronously.

    Any object with an async ``publish`` method that accepts an ``Event``
    satisfies this protocol — no inheritance required.
    """

    async def publish(self, event: Event[EventPayloadType]) -> None:
        """Publish a domain event.

        Args:
            event: The domain event to publish.
        """
        ...
