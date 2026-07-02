"""Tests for the URLLibClient adapter."""

import inspect

import pytest

from forging_blocks.infrastructure.http_client.urllib_client import URLLibClient


@pytest.mark.unit
class TestURLLibClient:
    """Tests for URLLibClient implementation."""

    def test_creation(self) -> None:
        """URLLibClient should be instantiable."""
        client = URLLibClient()
        assert client is not None

    def test_has_request_method(self) -> None:
        """URLLibClient should have request method."""
        client = URLLibClient()
        assert callable(client.request)

    def test_has_get_method(self) -> None:
        """URLLibClient should have get method."""
        client = URLLibClient()
        assert callable(client.get)

    def test_has_post_method(self) -> None:
        """URLLibClient should have post method."""
        client = URLLibClient()
        assert callable(client.post)

    def test_has_put_method(self) -> None:
        """URLLibClient should have put method."""
        client = URLLibClient()
        assert callable(client.put)

    def test_has_delete_method(self) -> None:
        """URLLibClient should have delete method."""
        client = URLLibClient()
        assert callable(client.delete)

    def test_methods_are_async(self) -> None:
        """All HTTP methods should be async (coroutine functions)."""
        client = URLLibClient()
        assert inspect.iscoroutinefunction(client.request)
        assert inspect.iscoroutinefunction(client.get)
        assert inspect.iscoroutinefunction(client.post)
        assert inspect.iscoroutinefunction(client.put)
        assert inspect.iscoroutinefunction(client.delete)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_returns_response_body(self) -> None:
        """GET should return a string response body for a real HTTP request."""
        client = URLLibClient()
        try:
            result = await client.get("https://httpbin.org/get")
            assert isinstance(result, str)
            assert len(result) > 0
        except OSError:
            pytest.skip("httpbin.org not reachable")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_with_headers(self) -> None:
        """GET should send custom headers."""
        client = URLLibClient()
        try:
            result = await client.get(
                "https://httpbin.org/headers",
                headers={"X-Custom": "test-value"},
            )
            assert "X-Custom" in result
            assert "test-value" in result
        except OSError:
            pytest.skip("httpbin.org not reachable")
