"""Event bus base class compliant with the application EventBusPort contract.

Defines the ``EventBusBase`` abstract interface for in-process message dispatch
with separate policies for events (multi-handler fan-out) and commands
(single-handler routing).
"""

from abc import ABC, abstractmethod

from forging_blocks.application.errors.event_bus_error import EventBusError
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.result import Result


class EventBusBase[EventPayloadType, CommandPayloadType, HandlerType](ABC):
    """Base class for event buses.

    Implementations handle:
      - Publishing events to one or more registered handlers.
      - Sending commands to a single registered handler.
      - Registering handlers for specific message types.
    """

    @abstractmethod
    async def publish(self, event: Event[EventPayloadType]) -> Result[None, EventBusError]:
        """Publish a domain event to all registered handlers.

        Args:
            event: The domain event to publish.

        Returns:
            A ``Result`` indicating success or an ``EventBusError``.

        """

    @abstractmethod
    async def send(self, command: Command[CommandPayloadType]) -> Result[None, EventBusError]:
        """Send a command to its registered handler.

        Args:
            command: The command to dispatch.

        Returns:
            A ``Result`` indicating success or an ``EventBusError``.

        """

    @abstractmethod
    def register_handler(
        self,
        message_type: type[Event[EventPayloadType]] | type[Command[CommandPayloadType]],
        handler: HandlerType,
    ) -> None:
        """Register a handler for the given message type.

        Args:
            message_type: The message class to handle.
            handler: A handler instance.

        """
