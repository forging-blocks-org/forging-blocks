"""Error raised when no handler is registered for a command type."""

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class NoHandlerError(Error[dict[str, object]]):
    """Raised when no handler is registered for a command type."""

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
