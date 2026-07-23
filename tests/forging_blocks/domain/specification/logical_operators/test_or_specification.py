import pytest

from forging_blocks.domain.specification.base import Specification
from forging_blocks.domain.specification.logical_operators.or_specification import (
    OrSpecification,
)


@pytest.mark.unit
class TestOrSpecification:
    def test_initialization_stores_both_specifications(self) -> None:
        """OrSpecification should store both left and right specifications."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 0

        left = LeftSpec()
        right = RightSpec()

        # Act
        or_spec = OrSpecification(left, right)

        # Assert
        assert or_spec.is_satisfied_by(5) is True
        assert or_spec.is_satisfied_by(-5) is True
        assert or_spec.is_satisfied_by(0) is False

    def test_is_satisfied_by_when_left_true_then_returns_true(self) -> None:
        """When left specification is satisfied, returns True."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 0

        or_spec = OrSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert or_spec.is_satisfied_by(5) is True

    def test_is_satisfied_by_when_right_true_then_returns_true(self) -> None:
        """When right specification is satisfied, returns True."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 0

        or_spec = OrSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert or_spec.is_satisfied_by(-5) is True

    def test_is_satisfied_by_when_both_true_then_returns_true(self) -> None:
        """When both specifications are satisfied, returns True."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        or_spec = OrSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert or_spec.is_satisfied_by(5) is True

    def test_is_satisfied_by_when_both_false_then_returns_false(self) -> None:
        """When both specifications are not satisfied, returns False."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 0

        or_spec = OrSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert or_spec.is_satisfied_by(0) is False

    def test_is_subclass_of_specification(self) -> None:
        """OrSpecification should be a subclass of Specification."""
        # Arrange & Act & Assert
        assert issubclass(OrSpecification, Specification)

    def test_uses_slots_for_memory_efficiency(self) -> None:
        """OrSpecification should use __slots__ for memory efficiency."""
        # Arrange & Act & Assert
        assert hasattr(OrSpecification, "__slots__")
        assert "_left_specification" in OrSpecification.__slots__
        assert "_right_specification" in OrSpecification.__slots__

    def test_repr_includes_class_name(self) -> None:
        """The repr should include the class name and both specifications."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return True

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return True

        or_spec = OrSpecification(LeftSpec(), RightSpec())

        # Act
        result = repr(or_spec)

        # Assert
        assert "OrSpecification" in result
