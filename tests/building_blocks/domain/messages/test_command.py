"""Unit tests for the Command module.

Tests for Command class.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import pytest

from building_blocks.domain.messages.command import Command
from building_blocks.domain.messages.message import Message, MessageMetadata


class PayloadAndValueNotImplCommand(Command):
    pass


class FakeUserCommand(Command[dict[str, Any]]):
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
    def value(self) -> dict[str, Any]:
        return self._payload

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

    def test_to_dict_when_called_then_includes_command_payload(self):
        message_id = uuid4()
        created_at = datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc)
        metadata = MessageMetadata(
            created_at=created_at, message_id=message_id, message_type="FakeUserCommand"
        )
        command = FakeUserCommand("customer_123", 99.99, metadata=metadata)

        result = command.to_dict()

        expected = {
            "metadata": {
                "message_id": str(message_id),
                "created_at": "2025-06-11T19:36:06+00:00",
                "message_type": "FakeUserCommand",
                "correlation_id": str(metadata.correlation_id),
                "causation_id": str(metadata.causation_id),
            },
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

    def test_domain_semantics_when_command_created_then_uses_imperative_naming(self):
        command = FakeUserCommand("customer_123", 99.99)

        assert "Command" in command.__class__.__name__
        assert hasattr(command, "issued_at")
        assert hasattr(command, "command_id")

    def test_constructuor_when_payload_not_implemented_then_raises_type_error(self):
        with pytest.raises(TypeError):
            PayloadAndValueNotImplCommand()  # type: ignore
