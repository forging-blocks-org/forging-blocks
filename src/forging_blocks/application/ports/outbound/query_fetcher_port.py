"""Outbound port for asynchronously fetching query results.

Defines the ``QueryFetcherPort`` ABC for dispatching query messages
and returning their results.  Supports CQRS-style architectures where
queries are processed independently of commands.

Responsibilities:
    - Abstract query dispatch from transport details.

Non-Responsibilities:
    - Define caching or projection logic.
    - Guarantee consistency between read and write models.
"""

from abc import abstractmethod

from forging_blocks.domain.messages.query import Query
from forging_blocks.foundation.ports import OutboundPort


class QueryFetcherPort[QueryPayloadType, QueryFetcherResult](
    OutboundPort,
):
    """ABC for dispatching query messages asynchronously.

    Infrastructure implementations determine delivery semantics.
    """

    @abstractmethod
    async def fetch(self, query: Query[QueryPayloadType]) -> QueryFetcherResult:
        """Fetch the result of a query.

        Args:
            query: The query instance.

        Returns:
            Any result returned by the underlying query handler.

        """
        ...
