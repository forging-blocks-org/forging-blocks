# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation import Err, ErrorMessage, Ok, ResultAccessError


@pytest.mark.unit
class TestOk:
    @pytest.fixture
    def ok_result(self) -> Ok[int, str]:
        return Ok(123)

    def test___init___when_value_is_given_then_stores_it(self, ok_result: Ok[int, str]) -> None:
        # Arrange done by fixture

        # Act
        result = ok_result._value

        # Assert
        assert result == 123

    def test_is_err_when_called_then_returns_false(self, ok_result: Ok[int, str]) -> None:
        # Arrange

        # Act
        result = ok_result.is_err

        # Assert
        assert result is False

    def test_is_ok_when_called_then_returns_true(self, ok_result: Ok[int, str]) -> None:
        # Arrange

        # Act
        result = ok_result.is_ok

        # Assert
        assert result is True

    def test_value_when_accessed_then_returns_inner_value(self, ok_result: Ok[int, str]) -> None:
        # Arrange

        # Act
        result = ok_result.value

        # Assert
        assert result == 123

    def test_error_when_accessed_then_raises_result_access_error(
        self, ok_result: Ok[int, str]
    ) -> None:
        # Arrange / Act / Assert
        with pytest.raises(ResultAccessError) as exc_info:
            _ = ok_result.error
        # Assert
        assert "Cannot access error" in str(exc_info.value)

    def test___repr___when_called_then_returns_readable_representation(
        self, ok_result: Ok[int, str]
    ) -> None:
        # Arrange

        # Act
        result = ok_result.__repr__()

        # Assert
        assert result == "Ok(123)"

    def test___eq___when_comparing_two_equal_ok_results_then_returns_true(self) -> None:
        # Arrange
        a = Ok(1)
        b = Ok(1)

        # Act
        result = a.__eq__(b)

        # Assert
        assert result is True

    def test___eq___when_comparing_different_ok_results_then_returns_false(
        self,
    ) -> None:
        # Arrange
        a = Ok(1)
        b = Ok(2)

        # Act
        result = a.__eq__(b)

        # Assert
        assert result is False

    def test___eq___when_comparing_with_different_class_then_returns_not_implemented(
        self,
    ) -> None:
        # Arrange
        ok = Ok(1)
        other = object()
        # Act
        result = ok.__eq__(other)
        # Assert
        assert result is False

    def test___hash___when_called_then_returns_hash_of_inner_value(
        self, ok_result: Ok[int, str]
    ) -> None:
        # Arrange

        # Act
        result = ok_result.__hash__()

        # Assert
        assert result == hash(123)

    def test___str___when_called_then_returns_string_representation(
        self, ok_result: Ok[int, str]
    ) -> None:
        # Arrange

        # Act
        result = ok_result.__str__()

        # Assert
        assert result == "Ok(123)"


@pytest.mark.unit
class TestErr:
    @pytest.fixture
    def err_result(self) -> Err[int, str]:
        return Err("boom")

    def test___init___when_error_is_given_then_stores_it(self, err_result: Err[int, str]) -> None:
        # Arrange done by fixture

        # Act
        result = err_result._error

        # Assert
        assert result == "boom"

    def test_is_err_when_called_then_returns_true(self, err_result: Err[int, str]) -> None:
        # Arrange

        # Act
        result = err_result.is_err

        # Assert
        assert result is True

    def test_is_ok_when_called_then_returns_false(self, err_result: Err[int, str]) -> None:
        # Arrange

        # Act
        result = err_result.is_ok

        # Assert
        assert result is False

    def test_value_when_accessed_then_raises_result_access_error(
        self, err_result: Err[int, str]
    ) -> None:
        # Arrange / Act / Assert
        with pytest.raises(ResultAccessError) as exc_info:
            _ = err_result.value
        # Assert
        assert "Cannot access value" in str(exc_info.value)

    def test_error_when_accessed_then_returns_inner_error(self, err_result: Err[int, str]) -> None:
        # Arrange

        # Act
        result = err_result.error

        # Assert
        assert result == "boom"

    def test___repr___when_called_then_returns_readable_representation(
        self, err_result: Err[int, str]
    ) -> None:
        # Arrange

        # Act
        result = err_result.__repr__()

        # Assert
        assert result == "Err('boom')"

    def test___eq___when_comparing_two_equal_err_results_then_returns_true(
        self,
    ) -> None:
        # Arrange
        a = Err("x")
        b = Err("x")

        # Act
        result = a.__eq__(b)

        # Assert
        assert result is True

    def test___eq___when_comparing_different_err_results_then_returns_false(
        self,
    ) -> None:
        # Arrange
        a = Err("x")
        b = Err("y")

        # Act
        result = a.__eq__(b)

        # Assert
        assert result is False

    def test___eq___when_comparing_err_with_different_class_then_returns_false(
        self,
    ) -> None:
        # Arrange
        err = Err("boom")
        other = object()

        # Act
        result = err.__eq__(other)

        # Assert
        assert result is False

    def test___hash___when_called_then_returns_hash_of_inner_error(
        self, err_result: Err[int, str]
    ) -> None:
        # Arrange

        # Act
        result = err_result.__hash__()

        # Assert
        assert result == hash("boom")

    def test___str___when_called_then_returns_string_representation(
        self, err_result: Err[int, str]
    ) -> None:
        # Arrange

        # Act
        result = err_result.__str__()

        # Assert
        # After you fix Err.__str__ to return "Err(...)" instead of "Ok(...)"
        assert result == "Err(boom)"
