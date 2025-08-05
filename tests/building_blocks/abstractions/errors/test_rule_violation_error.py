from building_blocks.abstractions.errors.core import ErrorMessage, ErrorMetadata
from building_blocks.abstractions.errors.rule_violation_error import RuleViolationError


class TestRuleViolationError:
    def test__str___when_called_then_return_the_expected_string(self) -> None:
        message = ErrorMessage("This is a rule violation error.")
        error = RuleViolationError(message)

        actual = str(error)

        expected = "Rule Violation: This is a rule violation error."
        assert actual == expected

    def test__str___when_message_is_empty_then_return_empty_string(self) -> None:
        message = ErrorMessage("")
        error = RuleViolationError(message)

        actual = str(error)

        expected = "Rule Violation: "
        assert actual == expected

    def test__str__when_message_and_metadata_defined_then_returns_combined_string(
        self,
    ) -> None:
        message = ErrorMessage("This is a rule violation error.")
        metadata = ErrorMetadata({"context": "some context"})
        error = RuleViolationError(message, metadata)

        actual = str(error)

        expected = (
            "Rule Violation: This is a rule violation error. "
            "| Context: {'context': 'some context'}"
        )
        assert actual == expected
