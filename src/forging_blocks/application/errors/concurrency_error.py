"""Concurrency error for optimistic concurrency failures in event stores."""

from uuid import UUID

from forging_blocks.application.errors.event_store_error import EventStoreError


class ConcurrencyError(EventStoreError):
    """Raised when an optimistic concurrency check fails.

    Attributes:
        aggregate_id: The aggregate that experienced the conflict.
        expected_version: The version the caller expected.
        actual_version: The version currently stored.

    """

    def __init__(self, aggregate_id: UUID, expected_version: int, actual_version: int) -> None:
        self.aggregate_id = aggregate_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict for aggregate {aggregate_id}: "
            f"expected version {expected_version}, actual {actual_version}"
        )
