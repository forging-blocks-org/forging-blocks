"""Module defining the base Query class for queries."""

from abc import abstractmethod

from forging_blocks.domain.messages.message import Message


class Query[QueryPayloadType](Message[QueryPayloadType]):
    """Base class for all queries.

    Queries represent a request to retrieve data from the system.
    They are handled by query handlers and should not modify state.

    Queries are named in interrogative mood (e.g., GetOrder, FindCustomer,
    ListProducts).

    Example:
        ```python
        from forging_blocks.domain.messages.decorators import query_dataclass


        @query_dataclass
        class GetOrder:
            order_id: str


        query = GetOrder(order_id="order-1")

        assert isinstance(query, Query)
        assert query.get_payload_fields() == {"order_id": "order-1"}
        assert query.message_id == query.metadata.message_id
        ```

    """

    @property
    @abstractmethod
    def _payload(self) -> QueryPayloadType:
        """Return the query-specific payload data.

        Subclasses MUST implement this property to return the query-specific
        data.
        """
