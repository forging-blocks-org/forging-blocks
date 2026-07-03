# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.validators.email_validator import EmailValidator


@pytest.mark.unit
class TestEmailValidator:
    def test_when_valid_email_then_no_error(self) -> None:
        result = EmailValidator("email").validate("user@example.com")

        assert result == []

    def test_when_invalid_format_then_error(self) -> None:
        result = EmailValidator("email").validate("not-an-email")

        assert len(result) == 1
        assert result[0].context["code"] == "invalid_email"

    def test_when_none_then_error(self) -> None:
        result = EmailValidator("email").validate(None)

        assert len(result) == 1
        assert result[0].context["code"] == "invalid_email"
