from forging_blocks.foundation.specification.base import Specification
from forging_blocks.foundation.specification.composable import ComposableSpecification


class NotSpecification[T](ComposableSpecification[T]):
    """Logical NOT of a specification.

    Satisfied if and only if the wrapped specification is NOT satisfied.

    Inherits composition operators from ``ComposableSpecification`` so that the
    result of a negation is itself composable (e.g. ``(~a) & b``).
    """

    __slots__ = ("_wrapped_specification",)

    def __init__(self, wrapped: Specification[T]) -> None:
        self._wrapped_specification = wrapped

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._wrapped_specification.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        return f"NotSpecification({self._wrapped_specification!r})"
