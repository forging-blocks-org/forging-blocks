# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

"""Unit tests for message dataclass decorators."""

from typing import cast

import pytest

from forging_blocks.domain.messages.message import Message


@pytest.mark.unit
class TestMessageDataclassDecorator:
    """Tests for the message_dataclass decorator internals."""

    def test_message_dataclass_when_patched_message_check_fails_then_type_error(
        self,
    ) -> None:
        from unittest.mock import patch

        from forging_blocks.domain.messages.decorators import (
            _PatchedMessage,
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
            "forging_blocks.domain.messages.decorators.isinstance",
            side_effect=_selective_isinstance,
        ):
            with pytest.raises(TypeError, match="does not satisfy _PatchedMessage"):
                message_dataclass(cast(type[Message[object]], NotAMessage))

    def test_decorated_messages_preserve_message_equality_by_id(self) -> None:
        """Two decorated messages with the same message_id are equal, regardless of field data."""
        import uuid

        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event
        from forging_blocks.domain.messages.message import MessageMetadata

        shared_id = uuid.uuid4()

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        # Same message_id, different field data — must be equal
        a = Shipped(
            tracking_code="TRK-001",
            metadata=MessageMetadata(
                message_type="Shipped",
                message_id=shared_id,
            ),
        )
        b = Shipped(
            tracking_code="TRK-002",
            metadata=MessageMetadata(
                message_type="Shipped",
                message_id=shared_id,
            ),
        )

        assert a.tracking_code != b.tracking_code, "precondition: field data differs"
        assert a == b, "messages with same message_id should be equal"
        assert hash(a) == hash(b), "messages with same message_id should have equal hashes"

    def test_decorated_messages_differ_by_message_id(self) -> None:
        """Two decorated messages with different message_ids are not equal, even if field data matches."""
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        a = Shipped(tracking_code="TRK-001")
        b = Shipped(tracking_code="TRK-001")

        assert a != b, "messages with different message_ids should not be equal"
