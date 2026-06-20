from collections.abc import Callable
from typing import Any, cast

import pytest

from forging_blocks.foundation.errors.not_callable_predicate_error import NotCallablePredicateError
from forging_blocks.foundation.specification.expression import ExpressionSpecification


@pytest.mark.unit
class TestExpressionSpecification:
    def test_initialization_with_valid_callable_then_succeeds(self) -> None:
        """When initialized with a valid callable predicate, no error is raised."""

        # Arrange
        def predicate(x: int) -> bool:
            return x > 0

        # Act & Assert
        spec = ExpressionSpecification(predicate)
        assert spec is not None

    def test_initialization_with_lambda_then_succeeds(self) -> None:
        """When initialized with a lambda, no error is raised."""

        # Arrange
        def predicate(x: int) -> bool:
            return x > 0

        # Act & Assert
        spec = ExpressionSpecification[int](predicate)
        assert spec is not None

    def test_initialization_with_non_callable_then_raises_not_callable_predicate_error(
        self,
    ) -> None:
        """When initialized with a non-callable object, raises NotCallablePredicateError."""
        # Arrange
        invalid_predicate: Any = 42

        # Act & Assert
        with pytest.raises(
            NotCallablePredicateError, match="predicate must be Callable and not int"
        ):
            ExpressionSpecification(cast(Callable[..., Any], invalid_predicate))

    def test_initialization_with_none_then_raises_not_callable_predicate_error(self) -> None:
        """When initialized with None, raises NotCallablePredicateError."""
        # Arrange & Act & Assert
        with pytest.raises(
            NotCallablePredicateError, match="predicate must be Callable and not NoneType"
        ):
            ExpressionSpecification(cast(Callable[..., Any], None))

    def test_initialization_with_string_then_raises_not_callable_predicate_error(self) -> None:
        """When initialized with a string, raises NotCallablePredicateError."""
        # Arrange & Act & Assert
        with pytest.raises(
            NotCallablePredicateError, match="predicate must be Callable and not str"
        ):
            ExpressionSpecification(cast(Callable[..., Any], "not_a_callable"))

    def test_is_satisfied_by_when_candidate_satisfies_predicate_then_returns_true(self) -> None:
        """When the candidate satisfies the predicate, returns True."""

        # Arrange
        def is_even(x: int) -> bool:
            return x % 2 == 0

        spec = ExpressionSpecification(is_even)
        candidate = 4

        # Act
        result = spec.is_satisfied_by(candidate)

        # Assert
        assert result is True

    def test_is_satisfied_by_when_candidate_does_not_satisfy_predicate_then_returns_false(
        self,
    ) -> None:
        """When the candidate does not satisfy the predicate, returns False."""

        # Arrange
        def is_even(x: int) -> bool:
            return x % 2 == 0

        spec = ExpressionSpecification(is_even)
        candidate = 3

        # Act
        result = spec.is_satisfied_by(candidate)

        # Assert
        assert result is False

    def test_is_satisfied_by_with_lambda_predicate_then_returns_correct_result(self) -> None:
        """Lambda predicates work correctly with is_satisfied_by."""
        # Arrange
        spec = ExpressionSpecification[int](lambda x: x > 10)

        # Act & Assert
        assert spec.is_satisfied_by(15) is True
        assert spec.is_satisfied_by(5) is False
        assert spec.is_satisfied_by(10) is False

    def test_is_satisfied_by_with_string_candidate_then_works(self) -> None:
        """String candidates work correctly with string predicates."""

        # Arrange
        def starts_with_hello(s: str) -> bool:
            return s.startswith("hello")

        spec = ExpressionSpecification(starts_with_hello)

        # Act & Assert
        assert spec.is_satisfied_by("hello world") is True
        assert spec.is_satisfied_by("goodbye") is False

    def test_initialization_with_description_then_stores_description(self) -> None:
        """When initialized with a description, it is stored correctly."""

        # Arrange
        def predicate(x: int) -> bool:
            return x > 0

        description = "Positive numbers only"

        # Act
        spec = ExpressionSpecification(predicate, description=description)

        # Assert
        assert repr(spec) == f"ExpressionSpecification({description!r})"

    def test_initialization_without_description_then_defaults_to_empty_string(self) -> None:
        """When initialized without a description, it defaults to empty string."""

        # Arrange
        def predicate(x: int) -> bool:
            return x > 0

        # Act
        spec = ExpressionSpecification(predicate)

        # Assert
        assert repr(spec) == "ExpressionSpecification(predicate)"

    def test_repr_when_description_provided_then_includes_description(self) -> None:
        """When a description is provided, repr includes it."""

        # Arrange
        def predicate(x: int) -> bool:
            return x > 0

        spec = ExpressionSpecification(predicate, description="Positive numbers")

        # Act
        result = repr(spec)

        # Assert
        assert "ExpressionSpecification" in result
        assert "Positive numbers" in result

    def test_repr_when_no_description_then_includes_predicate_name(self) -> None:
        """When no description is provided, repr includes the predicate name."""

        # Arrange
        def my_predicate(x: int) -> bool:
            return x > 0

        spec = ExpressionSpecification(my_predicate)

        # Act
        result = repr(spec)

        # Assert
        assert "ExpressionSpecification" in result
        assert "my_predicate" in result

    def test_repr_when_anonymous_lambda_then_uses_lambda_name(self) -> None:
        """When using an anonymous lambda, repr uses '<lambda>'."""
        # Arrange
        spec = ExpressionSpecification[int](lambda x: x > 0)

        # Act
        result = repr(spec)

        # Assert
        assert "ExpressionSpecification" in result
        assert "<lambda>" in result

    def test_repr_when_builtin_function_then_uses_function_name(self) -> None:
        """When using a builtin function, repr uses the function name."""
        # Arrange
        spec = ExpressionSpecification(str.isalpha)

        # Act
        result = repr(spec)

        # Assert
        assert "ExpressionSpecification" in result
        assert "isalpha" in result

    def test_is_subclass_of_composable_specification(self) -> None:
        """ExpressionSpecification should be a subclass of ComposableSpecification."""
        # Arrange & Act & Assert
        from forging_blocks.foundation.specification.composable import ComposableSpecification

        assert issubclass(ExpressionSpecification, ComposableSpecification)

    def test_and_operation_when_both_satisfied_then_returns_true(self) -> None:
        """AND operation with ExpressionSpecifications works correctly."""

        # Arrange
        def is_even(x: int) -> bool:
            return x % 2 == 0

        def is_positive(x: int) -> bool:
            return x > 0

        spec1 = ExpressionSpecification(is_even)
        spec2 = ExpressionSpecification(is_positive)
        combined = spec1 & spec2

        # Act & Assert
        assert combined.is_satisfied_by(4) is True
        assert combined.is_satisfied_by(5) is False
        assert combined.is_satisfied_by(-2) is False

    def test_or_operation_when_either_satisfied_then_returns_true(self) -> None:
        """OR operation with ExpressionSpecifications works correctly."""

        # Arrange
        def is_even(x: int) -> bool:
            return x % 2 == 0

        def is_positive(x: int) -> bool:
            return x > 0

        spec1 = ExpressionSpecification(is_even)
        spec2 = ExpressionSpecification(is_positive)
        combined = spec1 | spec2

        # Act & Assert
        assert combined.is_satisfied_by(4) is True
        assert combined.is_satisfied_by(5) is True
        assert combined.is_satisfied_by(-2) is True
        assert combined.is_satisfied_by(-3) is False

    def test_not_operation_when_inverts_result(self) -> None:
        """NOT operation with ExpressionSpecification works correctly."""

        # Arrange
        def is_even(x: int) -> bool:
            return x % 2 == 0

        spec = ExpressionSpecification(is_even)
        negated = ~spec

        # Act & Assert
        assert negated.is_satisfied_by(3) is True
        assert negated.is_satisfied_by(4) is False
