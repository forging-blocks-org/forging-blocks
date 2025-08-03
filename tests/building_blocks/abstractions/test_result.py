import pytest

from building_blocks.abstractions.result import Err, Ok, ResultAccessError


class FakeOk(Ok[str]):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class FakeErr(Err[str]):
    def __init__(self, error: str) -> None:
        super().__init__(error)


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


class TestResult:
    def test_is_ok_when_ok_then_return_true(self) -> None:
        result = FakeOk("value")

        assert result.is_ok is True

    def test_is_ok_when_err_then_return_false(self) -> None:
        result = FakeErr("error")

        assert result.is_ok is False

    def test_is_err_when_ok_then_return_false(self) -> None:
        result = FakeOk("value")

        assert result.is_err is False

    def test_is_err_when_err_then_return_true(self) -> None:
        result = FakeErr("value")

        assert result.is_err is True


class TestOk:
    def test_value_property_returns_value(self) -> None:
        expected_value = "value"
        result = FakeOk(expected_value)

        assert result.value == expected_value

    def test_error_property_raises_result_access_error(self) -> None:
        result = FakeOk("value")

        with pytest.raises(ResultAccessError) as exc_info:
            _ = result.error

        assert str(exc_info.value) == "Cannot access error from an Ok Result."


class TestErr:
    def test_value_property_raises_result_access_error(self) -> None:
        result = FakeErr("error")

        with pytest.raises(ResultAccessError) as exc_info:
            _ = result.value

        assert str(exc_info.value) == "Cannot access value from an Err Result."

    def test_error_property_returns_error(self) -> None:
        expected_error = "error"
        result = FakeErr(expected_error)

        assert result.error == expected_error
