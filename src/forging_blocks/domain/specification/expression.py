"""Expression-backed specification implementation.

Wraps a callable predicate. Inherits composition from ComposableSpecification.
"""

from collections.abc import Callable

from forging_blocks.foundation.errors.not_callable_predicate_error import NotCallablePredicateError

from .composable import ComposableSpecification


class ExpressionSpecification[T](ComposableSpecification[T]):
    """Specification defined by a callable predicate.

    Wraps a user-provided function that returns True/False.
    Composition operators are inherited from ComposableSpecification—
    do NOT reimplement them here.

    Example:
        >>> is_active = ExpressionSpecification(
        ...     lambda user: user.is_active, description="is_active"
        ... )
        >>> is_admin = ExpressionSpecification(
        ...     lambda user: user.role == "admin", description="is_admin"
        ... )
        >>> active_admin = is_active & is_admin  # Uses inherited operator

    """

    __slots__ = ("_predicate", "_description")

    def __init__(
        self,
        predicate: Callable[[T], bool],
        description: str = "",
    ) -> None:
        """Initialize the expression specification.

        Args:
            predicate: A callable that accepts a candidate and returns bool.
            description: Optional human-readable label for repr/debugging.

        Raises:
            NotCallablePredicateError: If predicate is not callable.

        """
        if not callable(predicate):
            raise NotCallablePredicateError(predicate)

        self._predicate = predicate
        self._description = description

    def is_satisfied_by(self, candidate: T) -> bool:
        """Evaluate the predicate against the candidate.

        Args:
            candidate: The object to test.

        Returns:
            The result of calling self._predicate(candidate).

        """
        return self._predicate(candidate)

    def __repr__(self) -> str:
        """Return a string representation for debugging.

        Uses the description if provided, otherwise extracts the function name.
        """
        if self._description:
            return f"ExpressionSpecification({self._description!r})"

        predicate_name = getattr(self._predicate, "__name__", "anonymous_predicate")
        return f"ExpressionSpecification({predicate_name})"
