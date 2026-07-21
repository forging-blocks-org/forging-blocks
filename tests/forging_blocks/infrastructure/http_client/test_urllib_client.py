"""Tests for the URLLibClient adapter."""

import asyncio
import inspect
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

import pytest

from forging_blocks.infrastructure.http_client.urllib_client import URLLibClient


class _EchoHandler(SimpleHTTPRequestHandler):
    """Handler that echoes request info back as text for testing."""

    def _respond(self, status: int = 200) -> None:
        body = f"method={self.command}\\npath={self.path}\\nheaders={dict(self.headers)}\\n"
        content_length = self.headers.get("Content-Length")
        if content_length:
            raw = self.rfile.read(int(content_length))
            body += f"body={raw.decode('utf-8')}"
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self) -> None:
        self._respond()

    def do_POST(self) -> None:
        self._respond()

    def do_PUT(self) -> None:
        self._respond()

    def do_DELETE(self) -> None:
        self._respond()

    def do_PATCH(self) -> None:
        self._respond()

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()


@pytest.fixture(scope="module")
def echo_server():
    """Start a local HTTP server that echoes requests; returns base URL."""
    server = HTTPServer(("127.0.0.1", 0), _EchoHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[0], server.server_address[1]
    url = f"http://{host}:{port}"
    yield url
    server.shutdown()
    thread.join(timeout=2)


@pytest.fixture
def client() -> URLLibClient:
    return URLLibClient()


@pytest.mark.unit
class TestURLLibClientUnit:
    """Tests that do not require a running server."""

    def test_creation(self, client: URLLibClient) -> None:
        assert client is not None

    def test_methods_are_callable(self, client: URLLibClient) -> None:
        for name in ("request", "get", "post", "put", "delete"):
            assert callable(getattr(client, name)), f"{name} is not callable"

    def test_methods_are_async(self, client: URLLibClient) -> None:
        for name in ("request", "get", "post", "put", "delete"):
            assert inspect.iscoroutinefunction(getattr(client, name)), f"{name} is not async"

    @pytest.mark.parametrize(
        "url",
        [
            "file:///etc/passwd",
            "file:///C:/windows/win.ini",
            "ftp://example.com/file",
            "gopher://localhost/",
            "data:text/plain,hello",
        ],
    )
    async def test_request_rejects_non_http_schemes(self, client: URLLibClient, url: str) -> None:
        with pytest.raises(ValueError, match="Disallowed URL scheme"):
            await client.request("GET", url)


@pytest.mark.integration
class TestURLLibClientIntegration:
    """Integration tests against a local echo server."""

    async def test_get_returns_response(self, client: URLLibClient, echo_server: str) -> None:
        url = f"{echo_server}/test-resource"
        result = await client.get(url)

        assert "method=GET" in result
        assert "path=/test-resource" in result

    async def test_get_with_headers(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.get(
            f"{echo_server}/headers",
            headers={"X-Custom": "test-value", "Accept": "text/plain"},
        )

        assert "'x-custom': 'test-value'" in result.lower()

    async def test_post_sends_body(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.post(f"{echo_server}/create", body="hello-world")

        assert "method=POST" in result
        assert "body=hello-world" in result

    async def test_post_with_headers(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.post(
            f"{echo_server}/json",
            body='{"key":"value"}',
            headers={"Content-Type": "application/json"},
        )

        assert "method=POST" in result
        assert "application/json" in result

    async def test_put_sends_body(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.put(f"{echo_server}/update", body="updated-data")

        assert "method=PUT" in result
        assert "body=updated-data" in result

    async def test_put_without_body(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.put(f"{echo_server}/touch")

        assert "method=PUT" in result

    async def test_delete_returns_response(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.delete(f"{echo_server}/remove")

        assert "method=DELETE" in result

    async def test_delete_with_headers(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.delete(
            f"{echo_server}/secure-remove",
            headers={"Authorization": "Bearer token123"},
        )

        assert "method=DELETE" in result
        assert "bearer token123" in result.lower()

    async def test_request_allows_http_schemes(
        self, client: URLLibClient, echo_server: str
    ) -> None:
        """http and https should not be rejected by the scheme guard."""
        result = await client.request("GET", f"{echo_server}/ok")
        assert "method=GET" in result

    async def test_request_raw_method(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.request("PATCH", f"{echo_server}/patch", body="raw")

        assert "method=PATCH" in result
        assert "body=raw" in result

    async def test_request_without_body(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.request("HEAD", f"{echo_server}/head")

        assert result == ""

    async def test_request_without_headers(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.request("GET", f"{echo_server}/no-headers")

        assert "method=GET" in result

    async def test_get_is_async(self, client: URLLibClient, echo_server: str) -> None:
        result = await client.get(f"{echo_server}/async-check")

        assert inspect.iscoroutinefunction(client.get)
        assert "method=GET" in result

    async def test_concurrent_requests(self, client: URLLibClient, echo_server: str) -> None:
        urls = [f"{echo_server}/c{i}" for i in range(3)]
        tasks = [client.get(u) for u in urls]
        results = await asyncio.gather(*tasks)

        assert len(results) == 3
        for i, r in enumerate(results):
            assert f"path=/c{i}" in r
