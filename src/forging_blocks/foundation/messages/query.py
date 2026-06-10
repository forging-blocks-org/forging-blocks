"""Module defining the base Query class for domain queries."""

from abc import abstractmethod
from typing import Any

from forging_blocks.foundation.messages.message import Message


class Query(Message[Any]):
    """Base class for all domain queries.

    Queries represent a request to retrieve data from the domain.
    They are handled by query handlers and should not modify state.

    Queries are named in interrogative mood (e.g., GetOrder, FindCustomer,
    ListProducts).

    Example:
        ```python
        class GetOrder(Query):
            def __init__(self, order_id: str):
                super().__init__()
                self._order_id = order_id

            @property
            def _payload(self) -> dict[str, Any]:
                return {"order_id": self._order_id}
        ```
    """

    @property
    @abstractmethod
    def _payload(self) -> dict[str, Any]: ...
