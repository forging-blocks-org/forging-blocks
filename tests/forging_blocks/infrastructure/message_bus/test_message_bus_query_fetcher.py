# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any, Self

import pytest

from forging_blocks.foundation.messages import MessageMetadata, Query
from forging_blocks.infrastructure import MessageBusQueryFetcher
from tests.fixtures.fake_message_bus import FakeMessageBus


class FakeQuery(Query):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, Any]:
        return {"foo": "bar"}

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


@pytest.mark.integration
class TestMessageBusQueryFetcher:
    """Integration tests for the MessageBusQueryFetcher adapter."""

    @pytest.fixture
    def expected_result(self) -> dict[str, str]:
        return {"fetched": "query"}

    @pytest.fixture
    def fake_bus(self, expected_result: dict[str, str]) -> FakeMessageBus:
        return FakeMessageBus(dispatch_result=expected_result)

    @pytest.fixture
    def fetcher(self, fake_bus: FakeMessageBus) -> MessageBusQueryFetcher:
        return MessageBusQueryFetcher(fake_bus)

    @pytest.fixture
    def query(self) -> FakeQuery:
        return FakeQuery()

    def test_init_when_called_then_stores_message_bus(self, fake_bus: FakeMessageBus) -> None:
        fetcher = MessageBusQueryFetcher(fake_bus)

        assert fetcher._message_bus is fake_bus

    async def test_fetch_when_called_then_delegates_to_message_bus_dispatch(
        self,
        fetcher: MessageBusQueryFetcher,
        query: FakeQuery,
        fake_bus: FakeMessageBus,
        expected_result: dict[str, str],
    ) -> None:
        result = await fetcher.fetch(query)

        assert result is expected_result
        assert len(fake_bus.dispatched_messages) == 1
        assert fake_bus.dispatched_messages[0] is query

    def test_implements_query_fetcher_port(self) -> None:
        """MessageBusQueryFetcher satisfies the QueryFetcherPort protocol."""
        assert hasattr(MessageBusQueryFetcher, "fetch")
