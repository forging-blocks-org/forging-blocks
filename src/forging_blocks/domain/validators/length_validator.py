"""Validator for string length constraints."""

from typing import Any

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError
from forging_blocks.foundation.rules import ValidationRule


class LengthValidator(ValidationRule):
    """Validates that a string's length falls within a ``[minimum, maximum]`` range."""

    def __init__(
        self,
        field: str,
        minimum_length: int = 0,
        maximum_length: int | None = None,
    ) -> None:
        self._field = field
        self._minimum_length = minimum_length
        self._maximum_length = maximum_length

    def validate(self, value: Any) -> list[RuleViolationError]:
        if not isinstance(value, str):
            return [
                RuleViolationError(
                    ErrorMessage(f"'{self._field}' must be a string."),
                    ErrorMetadata(context={"field": self._field, "code": "invalid_type"}),
                )
            ]

        errors: list[RuleViolationError] = []

        if len(value) < self._minimum_length:
            errors.append(
                RuleViolationError(
                    ErrorMessage(
                        f"'{self._field}' must be at least {self._minimum_length} characters."
                    ),
                    ErrorMetadata(context={"field": self._field, "code": "minimum_length"}),
                )
            )

        if self._maximum_length is not None and len(value) > self._maximum_length:
            errors.append(
                RuleViolationError(
                    ErrorMessage(
                        f"'{self._field}' must be at most {self._maximum_length} characters."
                    ),
                    ErrorMetadata(context={"field": self._field, "code": "maximum_length"}),
                )
            )

        return errors
