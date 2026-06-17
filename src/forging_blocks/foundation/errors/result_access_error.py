"""Errors raised when accessing Result.value or Result.error on the wrong variant"""

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class ResultAccessError(Error[dict[str, object]]):
    """Exception raised when trying to access value or err from an inappropriate Result variant."""

    def __init__(self, message: ErrorMessage | None = None) -> None:
        """Initialise with an optional custom error message.

        Args:
            message: Optional `ErrorMessage` describing the invalid
                access. Defaults to a generic message when not provided.
        """
        message = message or ErrorMessage("Invalid access on Result type.")
        super().__init__(message)

    @classmethod
    def cannot_access_value(cls) -> "ResultAccessError":
        """Create an error for accessing value from an Err Result."""
        return cls(ErrorMessage("Cannot access value from an Err Result."))

    @classmethod
    def cannot_access_error(cls) -> "ResultAccessError":
        """Create an error for accessing error from an Ok Result."""
        return cls(ErrorMessage("Cannot access error from an Ok Result."))
