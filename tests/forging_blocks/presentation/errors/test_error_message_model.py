"""Tests for the ErrorMessageModel dataclass."""

import pytest

from forging_blocks.presentation.errors.error_message_model import ErrorMessageModel


@pytest.mark.unit
class TestErrorMessageModel:
    """Structural tests for ErrorMessageModel dataclass."""

    def test_equality_by_value(self) -> None:
        a = ErrorMessageModel(title="x")
        b = ErrorMessageModel(title="x")
        assert a == b

    def test_inequality_when_title_differs(self) -> None:
        a = ErrorMessageModel(title="x")
        b = ErrorMessageModel(title="y")
        assert a != b

    def test_defaults_are_none(self) -> None:
        msg = ErrorMessageModel(title="title only")
        assert msg.detail is None
        assert msg.field is None
        assert msg.code is None
