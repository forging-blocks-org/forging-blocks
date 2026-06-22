"""Event store error type for application-level operations."""

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class EventStoreError(Error[dict[str, object]]):
    """Base error for event store operations."""

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
