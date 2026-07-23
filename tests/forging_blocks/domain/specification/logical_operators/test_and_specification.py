import pytest

from forging_blocks.foundation.specification.base import Specification
from forging_blocks.foundation.specification.logical_operators.and_specification import (
    AndSpecification,
)


@pytest.mark.unit
class TestAndSpecification:
    def test_initialization_stores_both_specifications(self) -> None:
        """AndSpecification should store both left and right specifications."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        left = LeftSpec()
        right = RightSpec()

        # Act
        and_spec = AndSpecification(left, right)

        # Assert
        assert and_spec.is_satisfied_by(5) is True
        assert and_spec.is_satisfied_by(0) is False
        assert and_spec.is_satisfied_by(15) is False

    def test_is_satisfied_by_when_both_true_then_returns_true(self) -> None:
        """When both specifications are satisfied, returns True."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        and_spec = AndSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert and_spec.is_satisfied_by(5) is True

    def test_is_satisfied_by_when_left_false_then_returns_false(self) -> None:
        """When left specification is not satisfied, returns False."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        and_spec = AndSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert and_spec.is_satisfied_by(-5) is False

    def test_is_satisfied_by_when_right_false_then_returns_false(self) -> None:
        """When right specification is not satisfied, returns False."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        and_spec = AndSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert and_spec.is_satisfied_by(15) is False

    def test_is_satisfied_by_when_both_false_then_returns_false(self) -> None:
        """When both specifications are not satisfied, returns False."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        and_spec = AndSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert and_spec.is_satisfied_by(-15) is False

    def test_with_string_candidates(self) -> None:
        """AndSpecification works with string candidates."""

        # Arrange
        class LeftSpec(Specification[str]):
            def is_satisfied_by(self, candidate: str) -> bool:
                return len(candidate) > 0

        class RightSpec(Specification[str]):
            def is_satisfied_by(self, candidate: str) -> bool:
                return candidate.startswith("hello")

        and_spec = AndSpecification(LeftSpec(), RightSpec())

        # Act & Assert
        assert and_spec.is_satisfied_by("hello world") is True
        assert and_spec.is_satisfied_by("") is False
        assert and_spec.is_satisfied_by("goodbye") is False

    def test_with_complex_objects(self) -> None:
        """AndSpecification works with complex object candidates."""

        # Arrange
        class Person:
            def __init__(self, name: str, age: int) -> None:
                self.name = name
                self.age = age

        class NameSpec(Specification[Person]):
            def is_satisfied_by(self, candidate: Person) -> bool:
                return len(candidate.name) > 0

        class AgeSpec(Specification[Person]):
            def is_satisfied_by(self, candidate: Person) -> bool:
                return candidate.age >= 18

        and_spec = AndSpecification(NameSpec(), AgeSpec())

        # Act & Assert
        assert and_spec.is_satisfied_by(Person("Alice", 25)) is True
        assert and_spec.is_satisfied_by(Person("", 25)) is False
        assert and_spec.is_satisfied_by(Person("Bob", 15)) is False

    def test_is_subclass_of_specification(self) -> None:
        """AndSpecification should be a subclass of Specification."""
        # Arrange & Act & Assert
        assert issubclass(AndSpecification, Specification)

    def test_uses_slots_for_memory_efficiency(self) -> None:
        """AndSpecification should use __slots__ for memory efficiency."""
        # Arrange & Act & Assert
        assert hasattr(AndSpecification, "__slots__")
        assert "_left_specification" in AndSpecification.__slots__
        assert "_right_specification" in AndSpecification.__slots__

    def test_repr_includes_class_name(self) -> None:
        """The repr should include the class name."""

        # Arrange
        class LeftSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return True

        class RightSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return True

        and_spec = AndSpecification(LeftSpec(), RightSpec())

        # Act
        result = repr(and_spec)

        # Assert
        assert "AndSpecification" in result
