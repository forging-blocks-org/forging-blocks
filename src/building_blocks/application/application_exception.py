"""Application exception module.

Auto-generated minimal module docstring.
"""


class ApplicationException(Exception):
    """Base class for all application-specific exceptions.

    This exception should be used to indicate issues that occur within the
    application layer, such as validation failures, service errors, or other
    application-specific issues.

    It is intended to be a general-purpose exception for the application layer,
    allowing for more specific exceptions to be derived from it as needed.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
