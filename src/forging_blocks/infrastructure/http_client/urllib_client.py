"""Standard-library HTTP client implementation of HttpClientPort.

Uses ``urllib.request`` wrapped in ``asyncio.to_thread()`` to provide an
async HTTP client with zero external dependencies.

This adapter is constrained to ``str`` request/response bodies — it natively
encodes request bodies as UTF-8 and decodes response bodies as UTF-8. For
other content types (bytes, JSON, etc.), use a dedicated adapter or a
wrapper that handles serialization.
"""

import asyncio
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from forging_blocks.application.ports.outbound.http_client_port import (
    HttpClientPort,
)


class URLLibClient(HttpClientPort[str, str]):
    """HTTP client backed by Python's ``urllib.request`` + ``asyncio.to_thread``.

    This adapter provides async HTTP methods without requiring external
    dependencies like ``httpx`` or ``aiohttp``. Request and response bodies
    are encoded/decoded as UTF-8 strings.

    Note:
        For production use with high concurrency or non-string payloads,
        consider an adapter backed by ``httpx`` or ``aiohttp`` instead.

    Raises:
        urllib.error.HTTPError: On HTTP 4xx/5xx responses.
        urllib.error.URLError: On network/connection failures.
        ValueError: On malformed URLs.
    """

    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        body: str | None = None,
    ) -> str:
        """Send an HTTP request and return the response body as a string.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            url: The target URL.
            headers: Optional HTTP headers.
            body: Optional request body string (UTF-8 encoded).

        Returns:
            The response body decoded as UTF-8 string.

        Raises:
            HTTPError: On 4xx/5xx HTTP responses.
            URLError: On network or connection failures.
            ValueError: On malformed URLs.
        """
        http_headers: dict[str, str] = headers or {}
        data: bytes | None = body.encode("utf-8") if body is not None else None

        # Block non-HTTP schemes — urllib supports file:// which allows
        # reading arbitrary files if a caller-controlled URL is passed.
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                f"Disallowed URL scheme '{parsed.scheme}'. Only http and https are supported."
            )

        def _do_request() -> str:
            req = Request(url, data=data, headers=http_headers, method=method)
            with urlopen(req) as response:  # nosec B310 — scheme validated above
                return response.read().decode("utf-8")

        return await asyncio.to_thread(_do_request)

    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> str:
        """Send an HTTP GET request."""
        return await self.request("GET", url, headers=headers)

    async def post(
        self,
        url: str,
        body: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> str:
        """Send an HTTP POST request."""
        return await self.request("POST", url, headers=headers, body=body)

    async def put(
        self,
        url: str,
        body: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> str:
        """Send an HTTP PUT request."""
        return await self.request("PUT", url, headers=headers, body=body)

    async def delete(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> str:
        """Send an HTTP DELETE request."""
        return await self.request("DELETE", url, headers=headers)
