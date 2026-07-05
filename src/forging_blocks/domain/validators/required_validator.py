"""Validator that fails when a value is None or an empty string."""

from typing import Any

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError
from forging_blocks.foundation.rules import ValidationRule


class RequiredValidator(ValidationRule):
    """Fails when the value is ``None`` or an empty string."""

    def __init__(self, field: str) -> None:
        self._field = field

    def validate(self, value: Any) -> list[RuleViolationError]:
        if value is None or value == "":
            return [
                RuleViolationError(
                    ErrorMessage(f"'{self._field}' is required."),
                    ErrorMetadata(context={"field": self._field, "code": "required"}),
                )
            ]
        return []
