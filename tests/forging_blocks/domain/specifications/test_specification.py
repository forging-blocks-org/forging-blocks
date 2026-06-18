"""Tests for the Specification pattern."""

import pytest

from forging_blocks.domain.specifications import (
    ExpressionSpecification,
    Specification,
)


class IsPositive(Specification[int]):
    """Specification that a number is positive."""

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate > 0


class IsEven(Specification[int]):
    """Specification that a number is even."""

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate % 2 == 0


@pytest.mark.unit
class TestSpecification:
    """Specification satisfaction and composition."""

    def test_is_satisfied_by_returns_true(self) -> None:
        """A specification returns True when the candidate meets the criteria."""
        spec = IsPositive()
        assert spec.is_satisfied_by(5) is True

    def test_is_satisfied_by_returns_false(self) -> None:
        """A specification returns False when the candidate does not meet criteria."""
        spec = IsPositive()
        assert spec.is_satisfied_by(-1) is False

    def test_and_specification(self) -> None:
        """AndSpecification is satisfied only when both specs are satisfied."""
        spec = IsPositive() & IsEven()
        assert spec.is_satisfied_by(4) is True
        assert spec.is_satisfied_by(3) is False  # not even
        assert spec.is_satisfied_by(-2) is False  # not positive

    def test_or_specification(self) -> None:
        """OrSpecification is satisfied when at least one spec is satisfied."""
        spec = IsPositive() | IsEven()
        assert spec.is_satisfied_by(4) is True
        assert spec.is_satisfied_by(3) is True  # positive
        assert spec.is_satisfied_by(-2) is True  # even
        assert spec.is_satisfied_by(-3) is False  # neither

    def test_not_specification(self) -> None:
        """NotSpecification negates the wrapped specification."""
        spec = ~IsPositive()
        assert spec.is_satisfied_by(-1) is True
        assert spec.is_satisfied_by(0) is True  # 0 is not positive
        assert spec.is_satisfied_by(5) is False

    def test_and_method(self) -> None:
        """The and_() method works the same as & operator."""
        spec = IsPositive().and_(IsEven())
        assert spec.is_satisfied_by(4) is True

    def test_or_method(self) -> None:
        """The or_() method works the same as | operator."""
        spec = IsPositive().or_(IsEven())
        assert spec.is_satisfied_by(3) is True

    def test_not_method(self) -> None:
        """The not_() method works the same as ~ operator."""
        spec = IsPositive().not_()
        assert spec.is_satisfied_by(-1) is True


@pytest.mark.unit
class TestExpressionSpecification:
    """ExpressionSpecification with callables."""

    def test_expression_satisfied(self) -> None:
        """ExpressionSpecification evaluates the callable."""
        spec = ExpressionSpecification[int](lambda x: x > 10)
        assert spec.is_satisfied_by(15) is True
        assert spec.is_satisfied_by(5) is False

    def test_expression_with_description(self) -> None:
        """ExpressionSpecification stores a description."""
        spec = ExpressionSpecification[int](lambda x: x > 0, description="positive")
        assert "positive" in repr(spec)
