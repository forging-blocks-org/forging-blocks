from forging_blocks.foundation import ErrorMessage, ValidationError


class InvalidReleaseLevelError(ValidationError):
    def __init__(self, value: str) -> None:
        super().__init__(
            ErrorMessage(
                f"Invalid release level '{value}'. Allowed values: patch, minor, major."
            )
        )
