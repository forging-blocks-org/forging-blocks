"""Error raised when a concurrency conflict is detected in the event store."""

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class ConcurrencyError(Error[dict[str, object]]):
    """Raised when a concurrency conflict is detected."""

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
