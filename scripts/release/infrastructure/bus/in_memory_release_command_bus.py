from typing import Any, TypeAlias

from forging_blocks.application.ports.inbound.message_handler import CommandHandler
from forging_blocks.foundation.messages.command import Command
from scripts.release.application.ports.outbound import ReleaseCommandBus

CommandSubscriberType: TypeAlias = dict[type[Command[Any]], CommandHandler[Command[Any]]]


class InMemoryReleaseCommandBus(ReleaseCommandBus[Command[Any]]):
    def __init__(self) -> None:
        self._subscribers: dict[type[Command[Any]], CommandHandler[Command[Any]]] = {}

    async def dispatch(self, message: Command[Any]) -> None:
        """Dispatch a message to the registered handler."""
        await self.send(message)

    async def register[CT: Command[Any]](
        self, command_type: type[CT], handler: CommandHandler[CT]
    ) -> None:
        self._subscribers[command_type] = handler  # type: ignore[reportArgumentType]

    async def send(self, message: Command[Any]) -> None:
        handler = self._subscribers[type(message)]
        await handler.handle(message)
