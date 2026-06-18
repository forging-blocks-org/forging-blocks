"""
Event Store infrastructure.

This module provides the EventStore port and its in-memory implementation.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class EventStore(ABC):
    """
    EventStore port.

    The EventStore is responsible for persisting and retrieving events
    for aggregate roots. It follows the Event Sourcing pattern.
    """

    @abstractmethod
    async def save_events(
        self, aggregate_id: str, events: List[dict], expected_version: Optional[int] = None
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
    ) -> List[dict]:
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
    async def get_snapshot(self, aggregate_id: str, version: int) -> Optional[dict]:
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
    async def save_snapshot(self, aggregate_id: str, version: int, snapshot: dict) -> None:
        """
        Save a snapshot of an aggregate.

        Args:
            aggregate_id: The unique identifier of the aggregate.
            version: The version of the snapshot.
            snapshot: The snapshot data.
        """
        pass


class ConcurrencyError(Exception):
    """
    Raised when a concurrency conflict is detected.
    """

    pass
