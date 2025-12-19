from forging_blocks.foundation import ErrorMessage, ValidationError


class InvalidPullRequestTitleError(ValidationError):
    def __init__(self, min_length: int, max_length: int) -> None:
        error_message = ErrorMessage(
            f"PullRequestTitle length have to be between  {min_length} and {max_length}."
        )
        super().__init__(error_message)
