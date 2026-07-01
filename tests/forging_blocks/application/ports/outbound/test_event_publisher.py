# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Self
from unittest.mock import AsyncMock, MagicMock

import pytest

from forging_blocks.application import EventPublisherPort
from forging_blocks.foundation.messages import Event, MessageMetadata


class FakeEvent(Event):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, str]:
        return {"foo": "bar"}

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.unit
class TestEventPublisherPortContract:
    """Contract tests verifying the EventPublisherPort protocol.

    Any object with an async ``publish`` method accepting an ``Event``
    must satisfy this port.
    """

    async def test_publish_when_called_with_event_then_completes(self) -> None:
        mock_publisher = MagicMock(spec=EventPublisherPort)
        mock_publisher.publish = AsyncMock()
        event = FakeEvent()

        await mock_publisher.publish(event)

        mock_publisher.publish.assert_awaited_with(event)
