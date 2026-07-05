"""Combines multiple validation rules into a single rule."""

from typing import Any

from forging_blocks.foundation.errors.rule_violation_error import RuleViolationError
from forging_blocks.foundation.rules import ValidationRule


class CompositeValidationRule(ValidationRule):
    """Combines multiple ``ValidationRule`` instances into a single rule.

    All rules are evaluated and their errors are concatenated (no
    short-circuit), so every validation failure is reported.
    """

    def __init__(self, rules: list[ValidationRule]) -> None:
        self._rules = rules

    def validate(self, value: Any) -> list[RuleViolationError]:
        errors: list[RuleViolationError] = []
        for rule in self._rules:
            errors.extend(rule.validate(value))
        return errors
