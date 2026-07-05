# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.validators.length_validator import LengthValidator


@pytest.mark.unit
class TestLengthValidator:
    def test_when_within_range_then_no_error(self) -> None:
        result = LengthValidator("password", minimum_length=8, maximum_length=20).validate(
            "ten-chars!"
        )

        assert result == []

    def test_when_too_short_then_error(self) -> None:
        result = LengthValidator("password", minimum_length=8).validate("abc")

        assert len(result) == 1
        assert result[0].context["code"] == "minimum_length"

    def test_when_too_long_then_error(self) -> None:
        result = LengthValidator("password", maximum_length=5).validate("abcdef")

        assert len(result) == 1
        assert result[0].context["code"] == "maximum_length"

    def test_when_not_a_string_then_error(self) -> None:
        result = LengthValidator("password").validate(123)

        assert len(result) == 1
        assert result[0].context["code"] == "invalid_type"
