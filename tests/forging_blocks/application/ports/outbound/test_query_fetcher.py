# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any, Self
from unittest.mock import AsyncMock, MagicMock

import pytest
from pytest import fixture

from forging_blocks.application import MessageBusPort, QueryFetcherPort
from forging_blocks.foundation.messages import MessageMetadata, Query


class FakeQuery(Query):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, Any]:
        return {"foo": "bar"}

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.unit
class TestQueryFetcher:
    @fixture
    def message_bus(self) -> MagicMock:
        bus = MagicMock(spec=MessageBusPort)
        bus.dispatch = AsyncMock()

        return bus

    async def test_fetch_when_called_then_call_message_bus_fetch_with_given_query(
        self, message_bus: MagicMock
    ) -> None:
        message_bus.dispatch.return_value = {"fetched": "query"}
        fetcher = QueryFetcherPort(message_bus)
        query = FakeQuery()

        result = await fetcher.fetch(query)

        expected_result = {"fetched": "query"}
        assert result == expected_result
        message_bus.dispatch.assert_awaited_with(query)
