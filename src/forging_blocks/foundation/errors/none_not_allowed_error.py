"""Error indicating that a None value was provided where it is not allowed."""

from forging_blocks.foundation.errors.error import Error


class NoneNotAllowedError(Error[dict[str, object]]):
    """Error indicating that a None value was provided where it is not allowed."""
