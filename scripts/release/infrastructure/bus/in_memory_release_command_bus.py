from typing import Any, TypeAlias, cast

from forging_blocks.application.ports.inbound.message_handler_port import MessageHandlerPort
from forging_blocks.domain.messages.command import Command
from scripts.release.application.ports.outbound import ReleaseCommandBus

CommandSubscriberType: TypeAlias = dict[type[Command[Any]], MessageHandlerPort[Command[Any], None]]


class InMemoryReleaseCommandBus(ReleaseCommandBus[Command[Any]]):
    def __init__(self) -> None:
        self._subscribers: dict[type[Command[Any]], MessageHandlerPort[Command[Any], None]] = {}

    async def dispatch(self, message: Command[Any]) -> None:
        """Dispatch a message to the registered handler."""
        await self.send(message)

    async def register[CT: Command[Any]](
        self, command_type: type[CT], handler: MessageHandlerPort[CT, None]
    ) -> None:
        self._subscribers[command_type] = cast(MessageHandlerPort[Command[Any], None], handler)

    async def send(self, message: Command[Any]) -> None:
        handler = self._subscribers[type(message)]
        await handler.handle(message)
