from typing import Any, cast

import pytest

from forging_blocks.domain.specification.base import Specification
from forging_blocks.domain.specification.composable import ComposableSpecification


@pytest.mark.unit
class TestComposableSpecification:
    def test_is_subclass_of_specification(self) -> None:
        """ComposableSpecification should be a subclass of Specification."""
        # Arrange & Act & Assert
        assert issubclass(ComposableSpecification, Specification)

    def test_cannot_be_instantiated_directly(self) -> None:
        """ComposableSpecification cannot be instantiated directly as it is still abstract."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            cast(Any, ComposableSpecification[int])()

    def test_subclass_can_be_instantiated(self) -> None:
        """Concrete subclasses of ComposableSpecification can be instantiated."""

        # Arrange
        class ConcreteSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        # Act & Assert
        spec = ConcreteSpec()
        assert spec is not None

    def test_and_returns_and_specification(self) -> None:
        """The and_ method should return an AndSpecification."""

        # Arrange
        class LeftSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        left = LeftSpec()
        right = RightSpec()

        # Act
        result = left.and_(right)

        # Assert
        from forging_blocks.domain.specification.logical_operators import AndSpecification

        assert isinstance(result, AndSpecification)
        assert result.is_satisfied_by(5) is True
        assert result.is_satisfied_by(15) is False
        assert result.is_satisfied_by(-5) is False

    def test_or_returns_or_specification(self) -> None:
        """The or_ method should return an OrSpecification."""

        # Arrange
        class LeftSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 0

        left = LeftSpec()
        right = RightSpec()

        # Act
        result = left.or_(right)

        # Assert
        from forging_blocks.domain.specification.logical_operators import OrSpecification

        assert isinstance(result, OrSpecification)
        assert result.is_satisfied_by(5) is True
        assert result.is_satisfied_by(-5) is True
        assert result.is_satisfied_by(0) is False

    def test_not_returns_not_specification(self) -> None:
        """The not_ method should return a NotSpecification."""

        # Arrange
        class MySpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        spec = MySpec()

        # Act
        result = spec.not_()

        # Assert
        from forging_blocks.domain.specification.logical_operators import NotSpecification

        assert isinstance(result, NotSpecification)
        assert result.is_satisfied_by(-5) is True
        assert result.is_satisfied_by(5) is False

    def test_and_operator_returns_and_specification(self) -> None:
        """The & operator should return an AndSpecification."""

        # Arrange
        class LeftSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        left = LeftSpec()
        right = RightSpec()

        # Act
        result = left & right

        # Assert
        from forging_blocks.domain.specification.logical_operators import AndSpecification

        assert isinstance(result, AndSpecification)
        assert result.is_satisfied_by(5) is True

    def test_or_operator_returns_or_specification(self) -> None:
        """The | operator should return an OrSpecification."""

        # Arrange
        class LeftSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class RightSpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 0

        left = LeftSpec()
        right = RightSpec()

        # Act
        result = left | right

        # Assert
        from forging_blocks.domain.specification.logical_operators import OrSpecification

        assert isinstance(result, OrSpecification)
        assert result.is_satisfied_by(5) is True

    def test_invert_operator_returns_not_specification(self) -> None:
        """The ~ operator should return a NotSpecification."""

        # Arrange
        class MySpec(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        spec = MySpec()

        # Act
        result = ~spec

        # Assert
        from forging_blocks.domain.specification.logical_operators import NotSpecification

        assert isinstance(result, NotSpecification)
        assert result.is_satisfied_by(-5) is True

    def test_chained_composition_works(self) -> None:
        """Chaining multiple compositions should work correctly."""

        # Arrange
        class Spec1(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class Spec2(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        class Spec3(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate % 2 == 0

        spec1 = Spec1()
        spec2 = Spec2()
        spec3 = Spec3()

        # Act
        combined = cast(ComposableSpecification[int], spec1 & spec2) | spec3

        # Assert
        assert combined.is_satisfied_by(4) is True  # satisfies spec1 & spec2
        assert combined.is_satisfied_by(2) is True  # satisfies spec3
        assert combined.is_satisfied_by(15) is False  # satisfies spec1 but not spec2 or spec3
        assert combined.is_satisfied_by(-2) is True  # satisfies spec3

    def test_composition_with_mixed_operators(self) -> None:
        """Mixing &, |, and ~ operators should work correctly."""

        # Arrange
        class Spec1(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        class Spec2(ComposableSpecification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate < 10

        spec1 = Spec1()
        spec2 = Spec2()

        # Act
        result = spec1 & ~spec2

        # Assert
        assert result.is_satisfied_by(15) is True  # >0 and not <10
        assert result.is_satisfied_by(5) is False  # >0 but also <10
        assert result.is_satisfied_by(-5) is False  # not >0

    def test_uses_slots_for_memory_efficiency(self) -> None:
        """ComposableSpecification should use __slots__ for memory efficiency."""
        # Arrange & Act & Assert
        assert hasattr(ComposableSpecification, "__slots__")
