"""Validator for numeric value ranges."""

from typing import Any

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.rule_violations.rule_violated_error import RuleViolatedError
from forging_blocks.foundation.rules import ValidationRule


class RangeValidator(ValidationRule):
    """Validates that a numeric value falls within a ``[minimum, maximum]`` range.

    Example:
        ```python
        validator = RangeValidator("age", minimum_value=0, maximum_value=150)

        errors = validator.validate(42)
        assert errors == []

        errors = validator.validate(-5)
        assert len(errors) == 1  # below minimum
        ```

    """

    def __init__(
        self,
        field: str,
        minimum_value: int | float | None = None,
        maximum_value: int | float | None = None,
    ) -> None:
        self._field = field
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value

    def _check_type(self, value: Any) -> RuleViolationError | None:
        if not isinstance(value, (int, float)):
            return RuleViolatedError(
                ErrorMessage(f"'{self._field}' must be a number."),
                ErrorMetadata(context={"field": self._field, "code": "invalid_type"}),
            )
        return None

    def _check_minimum(self, value: int | float) -> RuleViolationError | None:
        if self._minimum_value is not None and value < self._minimum_value:
            return RuleViolatedError(
                ErrorMessage(f"'{self._field}' must be at least {self._minimum_value}."),
                ErrorMetadata(context={"field": self._field, "code": "minimum_value"}),
            )
        return None

    def _check_maximum(self, value: int | float) -> RuleViolationError | None:
        if self._maximum_value is not None and value > self._maximum_value:
            return RuleViolatedError(
                ErrorMessage(f"'{self._field}' must be at most {self._maximum_value}."),
                ErrorMetadata(context={"field": self._field, "code": "maximum_value"}),
            )
        return None

    def validate(self, value: Any) -> list[RuleViolationError]:
        """Validate that the given value is a number within the configured range."""
        type_error = self._check_type(value)
        if type_error is not None:
            return [type_error]

        errors: list[RuleViolationError] = []
        minimum_error = self._check_minimum(value)
        if minimum_error is not None:
            errors.append(minimum_error)
        maximum_error = self._check_maximum(value)
        if maximum_error is not None:
            errors.append(maximum_error)
        return errors
