from typing import Any

from building_blocks.application.ports.outbound.message_bus import MessageBus
from building_blocks.domain.messages.query import Query


class QueryFetcher:
    def __init__(self, message_bus: MessageBus) -> None:
        self._message_bus = message_bus

    async def fetch(self, query: Query) -> Any:
        return await self._message_bus.dispatch(query)
