# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any, Self
from unittest.mock import AsyncMock, MagicMock

import pytest

from forging_blocks.application import CommandSenderPort
from forging_blocks.foundation.messages import Command, MessageMetadata


class FakeCommand(Command[str]):
    @property
    def value(self) -> str:
        return "foo"

    def _payload(self) -> dict[str, Any]:  # type: ignore[override]
        return {"foo": "foo"}

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.unit
class TestCommandSenderPortContract:
    """Contract tests verifying the CommandSenderPort protocol.

    Any object with an async ``send`` method accepting a ``Command``
    must satisfy this port.
    """

    async def test_send_when_called_with_command_then_completes(self) -> None:
        mock_sender = MagicMock(spec=CommandSenderPort)
        mock_sender.send = AsyncMock()
        command = FakeCommand()

        await mock_sender.send(command)

        mock_sender.send.assert_awaited_with(command)
