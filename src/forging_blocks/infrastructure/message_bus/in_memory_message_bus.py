"""In-memory message bus implementation for intra-process message routing.

Provides a simple synchronous dispatch mechanism that routes messages
to registered handlers based on message type.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar

from forging_blocks.application.ports.outbound.message_bus import MessageBus
from forging_blocks.foundation.messages.message import Message

MessageType = TypeVar("MessageType", bound=Message, contravariant=True)
MessageBusResultType = TypeVar("MessageBusResultType", covariant=True)


class InMemoryMessageBus(
    Generic[MessageType, MessageBusResultType],
    MessageBus[MessageType, MessageBusResultType],
):
    """In-memory message bus that routes messages to registered handlers.

    Handlers are registered by message type and invoked directly when a
    message of that type is dispatched. Suitable for testing, prototyping,
    and simple intra-process communication.

    Usage::

        bus = InMemoryMessageBus[Command, None]()
        bus.register(MyCommand, my_handler)
        await bus.dispatch(MyCommand())
    """

    __slots__ = ("_handlers",)

    def __init__(self) -> None:
        """Initialize the message bus with an empty handler registry."""
        self._handlers: dict[type[Message], Callable[[Any], Any]] = {}

    def register(self, message_type: type[Message], handler: Callable[[Any], Any]) -> None:
        """Register a handler for a specific message type.

        Args:
            message_type: The message type to handle.
            handler: A callable that processes the message. It should accept
                a message instance and return the appropriate result type.

        Raises:
            ValueError: If the message type is already registered.
        """
        if message_type in self._handlers:
            raise ValueError(
                f"Handler already registered for message type '{message_type.__name__}'."
            )
        self._handlers[message_type] = handler

    async def dispatch(self, message: MessageType) -> MessageBusResultType:
        """Dispatch a message to the registered handler.

        Args:
            message: The message instance to dispatch.

        Returns:
            The result from the handler.

        Raises:
            KeyError: If no handler is registered for the message type.
        """
        handler = self._handlers[type(message)]
        result = handler(message)
        return result
