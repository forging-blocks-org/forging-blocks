"""Event bus port for publishing events and sending commands.

Defines the ``EventBusPort`` contract for in-process message dispatch
with separate policies for events (multi-handler fan-out) and commands
(single-handler routing).
"""

from abc import abstractmethod

from forging_blocks.application.errors.event_bus_error import EventBusError
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.ports import OutboundPort
from forging_blocks.foundation.result import Result


class EventBusPort[EventPayloadType, CommandPayloadType, HandlerType](
    OutboundPort,
):
    """Abstract base class for event buses that publish events and send commands.

    Responsibilities:
        - Publish domain events to all registered handlers (fan-out).
        - Route commands to a single registered handler.
        - Manage handler registration and lookup by message type.

    Non-Responsibilities:
        - Guarantee delivery or implement transactional outbox.
        - Persist messages or provide replay capabilities.
        - Manage subscriptions, topics, or routing rules — those belong
          to infrastructure.
    """

    @abstractmethod
    async def publish(self, event: Event[EventPayloadType]) -> Result[None, EventBusError]:
        """Publish a domain event to all registered handlers.

        Args:
            event: The domain event to publish.

        Returns:
            A ``Result`` indicating success or an ``EventBusError``.

        """
        ...

    @abstractmethod
    async def send(self, command: Command[CommandPayloadType]) -> Result[None, EventBusError]:
        """Send a command to its registered handler.

        Args:
            command: The command to dispatch.

        Returns:
            A ``Result`` indicating success or an ``EventBusError``.

        """
        ...

    @abstractmethod
    def register_handler(
        self,
        message_type: type[Event[EventPayloadType]] | type[Command[CommandPayloadType]],
        handler: HandlerType,
    ) -> None:
        """Register a handler for the given message type.

        Args:
            message_type: The message class to handle.
            handler: A handler instance implementing the handler contract.

        """
