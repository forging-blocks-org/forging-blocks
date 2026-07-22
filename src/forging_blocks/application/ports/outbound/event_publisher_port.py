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

from abc import abstractmethod

from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.ports import OutboundPort


class EventPublisherPort[EventPayloadType](
    OutboundPort,
):
    """ABC for publishing domain events asynchronously.

    Infrastructure implementations must explicitly inherit this class.
    """

    @abstractmethod
    async def publish(self, event: Event[EventPayloadType]) -> None:
        """Publish a domain event.

        Args:
            event: The domain event to publish.

        """
