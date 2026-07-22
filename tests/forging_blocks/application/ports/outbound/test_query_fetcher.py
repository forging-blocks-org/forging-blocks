"""Contract tests for QueryFetcherPort.

These tests verify that a concrete implementation of ``QueryFetcherPort``
correctly exposes the ``fetch`` contract.  The port itself declares an
``@abstractmethod`` — the ``FakeQueryFetcher`` fixture provides a real
implementation so tests exercise behaviour, not mock expectations.
"""

from __future__ import annotations

from typing import Self

import pytest

from forging_blocks.application import QueryFetcherPort
from forging_blocks.foundation import OutboundPort
from forging_blocks.foundation.messages import MessageMetadata, Query


class FakeQuery(Query[str]):
    @property
    def value(self) -> str:
        return "baz"

    @property
    def _payload(self) -> dict[str, object]:
        return {"foo": "bar"}

    @classmethod
    def _from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls()


class FakeQueryFetcher(QueryFetcherPort[str, str]):
    """Concrete fixture that implements ``fetch`` with a configurable result."""

    def __init__(self, result: str = "") -> None:
        self.result: str = result
        self.fetched_queries: list[Query[str]] = []

    async def fetch(self, query: Query[str]) -> str:
        self.fetched_queries.append(query)
        return self.result


@pytest.mark.unit
class TestQueryFetcherPortContract:
    """Any object with an async ``fetch`` accepting a ``Query`` satisfies this port."""

    def test_fake_fetcher_is_instance_of_outbound_port(self) -> None:
        """Concrete implementation passes structural isinstance checks."""
        fetcher = FakeQueryFetcher()
        assert isinstance(fetcher, OutboundPort)
        assert isinstance(fetcher, QueryFetcherPort)

    async def test_fetch_returns_configured_result(self) -> None:
        """The concrete fetcher returns the result it was configured with."""
        expected = "fetched_query_result"
        fetcher = FakeQueryFetcher(result=expected)
        query = FakeQuery()

        result = await fetcher.fetch(query)

        assert result == expected

    async def test_fetch_records_dispatched_query(self) -> None:
        """The concrete fetcher records the query it receives."""
        fetcher = FakeQueryFetcher()
        query = FakeQuery()

        await fetcher.fetch(query)

        assert query in fetcher.fetched_queries
        assert len(fetcher.fetched_queries) == 1
