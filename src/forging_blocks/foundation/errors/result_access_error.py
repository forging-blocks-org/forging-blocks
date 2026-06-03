from forging_blocks.foundation.errors.base import Error
from forging_blocks.foundation.errors.core import ErrorMessage


class ResultAccessError(Error):
    """Exception raised when trying to access value or err from an inappropriate Result variant."""

    def __init__(self, message: ErrorMessage | None = None) -> None:
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
