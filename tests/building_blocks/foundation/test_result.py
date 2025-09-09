import pytest

from building_blocks.foundation.result import Err, Ok, ResultAccessError


class TestResultAccessError:
    def test_cannot_access_value_when_err_then_returns_itself_cant_access_value(
        self,
    ) -> None:
        method_result = ResultAccessError.cannot_access_value()

        assert isinstance(method_result, ResultAccessError)
        assert method_result.message == "Cannot access value from an Err Result."

    def test_cannot_access_error_when_ok_then_returns_itself_cant_access_error(
        self,
    ) -> None:
        method_result = ResultAccessError.cannot_access_error()

        assert isinstance(method_result, ResultAccessError)
        assert method_result.message == "Cannot access error from an Ok Result."

    def test_message_property_returns_message(self) -> None:
        actual_message = "Test Message"

        error = ResultAccessError(actual_message)

        expected_message = "Test Message"
        assert error.message == expected_message

    def test_message_property_returns_default_message_when_none(self) -> None:
        error = ResultAccessError()

        expected_message = "ResultAccessError"
        assert error.message == expected_message


class TestOk:
    def test_is_ok_when_ok_then_return_true(self) -> None:
        result = Ok("value")

        is_ok = result.is_ok

        expected_is_ok = True
        assert is_ok is expected_is_ok

    def test_is_err_when_ok_then_return_false(self) -> None:
        result = Ok("value")

        is_err = result.is_err

        expected_is_err = False
        assert is_err is expected_is_err

    def test_value_property_returns_value(self) -> None:
        result = Ok("value")

        value = result.value

        expected_value = "value"
        assert value == expected_value

    def test_error_property_raises_result_access_error(self) -> None:
        result = Ok("value")

        with pytest.raises(ResultAccessError) as exc_info:
            _ = result.error

        assert str(exc_info.value) == "Cannot access error from an Ok Result."

    def test_repr_returns_expected_string(self) -> None:
        result = Ok("value")

        repr_string = repr(result)

        expected_repr = "Ok('value')"
        assert repr_string == expected_repr


class TestErr:
    def test_value_property_raises_result_access_error(self) -> None:
        result = Err("error")

        with pytest.raises(ResultAccessError) as exc_info:
            _ = result.value

        assert str(exc_info.value) == "Cannot access value from an Err Result."

    def test_error_property_returns_error(self) -> None:
        result = Err("error")

        error = result.error

        expected_error = "error"
        assert error == expected_error

    def test_is_err_when_err_then_return_true(self) -> None:
        result = Err("value")

        is_err = result.is_err

        expected_is_err = True
        assert is_err is expected_is_err

    def test_is_ok_when_err_then_return_false(self) -> None:
        result = Err("error")

        is_ok = result.is_ok

        expected_is_ok = False
        assert is_ok is expected_is_ok

    def test_repr_returns_expected_string(self) -> None:
        result = Err("error")

        repr_string = repr(result)

        expected_repr = "Err('error')"
        assert repr_string == expected_repr
