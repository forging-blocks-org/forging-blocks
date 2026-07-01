"""Outbound port for asynchronously fetching query results.

QueryFetcherPort provides an application-blocks abstraction for retrieving data
by dispatching query messages through a MessageBusPort. It supports CQRS-style
architectures where queries are processed independently of commands.

Responsibilities:
    - Forward queries to the message bus.
    - Return the result of the query execution.

Non-Responsibilities:
    - Define caching or projection logic.
    - Guarantee consistency between read and write models.
"""

from forging_blocks.application.ports.outbound.message_bus import MessageBusPort
from forging_blocks.foundation.messages.query import Query
from forging_blocks.foundation.ports import OutboundPort


class QueryFetcherPort[QueryPayloadType, QueryFetcherResult](
    OutboundPort[Query[QueryPayloadType], QueryFetcherResult],
):
    """Outbound port for dispatching query messages.

    The QueryFetcherPort abstracts query execution through a MessageBusPort. It does
    not apply any interpretation to the returned data; shaping is the query
    handler's responsibility.
    """

    def __init__(
        self, message_bus: MessageBusPort[Query[QueryPayloadType], QueryFetcherResult]
    ) -> None:
        self._message_bus = message_bus

    async def fetch(self, query: Query[QueryPayloadType]) -> QueryFetcherResult:
        """Fetch the result of a query.

        Args:
            query: The query instance.

        Returns:
            Any result returned by the underlying query handler.

        Notes:
            - Asynchronous execution.
            - Data shape is determined by the handler responsible for the query.
        """
        return await self._message_bus.dispatch(query)
