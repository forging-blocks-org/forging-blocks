from typing import TypeAlias

from forging_blocks.application.ports.inbound.message_handler import CommandHandler
from forging_blocks.domain.messages.command import Command
from scripts.release.application.ports.outbound import ReleaseCommandBus

CommandSubscriberType: TypeAlias = dict[type[Command], CommandHandler]


class InMemoryReleaseCommandBus(ReleaseCommandBus):
    def __init__(self) -> None:
        self._subscribers: dict[type[Command], CommandHandler] = {}

    async def dispatch(self, message: Command) -> None:
        """Dispatch a message to the registered handler."""
        await self.send(message)

    async def register(
        self, command_type: type[Command], handler: CommandHandler
    ) -> None:
        self._subscribers[command_type] = handler

    async def send(self, message: Command) -> None:
        handler = self._subscribers[type(message)]
        await handler.handle(message)
