"""Event bus port for publishing events and sending commands.

Defines the ``EventBusPort`` protocol for in-process message dispatch
with separate policies for events (multi-handler fan-out) and commands
(single-handler routing).
"""

from typing import Protocol

from forging_blocks.application.errors.event_bus_error import EventBusError
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.result import Result


class EventBusPort[EventPayloadType, CommandPayloadType](Protocol):
    """Protocol for event buses that publish events and send commands.

    Implementations handle:
      - Publishing events to one or more registered handlers.
      - Sending commands to a single registered handler.
      - Registering handlers for specific message types.
    """

    async def publish(self, event: Event[EventPayloadType]) -> Result[None, EventBusError]:
        """Publish a domain event to all registered handlers.

        Args:
            event: The domain event to publish.

        Returns:
            A ``Result`` indicating success or an ``EventBusError``.
        """
        ...

    async def send(self, command: Command[CommandPayloadType]) -> Result[None, EventBusError]:
        """Send a command to its registered handler.

        Args:
            command: The command to dispatch.

        Returns:
            A ``Result`` indicating success or an ``EventBusError``.
        """
        ...

    def register_handler(
        self,
        message_type: type[Event[object]] | type[Command[object]],
        handler: object,
    ) -> None:
        """Register a handler for the given message type.

        Args:
            message_type: The message class to handle.
            handler: A handler instance (``EventHandler`` or ``CommandHandler``).
        """
        ...
