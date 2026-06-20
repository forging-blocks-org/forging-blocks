"""
Event Bus infrastructure.

This module provides the EventBus port and its in-memory implementation.
"""

from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Any, Callable, Type, TypeVar

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event

EventHandler = Callable[[Event[Any]], Awaitable[None]]
CommandHandler = Callable[[Command[Any]], Awaitable[None]]

E = TypeVar("E", bound=Event[Any])
C = TypeVar("C", bound=Command[Any])


class EventBus(ABC):
    """
    EventBus port.

    The EventBus is responsible for publishing events and sending commands
    to their respective handlers. It follows the publish-subscribe pattern
    for events and the command pattern for commands.
    """

    @abstractmethod
    async def publish(self, event: Event[Any]) -> None:
        """
        Publish an event to all registered handlers.

        Args:
            event: The event to publish.
        """
        pass

    @abstractmethod
    async def send(self, command: Command[Any]) -> None:
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


class NoHandlerError(Error[dict[str, object]]):
    """
    Raised when no handler is registered for a command type.
    """

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
