from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from pytest import fixture

from forging_blocks.application import MessageBus, QueryFetcher
from forging_blocks.domain import Query


class FakeQuery(Query):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, Any]:
        return {"foo": "bar"}


@pytest.mark.unit
class TestQueryFetcher:
    @fixture
    def message_bus(self) -> MagicMock:
        bus = MagicMock(spec=MessageBus)
        bus.dispatch = AsyncMock()

        return bus

    async def test_fetch_when_called_then_call_message_bus_fetch_with_given_query(
        self, message_bus: MagicMock
    ) -> None:
        message_bus.dispatch.return_value = {"fetched": "query"}
        fetcher = QueryFetcher(message_bus)
        query = FakeQuery()

        result = await fetcher.fetch(query)

        expected_result = {"fetched": "query"}
        assert result == expected_result
        message_bus.dispatch.assert_awaited_with(query)
