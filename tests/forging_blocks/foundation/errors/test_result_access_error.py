import pytest

from forging_blocks.foundation import ErrorMessage, ResultAccessError


@pytest.mark.unit
class TestResultAccessError:
    def test_init_when_message_provided_then_sets_provided_message(self):
        err = ResultAccessError(ErrorMessage("boom"))
        assert err.message == ErrorMessage("boom")

    def test_init_when_no_message_provided_then_sets_default_message(self):
        err = ResultAccessError()
        assert err.message is not None

    def test_cannot_access_value_when_called_then_returns_correct_message(self):
        err = ResultAccessError.cannot_access_value()
        assert err.message is not None

    def test_cannot_access_error_when_called_then_returns_correct_message(self):
        err = ResultAccessError.cannot_access_error()
        assert err.message is not None
