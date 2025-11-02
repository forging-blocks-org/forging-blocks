import pytest

from building_blocks.domain.errors import DomainRuleViolationError


class TestDomainRuleViolationError:
    def test_initialization_with_custom_message(self):
        custom_message = "Custom rule violation message."

        error = DomainRuleViolationError(message=custom_message)

        assert error.message == custom_message
        assert error.context == {}

    def test_initialization_with_context(self):
        custom_message = "Custom rule violation with context."
        context = {"key": "value"}

        error = DomainRuleViolationError(custom_message, context=context)

        assert error.context == context

    def test_str_representation(self):
        error = DomainRuleViolationError(
            message="Test message", context={"key": "value"}
        )
        assert str(error) == "Test message | Context: {'key': 'value'}"

    def test_raise_and_catch(self):
        with pytest.raises(DomainRuleViolationError) as exc_info:
            raise DomainRuleViolationError(
                "Test exception", context={"error": "details"}
            )

        error = exc_info.value
        assert error.message == "Test exception"
        assert error.context == {"error": "details"}
        assert str(error) == "Test exception | Context: {'error': 'details'}"

    def test_domain_rule_violation_error_with_context(self):
        error = DomainRuleViolationError(
            "Some rule violated", rule="RULE_1", context={"field": "value"}
        )
        assert str(error) == "[RULE_1] Some rule violated | Context: {'field': 'value'}"

    def test_domain_rule_violation_error_without_context(self):
        error = DomainRuleViolationError("Some rule violated", rule="RULE_1")
        assert str(error) == "[RULE_1] Some rule violated"
