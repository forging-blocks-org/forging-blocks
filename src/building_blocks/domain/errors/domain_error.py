"""Domain error module.

Auto-generated minimal module docstring.
"""


class DomainError(Exception):
    """Base class for all domain-related exceptions.

    This exception should be used to indicate issues that occur within the
    domain layer, such as validation failures, business rule violations, or
    other domain-specific issues.

    It is intended to be a general-purpose exception for the domain layer,
    allowing for more specific exceptions to be derived from it as needed.
    """
