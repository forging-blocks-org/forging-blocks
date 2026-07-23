"""Contract tests for CommandSenderPort.

These tests verify that a concrete implementation of ``CommandSenderPort``
correctly exposes the ``send`` contract.  The port itself declares an
``@abstractmethod`` — the ``FakeCommandSender`` fixture provides a real
implementation so tests exercise behaviour, not mock expectations.
"""

from __future__ import annotations

from typing import Self

import pytest

from forging_blocks.application import CommandSenderPort
from forging_blocks.domain.messages import Command, MessageMetadata
from forging_blocks.foundation import OutboundPort


class FakeCommand(Command[str]):
    @property
    def value(self) -> str:
        return "foo"

    @property
    def _payload(self) -> dict[str, object]:
        return {"foo": "foo"}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


class FakeCommandSender(CommandSenderPort[str]):
    """Concrete fixture that implements ``send`` and records dispatched commands."""

    def __init__(self) -> None:
        self.sent: list[Command[str]] = []

    async def send(self, command: Command[str]) -> None:
        self.sent.append(command)


@pytest.mark.unit
class TestCommandSenderPortContract:
    """Any object with an async ``send`` accepting a ``Command`` satisfies this port."""

    def test_fake_sender_is_instance_of_outbound_port(self) -> None:
        """Concrete implementation passes structural isinstance checks."""
        sender = FakeCommandSender()
        assert isinstance(sender, OutboundPort)
        assert isinstance(sender, CommandSenderPort)

    async def test_send_dispatches_command_to_fixture(self) -> None:
        """The concrete sender records the command it receives."""
        sender = FakeCommandSender()
        command = FakeCommand()

        await sender.send(command)

        assert command in sender.sent
        assert len(sender.sent) == 1
