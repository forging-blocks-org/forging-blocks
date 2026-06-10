# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
import pytest

from forging_blocks.foundation import ErrorMessage, ResultAccessError


@pytest.mark.unit
class TestResultAccessError:
    @pytest.fixture
    def base_error(self) -> ResultAccessError:
        return ResultAccessError()

    def test___init___when_no_message_given_then_sets_default_message(
        self, base_error: ResultAccessError
    ) -> None:
        result = base_error.message

        assert "Invalid access" in result.value

    def test___init___when_message_is_error_message_then_uses_str(self) -> None:
        msg = ErrorMessage("custom")

        error = ResultAccessError(msg)

        expected_error_message = ErrorMessage("custom")
        assert expected_error_message == error.message

    def test_cannot_access_value_when_called_then_returns_instance_with_specific_message(
        self,
    ) -> None:
        error = ResultAccessError.cannot_access_value()

        assert isinstance(error, ResultAccessError)
        assert "Cannot access value" in error.message.value

    def test_cannot_access_error_when_called_then_returns_instance_with_specific_message(
        self,
    ) -> None:
        error = ResultAccessError.cannot_access_error()

        assert isinstance(error, ResultAccessError)
        assert "Cannot access error" in error.message.value
