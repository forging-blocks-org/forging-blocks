from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.validation_error import ValidationError


class InvalidReleaseBranchNameError(ValidationError):
    def __init__(self) -> None:
        message = ErrorMessage("Release branch must follow 'release/vX.Y.Z'")
        super().__init__(message)
