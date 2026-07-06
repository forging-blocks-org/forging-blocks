# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

import pytest

from forging_blocks.domain.validators.range_validator import RangeValidator


@pytest.mark.unit
class TestRangeValidator:
    def test_when_within_range_then_no_error(self) -> None:
        result = RangeValidator("age", minimum_value=0, maximum_value=150).validate(30)

        assert result == []

    def test_when_below_minimum_then_error(self) -> None:
        result = RangeValidator("age", minimum_value=0).validate(-5)

        assert len(result) == 1
        assert result[0].context["code"] == "minimum_value"

    def test_when_above_maximum_then_error(self) -> None:
        result = RangeValidator("age", maximum_value=150).validate(200)

        assert len(result) == 1
        assert result[0].context["code"] == "maximum_value"

    def test_when_float_value_then_supported(self) -> None:
        result = RangeValidator("score", minimum_value=0.0, maximum_value=1.0).validate(0.5)

        assert result == []

    def test_when_not_numeric_then_error(self) -> None:
        result = RangeValidator("age").validate("thirty")

        assert len(result) == 1
        assert result[0].context["code"] == "invalid_type"
