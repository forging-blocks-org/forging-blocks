"""Error raised when a transaction operation fails."""

from forging_blocks.foundation.errors.error import Error


class TransactionError(Error[dict[str, object]]):
    """Error raised when a transaction operation fails."""

    pass
