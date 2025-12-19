from forging_blocks.foundation import ErrorMessage, ValidationError


class InvalidReleasePullRequestError(ValidationError):
    def __init__(self, reason: str) -> None:
        super().__init__(ErrorMessage(reason))
