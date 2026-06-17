from forging_blocks.foundation.errors.error import Error


class UnitOfWorkError(Error[dict[str, object]]):
    """Error raised when a Unit of Work operation fails."""

    pass
