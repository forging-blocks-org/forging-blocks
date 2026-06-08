# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation.errors import ResultAccessError
from forging_blocks.foundation.result import Err, Ok, Result


@pytest.mark.unit
class TestOk:
    @pytest.fixture
    def ok_result(self) -> Ok[int, str]:
        return Ok(123)

    def test___init___when_value_is_given_then_stores_it(self, ok_result: Ok[int, str]) -> None:
        result = ok_result._value

        assert result == 123

    def test___repr___when_called_then_returns_debug_representation(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.__repr__()

        assert result == "Ok(123)"

    def test___str___when_called_then_returns_user_friendly_string(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.__str__()

        assert result == "Ok(123)"

    def test___eq___when_comparing_two_equal_ok_results_then_returns_true(self) -> None:
        a: Ok[object, object] = Ok(1)
        b: Ok[object, object] = Ok(1)

        result = a.__eq__(b)

        assert result is True

    def test___eq___when_comparing_different_ok_results_then_returns_false(self) -> None:
        a: Ok[object, object] = Ok(1)
        b: Ok[object, object] = Ok(2)

        result = a.__eq__(b)

        assert result is False

    def test___eq___when_comparing_with_different_type_then_returns_false(self) -> None:
        ok: Ok[object, object] = Ok(1)
        other = object()

        result = ok.__eq__(other)

        assert result is False

    def test___hash___when_called_then_returns_hash_of_inner_value(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.__hash__()

        assert result == hash(123)

    def test_is_ok_when_called_then_returns_true(self, ok_result: Ok[int, str]) -> None:
        result = ok_result.is_ok

        assert result is True

    def test_is_err_when_called_then_returns_false(self, ok_result: Ok[int, str]) -> None:
        result = ok_result.is_err

        assert result is False

    def test_value_when_accessed_then_returns_inner_value(self, ok_result: Ok[int, str]) -> None:
        result = ok_result.value

        assert result == 123

    def test_error_when_accessed_then_raises_result_access_error(
        self, ok_result: Ok[int, str]
    ) -> None:
        with pytest.raises(ResultAccessError) as exc_info:
            _ = ok_result.error

        assert "Cannot access error" in str(exc_info.value)

    def test_map_when_called_with_fn_then_applies_fn_and_returns_new_ok(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.map(lambda x: x + 1)

        assert result == Ok(124)

    def test_map_when_called_with_type_change_then_returns_ok_with_new_type(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.map(lambda x: str(x))

        assert result == Ok("123")

    def test_map_error_when_called_then_passes_through_unchanged(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.map_error(lambda e: e.upper())

        assert result == Ok(123)

    def test_flat_map_when_called_with_fn_returning_ok_then_returns_that_ok(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.flat_map(lambda x: Ok(x + 1))

        assert result == Ok(124)

    def test_flat_map_when_called_with_fn_returning_err_then_returns_that_err(
        self, ok_result: Ok[int, str]
    ) -> None:
        result: Result[str, str] = ok_result.flat_map(lambda _: Err("failed"))

        assert result == Err("failed")

    def test_get_value_or_when_called_then_returns_inner_value(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.get_value_or(0)

        assert result == 123

    def test_get_value_or_else_when_called_then_returns_inner_value(
        self, ok_result: Ok[int, str]
    ) -> None:
        result = ok_result.get_value_or_else(lambda e: len(e))

        assert result == 123
