"""
In-memory implementation of the EventBus port.

This implementation stores handlers in memory and is suitable for testing
and development purposes.
"""

from collections import defaultdict
from typing import Callable, List, Type

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.infrastructure.event_bus import EventBus, NoHandlerError

EventHandler = Callable[[Event], None]
CommandHandler = Callable[[Command], None]


class InMemoryEventBus(EventBus):
    """
    In-memory implementation of the EventBus port.

    Stores event handlers and command handlers in dictionaries.
    """

    def __init__(self) -> None:
        self._event_handlers: dict[Type[Event], List[EventHandler]] = defaultdict(list)
        self._command_handlers: dict[Type[Command], CommandHandler] = {}

    async def publish(self, event: Event) -> None:
        """
        Publish an event to all registered handlers.

        Args:
            event: The event to publish.
        """
        handlers = self._event_handlers.get(type(event), [])
        for handler in handlers:
            await handler(event)

    async def send(self, command: Command) -> None:
        """
        Send a command to its handler.

        Args:
            command: The command to send.

        Raises:
            NoHandlerError: If no handler is registered for the command type.
        """
        handler = self._command_handlers.get(type(command))
        if handler is None:
            raise NoHandlerError(
                f"No handler registered for command type: {type(command).__name__}"
            )
        await handler(command)

    def subscribe(self, event_type: Type[Event], handler: EventHandler) -> None:
        """
        Subscribe a handler to an event type.

        Args:
            event_type: The type of event to subscribe to.
            handler: The handler function to call when the event is published.
        """
        self._event_handlers[event_type].append(handler)

    def register_command_handler(
        self, command_type: Type[Command], handler: CommandHandler
    ) -> None:
        """
        Register a handler for a command type.

        Args:
            command_type: The type of command to handle.
            handler: The handler function to call when the command is sent.
        """
        self._command_handlers[command_type] = handler
