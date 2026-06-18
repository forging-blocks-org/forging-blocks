"""
Event Bus infrastructure.

This module provides the EventBus port and its in-memory implementation.
"""

from abc import ABC, abstractmethod
from typing import Callable, Type, TypeVar

from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event

EventHandler = Callable[[Event], None]
CommandHandler = Callable[[Command], None]

E = TypeVar("E", bound=Event)
C = TypeVar("C", bound=Command)


class EventBus(ABC):
    """
    EventBus port.

    The EventBus is responsible for publishing events and sending commands
    to their respective handlers. It follows the publish-subscribe pattern
    for events and the command pattern for commands.
    """

    @abstractmethod
    async def publish(self, event: Event) -> None:
        """
        Publish an event to all registered handlers.

        Args:
            event: The event to publish.
        """
        pass

    @abstractmethod
    async def send(self, command: Command) -> None:
        """
        Send a command to its handler.

        Args:
            command: The command to send.

        Raises:
            NoHandlerError: If no handler is registered for the command type.
        """
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[E], handler: EventHandler) -> None:
        """
        Subscribe a handler to an event type.

        Args:
            event_type: The type of event to subscribe to.
            handler: The handler function to call when the event is published.
        """
        pass

    @abstractmethod
    def register_command_handler(self, command_type: Type[C], handler: CommandHandler) -> None:
        """
        Register a handler for a command type.

        Args:
            command_type: The type of command to handle.
            handler: The handler function to call when the command is sent.
        """
        pass


class NoHandlerError(Exception):
    """
    Raised when no handler is registered for a command type.
    """

    pass
