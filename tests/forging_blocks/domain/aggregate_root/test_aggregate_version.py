# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.domain import AggregateVersion


@pytest.mark.unit
class TestAggregateVersion:
    def test___init___when_value_is_not_int_then_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            AggregateVersion("1")  # type: ignore

    def test___init___when_value_is_negative_then_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            AggregateVersion(-1)

    def test_value_when_accessed_then_returns_correct_integer(self) -> None:
        version = AggregateVersion(3)
        result = version.value
        assert result == 3

    def test_increment_when_called_then_returns_new_instance_with_value_incremented(
        self,
    ) -> None:
        version = AggregateVersion(2)
        result = version.increment()
        assert result.value == 3
        assert result is not version

    def test___eq___when_values_are_equal_then_returns_true(self) -> None:
        a = AggregateVersion(1)
        b = AggregateVersion(1)
        assert a == b

    def test___eq___when_values_differ_then_returns_false(self) -> None:
        a = AggregateVersion(1)
        b = AggregateVersion(2)
        assert a != b
