from forging_blocks.domain.specification.base import Specification
from forging_blocks.domain.specification.composable import ComposableSpecification


class OrSpecification[T](ComposableSpecification[T]):
    """Logical OR of two specifications.

    Satisfied if and only if at least one of left or right is satisfied.

    Inherits composition operators from ``ComposableSpecification`` so that the
    result of a disjunction is itself composable (e.g. ``(a | b) & c``).
    """

    __slots__ = ("_left_specification", "_right_specification")

    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left_specification = left
        self._right_specification = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left_specification.is_satisfied_by(
            candidate
        ) or self._right_specification.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        return f"OrSpecification({self._left_specification!r}, {self._right_specification!r})"
