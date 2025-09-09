"""
Unit tests for the Command module.

Tests for Command class.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import pytest

from building_blocks.domain.messages.command import Command
from building_blocks.domain.messages.message import Message, MessageMetadata


class PayloadNotImplementedCommand(Command):
    pass


class FakeUserCommand(Command):
    def __init__(
        self,
        customer_id: str,
        amount: float,
        metadata: MessageMetadata | None = None,
    ):
        super().__init__(metadata)
        self._customer_id = customer_id
        self._amount = amount

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def _payload(self) -> dict[str, Any]:
        return {"customer_id": self._customer_id, "amount": self._amount}


class TestCommand:
    def test_inheritance_when_instantied_then_is_message(self):
        command = FakeUserCommand("customer_123", 99.99)

        assert isinstance(command, Message)
        assert isinstance(command, Command)

    def test_command_id_when_called_then_returns_message_id(self):
        command = FakeUserCommand("customer_123", 99.99)

        command_id = command.command_id

        assert command_id == command.message_id

    def test_issued_at_when_called_then_returns_created_at(self):
        command = FakeUserCommand("customer_123", 99.99)

        issued_at = command.issued_at

        assert issued_at == command.created_at

    def test_message_type_when_called_then_returns_command_class_name(self):
        command = FakeUserCommand("customer_123", 99.99)

        assert command.message_type == "FakeUserCommand"

    def test_to_dict_when_called_then_includes_command_payload(self):
        message_id = uuid4()
        created_at = datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc)
        metadata = MessageMetadata(message_id=message_id, created_at=created_at)

        command = FakeUserCommand("customer_123", 99.99, metadata=metadata)
        result = command.to_dict()

        expected = {
            "message_id": str(message_id),
            "created_at": "2025-06-11T19:36:06+00:00",
            "message_type": "FakeUserCommand",
            "payload": {
                "customer_id": "customer_123",
                "amount": 99.99,
            },
        }
        assert result == expected

    def test_payload_when_called_then_returns_command_data(self):
        command = FakeUserCommand("customer_123", 99.99)

        payload = command._payload

        expected = {"customer_id": "customer_123", "amount": 99.99}
        assert payload == expected

    def test_equality_when_same_command_id_then_true(self):
        metadata = MessageMetadata()

        command1 = FakeUserCommand("customer_123", 99.99, metadata=metadata)
        command2 = FakeUserCommand(
            "customer_456", 199.99, metadata=metadata
        )  # Different payload, same metadata

        assert command1 == command2  # Commands are equal by command_id, not domain data

    def test_domain_semantics_when_command_created_then_uses_imperative_naming(self):
        # This is more of a documentation test - commands should be named in imperative
        # mood
        command = FakeUserCommand("customer_123", 99.99)

        # The class name should suggest an action to perform
        # This test documents the expected naming convention
        assert "Command" in command.__class__.__name__
        assert hasattr(command, "issued_at")  # Commands have issued_at, not occurred_at
        assert hasattr(command, "command_id")  # Commands have command_id, not event_id

    def test_constructuor_when_payload_not_implemented_then_raises_type_error(self):
        with pytest.raises(TypeError):
            PayloadNotImplementedCommand()  # type: ignore
