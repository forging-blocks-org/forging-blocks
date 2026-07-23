"""Unit tests for the Command module.

Tests for Command class.
"""
# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false

from typing import Any, Self

import pytest

from forging_blocks.foundation.messages import Command, Message, MessageMetadata


class PayloadAndValueNotImplCommand(Command):
    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


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

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(
            customer_id=str(data.get("customer_id", "")),
            amount=float(str(data.get("amount", 0.0))),
            metadata=metadata,
        )


@pytest.mark.unit
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
