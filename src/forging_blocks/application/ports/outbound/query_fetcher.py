"""Outbound port for asynchronously fetching query results.

QueryFetcher provides an application-layer abstraction for retrieving data
by dispatching query messages through a MessageBus. It supports CQRS-style
architectures where queries are processed independently of commands.

Responsibilities:
    - Forward queries to the message bus.
    - Return the result of the query execution.

Non-Responsibilities:
    - Define caching or projection logic.
    - Guarantee consistency between read and write models.
"""

from typing import TypeVar

from forging_blocks.application.ports.outbound.message_bus import MessageBus
from forging_blocks.domain.messages.query import Query
from forging_blocks.foundation.ports import OutboundPort

QueryFetcherResult = TypeVar("QueryFetcherResult", covariant=True)


class QueryFetcher(OutboundPort[Query, QueryFetcherResult]):
    """Outbound port for dispatching query messages.

    The QueryFetcher abstracts query execution through a MessageBus. It does
    not apply any interpretation to the returned data; shaping is the query
    handler’s responsibility.
    """

    def __init__(self, message_bus: MessageBus[Query, QueryFetcherResult]) -> None:
        self._message_bus = message_bus

    async def fetch(self, query: Query) -> QueryFetcherResult:
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
