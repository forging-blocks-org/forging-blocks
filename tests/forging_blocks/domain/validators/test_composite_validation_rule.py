# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.validators.composite_validation_rule import CompositeValidationRule
from forging_blocks.domain.validators.email_validator import EmailValidator
from forging_blocks.domain.validators.length_validator import LengthValidator
from forging_blocks.domain.validators.required_validator import RequiredValidator


@pytest.mark.unit
class TestCompositeValidationRule:
    def test_when_all_pass_then_no_error(self) -> None:
        composite = CompositeValidationRule(
            [
                RequiredValidator("email"),
                EmailValidator("email"),
            ]
        )
        result = composite.validate("user@example.com")

        assert result == []

    def test_when_one_fails_then_collects_error(self) -> None:
        composite = CompositeValidationRule(
            [
                RequiredValidator("email"),
                EmailValidator("email"),
            ]
        )
        result = composite.validate("invalid")

        assert len(result) == 1
        assert result[0].context["code"] == "invalid_email"

    def test_when_multiple_fail_then_collects_all(self) -> None:
        composite = CompositeValidationRule(
            [
                RequiredValidator("name"),
                LengthValidator("name", minimum_length=5),
            ]
        )
        result = composite.validate("ab")

        assert len(result) == 1
