from forging_blocks.application.ports.inbound.message_handler import EventHandler
from forging_blocks.domain.messages.event import Event
from forging_blocks.foundation.ports import OutboundPort


class ReleaseMessageBus(OutboundPort):
    """
    Outbound port for registering message handlers and publishing release-related events.
    A ReleaseEventBus routes messages to their respective handlers and
    publishes domain event asynchronously.
    """

    async def register(self, message: Event, handler: EventHandler) -> None:
        """Register a message handler for a specific message type.
        Args:
            message: The message type to handle.
            handler: The handler responsible for processing the message.
        Notes:
            - Handlers should be asynchronous.
            - Registration is typically done at application startup.
        """
        ...

    async def publish(self, event: Event) -> None:
        """Publish a release-related domain event.

        Args:
            event: The domain event to publish.
        Notes:
            - Asynchronous and fire-and-forget.
            - Delivery reliability depends on the EventBus implementation.
        """
        ...
