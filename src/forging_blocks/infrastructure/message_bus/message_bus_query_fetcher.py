"""Message-bus-backed QueryFetcherPort adapter.

Delegates query dispatch to an injected ``MessageBusPort``.
"""

from forging_blocks.application.ports.outbound.message_bus import MessageBusPort
from forging_blocks.foundation.messages.query import Query


class MessageBusQueryFetcher[QueryPayloadType, QueryFetcherResult]:
    """Infrastructure adapter that fetches query results via a ``MessageBusPort``.

    Implements ``QueryFetcherPort`` by delegating ``fetch`` to
    ``MessageBusPort.dispatch``.
    """

    def __init__(
        self,
        message_bus: MessageBusPort[Query[QueryPayloadType], QueryFetcherResult],
    ) -> None:
        self._message_bus = message_bus

    async def fetch(self, query: Query[QueryPayloadType]) -> QueryFetcherResult:
        """Fetch a query result via the message bus."""
        return await self._message_bus.dispatch(query)
