"""Outbound port for asynchronously fetching query results.

Defines the ``QueryFetcherPort`` protocol for dispatching query messages
and returning their results.  Supports CQRS-style architectures where
queries are processed independently of commands.

Responsibilities:
    - Abstract query dispatch from transport details.

Non-Responsibilities:
    - Define caching or projection logic.
    - Guarantee consistency between read and write models.
"""

from typing import Protocol

from forging_blocks.foundation.messages.query import Query
from forging_blocks.foundation.ports import OutboundPort


class QueryFetcherPort[QueryPayloadType, QueryFetcherResult](
    OutboundPort[Query[QueryPayloadType], QueryFetcherResult],
    Protocol,
):
    """Protocol for dispatching query messages asynchronously.

    Any object with an async ``fetch`` method that accepts a ``Query`` and
    returns a result satisfies this protocol — no inheritance required.
    """

    async def fetch(self, query: Query[QueryPayloadType]) -> QueryFetcherResult:
        """Fetch the result of a query.

        Args:
            query: The query instance.

        Returns:
            Any result returned by the underlying query handler.
        """
        ...
