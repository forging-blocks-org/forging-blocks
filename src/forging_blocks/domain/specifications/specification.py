"""Base ``Specification`` class and ``ExpressionSpecification``.

Provides the fundamental building block for the Specification pattern,
allowing domain-level query predicates to be composed logically.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """Base class for all specifications.

    A specification is a predicate that determines whether a candidate
    object satisfies a set of criteria. Specifications can be combined
    using logical operators (``&``, ``|``, ``~``).
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check whether the candidate satisfies this specification.

        Args:
            candidate: The object to evaluate.

        Returns:
            ``True`` if the candidate satisfies the specification.
        """
        ...

    def and_(self, other: "Specification[T]") -> "Specification[T]":
        """Return a specification that is the logical AND of this and *other*."""
        from .composite import AndSpecification  # fmt: skip

        return AndSpecification(self, other)

    def or_(self, other: "Specification[T]") -> "Specification[T]":
        """Return a specification that is the logical OR of this and *other*."""
        from .composite import OrSpecification  # fmt: skip

        return OrSpecification(self, other)

    def not_(self) -> "Specification[T]":
        """Return a specification that is the logical negation of this."""
        from .composite import NotSpecification  # fmt: skip

        return NotSpecification(self)

    def __and__(self, other: "Specification[T]") -> "Specification[T]":
        return self.and_(other)

    def __or__(self, other: "Specification[T]") -> "Specification[T]":
        return self.or_(other)

    def __invert__(self) -> "Specification[T]":
        return self.not_()


class ExpressionSpecification[T](Specification[T]):
    """A specification defined by a callable expression.

    Useful for inline predicates without creating a dedicated subclass.

    Args:
        expression: A callable that takes a candidate and returns a bool.
        description: Optional human-readable description of the predicate.
    """

    __slots__ = ("_expression", "_description")

    def __init__(self, expression: Callable[[T], bool], description: str = "") -> None:
        self._expression = expression
        self._description = description

    def is_satisfied_by(self, candidate: T) -> bool:
        """Evaluate the expression against the candidate."""
        return self._expression(candidate)

    def __repr__(self) -> str:
        desc = self._description or self._expression.__name__
        return f"ExpressionSpecification({desc})"
