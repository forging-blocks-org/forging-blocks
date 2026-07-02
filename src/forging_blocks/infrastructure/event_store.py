"""
Event Store infrastructure.

This module provides the EventStorePort port and its in-memory implementation.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class EventStorePort(ABC):
    """
    EventStorePort port.

    The EventStorePort is responsible for persisting and retrieving events
    for aggregate roots. It follows the Event Sourcing pattern.
    """

    @abstractmethod
    async def save_events(
        self,
        aggregate_id: str,
        events: List[dict[str, Any]],
        expected_version: Optional[int] = None,
    ) -> None:
        """
        Save a list of events for an aggregate.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            events: The list of events to save.
            expected_version: The expected version of the aggregate.

        Raises:
            ConcurrencyError: If the expected version does not match the current version.
        """
        pass

    @abstractmethod
    async def get_events(
        self,
        aggregate_id: str,
        from_version: Optional[int] = None,
        to_version: Optional[int] = None,
    ) -> list[dict[str, object]]:
        """
        Retrieve events for an aggregate.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            from_version: The starting version (inclusive).
            to_version: The ending version (inclusive).

        Returns:
            A list of events.
        """
        pass

    @abstractmethod
    async def get_snapshot(self, aggregate_id: str, version: int) -> dict[str, object] | None:
        """
        Retrieve a snapshot of an aggregate at a specific version.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            version: The version of the snapshot.

        Returns:
            The snapshot data, or None if not found.
        """
        pass

    @abstractmethod
    async def save_snapshot(
        self, aggregate_id: str, version: int, snapshot: dict[str, object]
    ) -> None:
        """
        Save a snapshot of an aggregate.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            version: The version of the snapshot.
            snapshot: The snapshot data.
        """
        pass


class ConcurrencyError(Error[dict[str, object]]):
    """
    Raised when a concurrency conflict is detected.
    """

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
