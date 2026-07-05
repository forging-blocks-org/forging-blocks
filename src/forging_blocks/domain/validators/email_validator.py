"""Validator for email address format."""

import re
from typing import Any

from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata
from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError
from forging_blocks.foundation.rules import ValidationRule


class EmailValidator(ValidationRule):
    """Validates that a string value is a well-formed email address."""

    _EMAIL_PATTERN: re.Pattern[str] = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
        r"[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
    )

    def __init__(self, field: str) -> None:
        self._field = field

    def validate(self, value: Any) -> list[RuleViolationError]:
        if value is None or not isinstance(value, str) or not self._EMAIL_PATTERN.match(value):
            return [
                RuleViolationError(
                    ErrorMessage(f"'{self._field}' must be a valid email address."),
                    ErrorMetadata(context={"field": self._field, "code": "invalid_email"}),
                )
            ]
        return []
