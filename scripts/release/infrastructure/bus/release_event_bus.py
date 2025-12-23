from forging_blocks.application.ports.inbound.message_handler import MessageHandler
from forging_blocks.domain.messages.message import Message
from scripts.release.application.ports.outbound import ReleaseMessageBus


class InMemoryReleaseEventBus(ReleaseMessageBus):
    def __init__(self):
        self._subscribers: list[MessageHandler] = []

    def subscribe(self, handler: MessageHandler):
        self._subscribers.append(handler)

    async def publish(self, message: Message):
        for handler in self._subscribers:
            await handler.handle(message)
