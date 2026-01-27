import pytest

from forging_blocks.foundation import (
    CombinedRuleViolationErrors,
    ErrorMessage,
    RuleViolationError,
)


@pytest.mark.unit
class TestRuleViolationError:
    def test_constructor(self) -> None:
        error_message = ErrorMessage("Test rule violation error")

        error = RuleViolationError(error_message)

        assert isinstance(error, RuleViolationError)


@pytest.mark.unit
class TestCombinedRuleViolationErrors:
    def test_constructor(self) -> None:
        error_message = ErrorMessage("Test rule violation error")
        error = RuleViolationError(error_message)

        combined_errors = CombinedRuleViolationErrors([error])

        assert isinstance(combined_errors, CombinedRuleViolationErrors)
