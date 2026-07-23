"""Message-bus-backed QueryFetcherPort adapter.

Delegates query dispatch to an injected ``MessageBusPort``.
"""

from forging_blocks.application.ports.outbound.message_bus_port import MessageBusPort
from forging_blocks.application.ports.outbound.query_fetcher_port import QueryFetcherPort
from forging_blocks.domain.messages.query import Query


class MessageBusQueryFetcher[QueryPayloadType, QueryFetcherResult](
    QueryFetcherPort[QueryPayloadType, QueryFetcherResult]
):
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
