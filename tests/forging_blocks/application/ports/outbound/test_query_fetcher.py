# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from typing import Any, Self
from unittest.mock import AsyncMock, MagicMock

import pytest

from forging_blocks.application import QueryFetcherPort
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
class TestQueryFetcherPortContract:
    """Contract tests verifying the QueryFetcherPort protocol.

    Any object with an async ``fetch`` method accepting a ``Query``
    and returning a result must satisfy this port.
    """

    async def test_fetch_when_called_with_query_then_returns_result(self) -> None:
        mock_fetcher = MagicMock(spec=QueryFetcherPort)
        expected_result = {"fetched": "query"}
        mock_fetcher.fetch = AsyncMock(return_value=expected_result)
        query = FakeQuery()

        result = await mock_fetcher.fetch(query)

        assert result == expected_result
        mock_fetcher.fetch.assert_awaited_with(query)
