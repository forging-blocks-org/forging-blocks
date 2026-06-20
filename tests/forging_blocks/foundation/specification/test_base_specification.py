from abc import ABC
from typing import Any, cast

import pytest

from forging_blocks.foundation.specification.base import Specification


@pytest.mark.unit
class TestSpecification:
    def test_is_abstract_base_class(self) -> None:
        """Specification should be an abstract base class."""
        # Arrange & Act & Assert
        assert issubclass(Specification, ABC)

    def test_cannot_instantiate_directly(self) -> None:
        """Specification cannot be instantiated directly as it is abstract."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            cast(Any, Specification)()

    def test_has_is_satisfied_by_abstract_method(self) -> None:
        """Specification should have an abstract is_satisfied_by method."""
        # Arrange & Act & Assert
        assert hasattr(Specification, "is_satisfied_by")
        assert "is_satisfied_by" in Specification.__abstractmethods__

    def test_subclass_must_implement_is_satisfied_by(self) -> None:
        """Concrete subclasses must implement is_satisfied_by."""

        # Arrange
        class IncompleteSpecification(Specification[int]):
            pass

        # Act & Assert
        with pytest.raises(TypeError):
            cast(Any, IncompleteSpecification)()

    def test_subclass_with_is_satisfied_by_implemented_can_be_instantiated(self) -> None:
        """Concrete subclasses that implement is_satisfied_by can be instantiated."""

        # Arrange
        class ConcreteSpecification(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 0

        # Act & Assert
        spec = ConcreteSpecification()
        assert spec is not None
        assert spec.is_satisfied_by(5) is True
        assert spec.is_satisfied_by(-5) is False

    def test_is_satisfied_by_signature_with_generic_type(self) -> None:
        """is_satisfied_by should accept a generic type T and return bool."""

        # Arrange
        class ConcreteSpecification(Specification[str]):
            def is_satisfied_by(self, candidate: str) -> bool:
                return len(candidate) > 0

        # Act & Assert
        spec = ConcreteSpecification()
        assert spec.is_satisfied_by("hello") is True
        assert spec.is_satisfied_by("") is False
