"""Composite specification implementations for logical combinations."""

from typing import TypeVar

from .specification import Specification

T = TypeVar("T")


class AndSpecification[T](Specification[T]):
    """Logical AND of two specifications.

    Is satisfied when both constituent specifications are satisfied.
    """

    __slots__ = ("_left", "_right")

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Return ``True`` only if both specifications are satisfied."""
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class OrSpecification[T](Specification[T]):
    """Logical OR of two specifications.

    Is satisfied when at least one of the constituent specifications is satisfied.
    """

    __slots__ = ("_left", "_right")

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        """Return ``True`` if either specification is satisfied."""
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class NotSpecification[T](Specification[T]):
    """Logical negation of a specification.

    Is satisfied when the wrapped specification is not satisfied.
    """

    __slots__ = ("_spec",)

    def __init__(self, spec: Specification[T]) -> None:
        self._spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        """Return ``True`` if the wrapped specification is *not* satisfied."""
        return not self._spec.is_satisfied_by(candidate)
