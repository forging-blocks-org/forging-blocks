from building_blocks.foundation.errors.core import ErrorMessage
from building_blocks.foundation.errors.rule_violation_error import (
    CombinedRuleViolationErrors,
    RuleViolationError,
)


class TestRuleViolationError:
    def test_constructor(self) -> None:
        error_message = ErrorMessage("Test rule violation error")

        error = RuleViolationError(error_message)

        assert isinstance(error, RuleViolationError)


class TestCombinedRuleViolationErrors:
    def test_constructor(self) -> None:
        error_message = ErrorMessage("Test rule violation error")
        error = RuleViolationError(error_message)

        combined_errors = CombinedRuleViolationErrors([error])

        assert isinstance(combined_errors, CombinedRuleViolationErrors)
