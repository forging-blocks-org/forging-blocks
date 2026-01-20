from typing import Any

from forging_blocks.foundation.errors import ErrorMessage, ValidationError


class InvalidPullRequestIdError(ValidationError):
    def __init__(self, pull_request_id: Any) -> None:
        super().__init__(
            ErrorMessage(
                f"Invalid pull request ID: {pull_request_id}. It must be a positive integer."
            )
        )
