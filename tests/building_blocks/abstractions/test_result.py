import pytest

from building_blocks.abstractions.result import Err, Ok, Result, ResultAccessError


class FakeOk(Ok[str, None]):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class FakeErr(Err[None, str]):
    def __init__(self, error: str) -> None:
        super().__init__(error)


class TestResult:
    def test_value_when_ok_result_then_returns_value(self) -> None:
        # Arrange
        value = "success"
        result: Ok[str, str] = Ok(value)
        # Act
        actual_value = result.value
        # Assert
        assert actual_value == value

    def test_value_when_err_result_then_raises_result_access_error(self) -> None:
        # Arrange
        result: Err[str, str] = Err("failure")
        # Act / Assert
        with pytest.raises(ResultAccessError):
            _ = result.value

    def test_error_when_err_result_then_returns_error(self) -> None:
        # Arrange
        error = "failure"
        result: Err[str, str] = Err(error)
        # Act
        actual_error = result.error
        # Assert
        assert actual_error == error

    def test_error_when_ok_result_then_raises_result_access_error(self) -> None:
        # Arrange
        result: Ok[str, str] = Ok("success")
        # Act / Assert
        with pytest.raises(ResultAccessError):
            _ = result.error

    def test_repr_when_ok_result_then_returns_expected_string(self) -> None:
        # Arrange
        value = 42
        result: Ok[int, int] = Ok(value)
        # Act
        result_str = repr(result)
        # Assert
        assert result_str == "Ok(42)"

    def test_repr_when_err_result_then_returns_expected_string(self) -> None:
        # Arrange
        error = "bad things"
        result: Err[str, str] = Err(error)
        # Act
        result_str = repr(result)
        # Assert
        assert result_str == "Err('bad things')"

    def test_isinstance_when_ok_result_then_is_instance_of_ok_and_result(self) -> None:
        # Arrange
        result: Result[int, str] = Ok(5)
        # Act & Assert
        assert isinstance(result, Result)
        assert isinstance(result, Ok)

    def test_isinstance_when_err_result_then_is_instance_of_err_and_result(
        self,
    ) -> None:
        # Arrange
        result: Result[int, str] = Err("fail")
        # Act & Assert
        assert isinstance(result, Result)
        assert isinstance(result, Err)
