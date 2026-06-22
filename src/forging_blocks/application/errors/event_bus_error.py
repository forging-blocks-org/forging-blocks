"""Event bus error type for application-level operations."""

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class EventBusError(Error[dict[str, object]]):
    """Base error for event bus operations."""

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
