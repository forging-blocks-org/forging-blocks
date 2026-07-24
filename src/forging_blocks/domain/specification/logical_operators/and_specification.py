from forging_blocks.domain.specification.base import Specification
from forging_blocks.domain.specification.composable import ComposableSpecification


class AndSpecification[T](ComposableSpecification[T]):
    """Logical AND of two specifications.

    Satisfied if and only if both left and right specifications are satisfied.

    Inherits composition operators from ``ComposableSpecification`` so that the
    result of a conjunction is itself composable (e.g. ``(a & b) | c``).
    """

    __slots__ = ("_left_specification", "_right_specification")

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left_specification = left
        self._right_specification = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left_specification.is_satisfied_by(
            candidate
        ) and self._right_specification.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        return f"AndSpecification({self._left_specification!r}, {self._right_specification!r})"
