from typing import TypeAlias

from forging_blocks.application.ports.inbound.message_handler import CommandHandler
from forging_blocks.domain.messages.command import Command

from scripts.release.application.ports.outbound import ReleaseCommandBus


CommandSubscriberType: TypeAlias = dict[type[Command], CommandHandler]


class InMemoryReleaseCommandBus(ReleaseCommandBus):
    def __init__(self):
        self._subscribers = {}

    async def register(self, command_type: type[Command], handler: CommandHandler) -> None:
        self._subscribers[command_type] = handler

    async def send(self, message: Command) -> None:
        handler = self._subscribers[type(message)]

        await handler.handle(message)
