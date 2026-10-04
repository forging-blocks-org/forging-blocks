# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

"""Unit tests for message dataclass decorators."""

from typing import Self, cast

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

        a = Shipped(
            tracking_code="TRK-001",
            metadata=MessageMetadata(message_type="Shipped", message_id=shared_id),
        )
        b = Shipped(
            tracking_code="TRK-002",
            metadata=MessageMetadata(message_type="Shipped", message_id=shared_id),
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

    def test_from_payload_fields_raises_typeerror_when_unknown_keys_present(self) -> None:
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event
        from forging_blocks.domain.messages.message import MessageMetadata

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        with pytest.raises(TypeError, match="Unknown field"):
            Shipped.from_payload_fields(
                {"tracking_code": "TRK-001", "garbage": "bad"},
                MessageMetadata(message_type="Shipped", message_id="test-id"),
            )

    def test_from_payload_fields_succeeds_when_all_keys_match(self) -> None:
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event
        from forging_blocks.domain.messages.message import MessageMetadata

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        result = Shipped.from_payload_fields(
            {"tracking_code": "TRK-001"},
            MessageMetadata(message_type="Shipped", message_id="test-id"),
        )
        assert result.tracking_code == "TRK-001"
        assert result.metadata.message_type == "Shipped"

    def test_get_payload_fields_returns_non_private_dataclass_fields(self) -> None:
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        msg = Shipped(tracking_code="TRK-001")
        result = msg.get_payload_fields()
        assert result == {"tracking_code": "TRK-001"}

    def test_setattr_on_frozen_message_raises_frozen_instance_error(self) -> None:
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        msg = Shipped(tracking_code="TRK-001")
        import dataclasses

        with pytest.raises(dataclasses.FrozenInstanceError, match="cannot assign to field"):
            msg.tracking_code = "changed"

    def test_delattr_on_frozen_message_raises_frozen_instance_error(self) -> None:
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        msg = Shipped(tracking_code="TRK-001")
        import dataclasses

        with pytest.raises(dataclasses.FrozenInstanceError, match="cannot delete field"):
            del msg.tracking_code

    def test_marker_mutation_on_frozen_message_raises_frozen_instance_error(self) -> None:
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event

        @event_dataclass
        class Shipped(Event[dict[str, object]]):
            tracking_code: str

        msg = Shipped(tracking_code="TRK-001")
        import dataclasses

        with pytest.raises(dataclasses.FrozenInstanceError, match="cannot delete field"):
            delattr(msg, "__init_finished__")

        with pytest.raises(dataclasses.FrozenInstanceError, match="cannot assign to field"):
            msg.__setattr__("__init_finished__", False)

    def test_delattr_during_message_initialization_is_allowed(self) -> None:
        from forging_blocks.domain.messages.decorators import event_dataclass
        from forging_blocks.domain.messages.event import Event
        from forging_blocks.domain.messages.message import MessageMetadata

        @event_dataclass
        class Discarded(Event[dict[str, object]]):
            tracking_code: str

            def __init__(self, tracking_code: str) -> None:
                object.__setattr__(self, "tracking_code", tracking_code)
                del self.tracking_code
                super().__init__()

            @property
            def _payload(self) -> dict[str, object]:
                return {"tracking_code": self.tracking_code}

            @classmethod
            def from_payload_fields(
                cls,
                data: dict[str, object],
                metadata: MessageMetadata,
            ) -> Self:
                message = cls(tracking_code=cast(str, data["tracking_code"]))
                object.__setattr__(message, "_metadata", metadata)
                return message

            @property
            def value(self) -> dict[str, object]:
                return self._payload

        message = Discarded(tracking_code="TRK-001")

        assert not hasattr(message, "tracking_code")
