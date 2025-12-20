from forging_blocks.foundation import ErrorMessage, ValidationError


class InvalidReleaseBranchNameError(ValidationError):
    def __init__(self, value: str) -> None:
        super().__init__(
            ErrorMessage(
                f"Invalid release branch name '{value}'. "
                "Release branches must start with 'release/v<version>'."
            )
        )
