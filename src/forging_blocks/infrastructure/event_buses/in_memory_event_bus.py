"""In-memory implementation of the EventBusPort port.

Dispatches events to multiple registered handlers (fan-out) and
commands to a single registered handler.  Handlers are looked up
by the exact type of the message.
"""

from typing import Any, cast

from forging_blocks.application.errors.event_bus_error import EventBusError
from forging_blocks.application.ports.inbound.message_handler import (
    CommandHandler,
    EventHandler,
)
from forging_blocks.application.ports.outbound.event_bus import EventBusPort
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.result import Err, Ok, Result


class InMemoryEventBus[EventPayloadType, CommandPayloadType](
    EventBusPort[EventPayloadType, CommandPayloadType]
):
    """In-memory event bus with separate event/command dispatch.

    Attributes:
        _event_handlers: Per-event-type list of handlers.
        _command_handlers: Per-command-type single handler.
    """

    __slots__ = ("_command_handlers", "_event_handlers")

    def __init__(self) -> None:
        self._event_handlers: dict[type[Any], list[EventHandler[Any]]] = {}
        self._command_handlers: dict[type[Any], CommandHandler[Any]] = {}

    def register_handler(self, message_type: type[Any], handler: Any) -> None:
        """Register a handler for a message type.

        For event types, multiple handlers can be registered (fan-out).
        For command types, only one handler is allowed per type.

        Args:
            message_type: The message class to handle.
            handler: A handler instance.
        """
        if issubclass(message_type, Event):
            self._event_handlers.setdefault(cast(type[Any], message_type), []).append(handler)
        elif issubclass(message_type, Command):
            self._command_handlers[message_type] = handler

    async def publish(self, event: Event[EventPayloadType]) -> Result[None, EventBusError]:
        """Publish an event to all registered handlers.

        Args:
            event: The domain event.

        Returns:
            ``Ok(None)`` on success, or ``Err(EventBusError)`` if any
            handler raises.
        """
        handlers = self._event_handlers.get(type(event), [])
        for handler in handlers:
            try:
                await handler.handle(event)
            except Exception as exc:
                return Err(EventBusError(str(exc)))
        return Ok(None)

    async def send(self, command: Command[CommandPayloadType]) -> Result[None, EventBusError]:
        """Send a command to its registered handler.

        Args:
            command: The command.

        Returns:
            ``Ok(None)`` on success, or ``Err(EventBusError)`` if the
            handler raises or no handler is registered.
        """
        handler = self._command_handlers.get(type(command))
        if handler is None:
            return Err(EventBusError(f"No handler registered for {type(command).__name__}"))
        try:
            await handler.handle(command)
        except Exception as exc:
            return Err(EventBusError(str(exc)))
        return Ok(None)
