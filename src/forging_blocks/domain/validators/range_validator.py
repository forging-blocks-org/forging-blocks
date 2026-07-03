"""Validator for numeric value ranges."""

from typing import Any

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError
from forging_blocks.foundation.rules import ValidationRule


class RangeValidator(ValidationRule):
    """Validates that a numeric value falls within a ``[minimum, maximum]`` range."""

    def __init__(
        self,
        field: str,
        minimum_value: int | float | None = None,
        maximum_value: int | float | None = None,
    ) -> None:
        self._field = field
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value

    def validate(self, value: Any) -> list[RuleViolationError]:
        if not isinstance(value, (int, float)):
            return [
                RuleViolationError(
                    ErrorMessage(f"'{self._field}' must be a number."),
                    ErrorMetadata(context={"field": self._field, "code": "invalid_type"}),
                )
            ]

        errors: list[RuleViolationError] = []

        if self._minimum_value is not None and value < self._minimum_value:
            errors.append(
                RuleViolationError(
                    ErrorMessage(f"'{self._field}' must be at least {self._minimum_value}."),
                    ErrorMetadata(context={"field": self._field, "code": "minimum_value"}),
                )
            )

        if self._maximum_value is not None and value > self._maximum_value:
            errors.append(
                RuleViolationError(
                    ErrorMessage(f"'{self._field}' must be at most {self._maximum_value}."),
                    ErrorMetadata(context={"field": self._field, "code": "maximum_value"}),
                )
            )

        return errors
