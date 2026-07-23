"""Unit tests for message dataclass decorators."""

import pytest


@pytest.mark.unit
class TestMessageDataclassDecorator:
    """Tests for the message_dataclass decorator internals."""

    def test_message_dataclass_when_patched_message_check_fails_then_type_error(
        self,
    ) -> None:
        from unittest.mock import patch

        from forging_blocks.foundation.messages.decorators import (
            _PatchedMessage,  # pyright: ignore[reportPrivateUsage]
            message_dataclass,
        )

        class NotAMessage:
            x: int

        original_isinstance = isinstance

        def _selective_isinstance(obj: object, cls: type) -> bool:
            if cls is _PatchedMessage:
                return False
            return original_isinstance(obj, cls)

        with patch(
            "forging_blocks.foundation.messages.decorators.isinstance",
            side_effect=_selective_isinstance,
        ):
            with pytest.raises(TypeError, match="does not satisfy _PatchedMessage"):
                message_dataclass(NotAMessage)  # type: ignore[reportArgumentType]
