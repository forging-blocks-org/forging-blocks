import pytest

from forging_blocks.domain.specification.base import Specification
from forging_blocks.domain.specification.logical_operators.not_specification import (
    NotSpecification,
)


@pytest.mark.unit
class TestNotSpecification:
    def test_initialization_stores_wrapped_specification(self) -> None:
        """NotSpecification should store the wrapped specification."""

        # Arrange
        class ConcreteSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        spec = ConcreteSpec()

        # Act
        not_spec = NotSpecification(spec)

        # Assert
        assert not_spec.is_satisfied_by(5) is False
        assert not_spec.is_satisfied_by(-5) is True

    def test_is_satisfied_by_when_wrapped_true_then_returns_false(self) -> None:
        """When wrapped specification is satisfied, returns False."""

        # Arrange
        class ConcreteSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        not_spec = NotSpecification(ConcreteSpec())

        # Act & Assert
        assert not_spec.is_satisfied_by(5) is False

    def test_is_satisfied_by_when_wrapped_false_then_returns_true(self) -> None:
        """When wrapped specification is not satisfied, returns True."""

        # Arrange
        class ConcreteSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        not_spec = NotSpecification(ConcreteSpec())

        # Act & Assert
        assert not_spec.is_satisfied_by(-5) is True

    def test_is_subclass_of_specification(self) -> None:
        """NotSpecification should be a subclass of Specification."""
        # Arrange & Act & Assert
        assert issubclass(NotSpecification, Specification)

    def test_uses_slots_for_memory_efficiency(self) -> None:
        """NotSpecification should use __slots__ for memory efficiency."""
        # Arrange & Act & Assert
        assert hasattr(NotSpecification, "__slots__")
        assert "_wrapped_specification" in NotSpecification.__slots__

    def test_repr_includes_class_name(self) -> None:
        """The repr should include the class name and the wrapped specification."""

        # Arrange
        class ConcreteSpec(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        not_spec = NotSpecification(ConcreteSpec())

        # Act
        result = repr(not_spec)

        # Assert
        assert "NotSpecification" in result
