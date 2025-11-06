"""Outbound port for a message bus."""

from typing import Generic, Protocol, TypeVar

from building_blocks.application.ports.inbound.message_handler import MessageHandler
from building_blocks.domain.messages.message import Message

TResponse = TypeVar("TResponse", covariant=True)


class MessageBus(Protocol, Generic[TResponse]):
    """Asynchronous outbound port for a message bus."""

    async def dispatch(self, message: Message) -> TResponse:
        """Dispatch a message asynchronously."""
        ...

    async def register_handler(self, handler: MessageHandler) -> None:
        """Register a message handler asynchronously."""
        ...
