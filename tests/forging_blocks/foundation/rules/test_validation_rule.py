from typing import Any

import pytest

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError
from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.rule_violations.rule_violated_error import RuleViolatedError
from forging_blocks.foundation.rules import ValidationRule


@pytest.mark.unit
class TestValidationRule:
    def test_when_concrete_implementation_then_returns_errors(self) -> None:
        class AlwaysFailingRule(ValidationRule):
            def validate(self, value: Any) -> list[RuleViolationError]:
                del value
                return [RuleViolatedError(ErrorMessage("no"))]

        rule = AlwaysFailingRule()
        result = rule.validate(None)

        assert len(result) == 1
        assert str(result[0]) == "RuleViolatedError: no"

    def test_when_concrete_implementation_then_can_return_empty(self) -> None:
        class AlwaysPassingRule(ValidationRule):
            def validate(self, value: Any) -> list[RuleViolationError]:
                del value
                return []

        rule = AlwaysPassingRule()
        result = rule.validate(42)

        assert result == []
