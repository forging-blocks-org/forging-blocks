# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.validators.required_validator import RequiredValidator


@pytest.mark.unit
class TestRequiredValidator:
    def test_when_value_is_none_then_error(self) -> None:
        result = RequiredValidator("name").validate(None)

        assert len(result) == 1
        assert result[0].context == {"field": "name", "code": "required"}

    def test_when_value_is_empty_string_then_error(self) -> None:
        result = RequiredValidator("name").validate("")

        assert len(result) == 1
        assert result[0].context["code"] == "required"

    def test_when_value_is_non_empty_then_no_error(self) -> None:
        result = RequiredValidator("name").validate("Alice")

        assert result == []
