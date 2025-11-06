"""Module defining the base Query class for domain queries."""

from abc import ABC, abstractmethod
from typing import Any

from building_blocks.domain.messages.message import Message


class Query(Message, ABC):
    """Base class for all domain queries.

    Queries represent a request to retrieve data from the domain.
    They are handled by query handlers and should not modify state.

    Queries are named in interrogative mood (e.g., GetOrder, FindCustomer,
    listProducts).

    Example:
        >>> class GetOrder(Query):
        ...     def __init__(
        ...         self,
        ...         order_id: str,
        ...         metadata: MessageMetadata | None = None
        ...     ):
        ...         super().__init__(metadata)
        ...         self._order_id = order_id
        ...
        ...     @property
        ...     def order_id(self) -> str:
        ...         return self._order_id
        ...
        ...     @property
        ...     def payload(self) -> dict[str, Any]:
        ...         return {
        ...             "order_id": self._order_id
        ...         }
    """

    @property
    @abstractmethod
    def _payload(self) -> dict[str, Any]:
        """Get the domain-specific data carried by this query.

        Returns:
            dict[str, Any]: The query payload as a dictionary
        """
        pass
