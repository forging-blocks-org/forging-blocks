"""NotCallablePredicateError module.

Defines the NotCallablePredicateError exception that is raised when a specification
predicate is not callable. This error is typically raised by ExpressionSpecification
when an invalid predicate is provided during initialization.
"""

from typing import Mapping

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class NotCallablePredicateError[MetadataType: Mapping[str, object]](Error[MetadataType]):
    """Exception raised when a specification predicate is not callable.

    This error is raised by ExpressionSpecification when the provided predicate
    argument is not a callable object. The error message includes the actual type
    of the predicate that was provided, helping developers identify and fix the issue.

    Attributes:
        message: Structured error message containing the type name of the invalid predicate.
        metadata: Optional metadata providing additional context about the error.
        context: Shortcut access to the metadata context dictionary.

    Example:
        >>> from forging_blocks.domain.specification import ExpressionSpecification
        >>> spec = ExpressionSpecification(123)  # Not callable
        Traceback (most recent call last):
            ...
        NotCallablePredicateError: predicate must be Callable and not int

    """

    def __init__(
        self,
        predicate: object,
    ) -> None:
        """Initialize the NotCallablePredicateError with the invalid predicate.

        Args:
            predicate: The object that was provided as a predicate but is not callable.
                The type name of this object will be included in the error message.

        """
        message = ErrorMessage(f"predicate must be Callable and not {type(predicate).__name__}")
        super().__init__(message)
