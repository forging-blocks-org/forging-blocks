# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any, Self
from unittest.mock import AsyncMock, MagicMock

import pytest

from forging_blocks.application import MessageBusPort, QueryFetcherPort
from forging_blocks.foundation.messages import MessageMetadata, Query
from forging_blocks.infrastructure import MessageBusQueryFetcher


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


@pytest.mark.integration
class TestMessageBusQueryFetcher:
    """Integration tests for the MessageBusQueryFetcher adapter."""

    def test_init_when_called_then_stores_message_bus(self) -> None:
        bus = MagicMock(spec=MessageBusPort)

        fetcher = MessageBusQueryFetcher(bus)

        assert fetcher._message_bus is bus

    async def test_fetch_when_called_then_delegates_to_message_bus_dispatch(self) -> None:
        bus = MagicMock(spec=MessageBusPort)
        expected_result = {"fetched": "query"}
        bus.dispatch = AsyncMock(return_value=expected_result)
        fetcher = MessageBusQueryFetcher(bus)
        query = FakeQuery()

        result = await fetcher.fetch(query)

        assert result is expected_result
        bus.dispatch.assert_awaited_once_with(query)

    async def test_implements_query_fetcher_port(self) -> None:
        """MessageBusQueryFetcher satisfies the QueryFetcherPort protocol."""
        bus = MagicMock(spec=MessageBusPort)
        fetcher = MessageBusQueryFetcher(bus)

        assert isinstance(fetcher, QueryFetcherPort)
