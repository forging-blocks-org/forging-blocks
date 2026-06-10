# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation.errors import ResultAccessError
from forging_blocks.foundation.result import Err, Ok


@pytest.mark.unit
class TestErr:
    @pytest.fixture
    def err_result(self) -> Err[int, str]:
        return Err("boom")

    def test___init___when_error_is_given_then_stores_it(self, err_result: Err[int, str]) -> None:
        result = err_result._error

        assert result == "boom"

    def test___repr___when_called_then_returns_debug_representation(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.__repr__()

        assert result == "Err('boom')"

    def test___str___when_called_then_returns_user_friendly_string(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.__str__()

        assert result == "Err(boom)"

    def test___eq___when_comparing_two_equal_err_results_then_returns_true(self) -> None:
        a: Err[object, str] = Err("x")
        b: Err[object, str] = Err("x")

        result = a.__eq__(b)

        assert result is True

    def test___eq___when_comparing_different_err_results_then_returns_false(self) -> None:
        a: Err[object, str] = Err("x")
        b: Err[object, str] = Err("y")

        result = a.__eq__(b)

        assert result is False

    def test___eq___when_comparing_with_different_type_then_returns_false(self) -> None:
        err: Err[object, str] = Err("boom")
        other = object()

        result = err.__eq__(other)

        assert result is False

    def test___hash___when_called_then_returns_hash_of_inner_error(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.__hash__()

        assert result == hash("boom")

    def test_is_ok_when_called_then_returns_false(self, err_result: Err[int, str]) -> None:
        result = err_result.is_ok

        assert result is False

    def test_is_err_when_called_then_returns_true(self, err_result: Err[int, str]) -> None:
        result = err_result.is_err

        assert result is True

    def test_value_when_accessed_then_raises_result_access_error(
        self, err_result: Err[int, str]
    ) -> None:
        with pytest.raises(ResultAccessError) as exc_info:
            _ = err_result.value

        assert "Cannot access value" in str(exc_info.value)

    def test_error_when_accessed_then_returns_inner_error(self, err_result: Err[int, str]) -> None:
        result = err_result.error

        assert result == "boom"

    def test_map_when_called_then_passes_through_unchanged(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.map(lambda x: x + 1)

        assert result == Err("boom")

    def test_map_error_when_called_with_fn_then_applies_fn_and_returns_new_err(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.map_error(lambda e: e.upper())

        assert result == Err("BOOM")

    def test_map_error_when_called_with_type_change_then_returns_err_with_new_type(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.map_error(lambda e: len(e))

        assert result == Err(4)

    def test_flat_map_when_called_then_passes_through_unchanged(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.flat_map(lambda x: Ok(x + 1))

        assert result == Err("boom")

    def test_get_value_or_when_called_then_returns_default(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.get_value_or(42)

        assert result == 42

    def test_get_value_or_else_when_called_then_calls_fn_with_error(
        self, err_result: Err[int, str]
    ) -> None:
        result = err_result.get_value_or_else(lambda e: len(e))

        assert result == 4
