"""Tests for the ErrorViewModel dataclass."""

import pytest

from forging_blocks.presentation import ErrorViewModel
from forging_blocks.presentation.errors.error_message_model import ErrorMessageModel


@pytest.mark.unit
class TestErrorViewModel:
    """Structural tests for ErrorViewModel."""

    def test_empty_view_model_has_no_messages(self) -> None:
        vm = ErrorViewModel()
        assert vm.messages == []

    def test_view_model_stores_multiple_messages(self) -> None:
        msg1 = ErrorMessageModel(title="Error 1")
        msg2 = ErrorMessageModel(title="Error 2")
        vm = ErrorViewModel(messages=[msg1, msg2])
        assert len(vm.messages) == 2
