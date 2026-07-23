"""Module defining the base Query class for queries."""

from abc import abstractmethod

from forging_blocks.foundation.messages.message import Message


class Query[QueryPayloadType](Message[QueryPayloadType]):
    """Base class for all queries.

    Queries represent a request to retrieve data from the system.
    They are handled by query handlers and should not modify state.

    Queries are named in interrogative mood (e.g., GetOrder, FindCustomer,
    ListProducts).

    Example:
        ```python
        class GetOrder(Query[dict[str, object]]):
            def __init__(self, order_id: str):
                super().__init__()
                self._order_id = order_id

            @property
            def _payload(self) -> dict[str, object]:
                return {"order_id": self._order_id}
        ```

    """

    @property
    @abstractmethod
    def _payload(self) -> QueryPayloadType:
        """Return the query-specific payload data.

        Subclasses MUST implement this property to return the query-specific
        data.
        """
