"""Module for fetching queries via a message bus."""

from typing import Any

from building_blocks.application.ports.outbound.message_bus import MessageBus
from building_blocks.domain.messages.query import Query


class QueryFetcher:
    """Asynchronous outbound port for fetching queries.

    QueryFetcher is designed to retrieve data by dispatching query messages through a message bus.
    It is ideal for implementing the query side if you are applying a CQRS-like architecture.

    This implementation is composed with a MessageBus to delegate the actual message dispatching
    logic.
    """

    def __init__(self, message_bus: MessageBus) -> None:
        self._message_bus = message_bus

    async def fetch(self, query: Query) -> Any:
        """Fetch a query asynchronously.

        Args:
            query: The query to be fetched.

        Returns:
            The result of the query.
        """
        return await self._message_bus.dispatch(query)
