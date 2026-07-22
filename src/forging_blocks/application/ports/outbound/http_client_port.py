"""HTTP client port for abstract HTTP client operations.

Defines the ``HttpClientPort`` that application code depends on,
decoupling HTTP requests from any specific client implementation.

Responsibilities:
    - Send HTTP requests (GET, POST, PUT, DELETE) to external services.
    - Abstract transport details (HTTP libraries, connection pooling).

Non-Responsibilities:
    - Retry logic or circuit-breaking (handled by infrastructure/decorators).
    - Serialization or deserialization of request/response bodies.
    - Service discovery or URL resolution.
"""

from abc import abstractmethod

from forging_blocks.foundation.ports import OutboundPort


class HttpClientPort[RequestType, ResponseType](
    OutboundPort,
):
    """ABC for making HTTP requests to external services.

    Any object with the async ``request``, ``get``, ``post``, ``put``,
    and ``delete`` methods satisfies this protocol — no inheritance required.

    Type Parameters:
        RequestType: The type of the request body.
        ResponseType: The type of the response body.
    """

    @abstractmethod
    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        body: RequestType | None = None,
    ) -> ResponseType:
        """Send an HTTP request with the given method, URL, and optional body.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.).
            url: The target URL.
            headers: Optional HTTP headers.
            body: Optional request body.

        Returns:
            The response body of type ResponseType.

        """
        ...

    @abstractmethod
    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> ResponseType:
        """Send an HTTP GET request.

        Args:
            url: The target URL.
            headers: Optional HTTP headers.

        Returns:
            The response body of type ResponseType.

        """
        ...

    @abstractmethod
    async def post(
        self,
        url: str,
        body: RequestType | None = None,
        headers: dict[str, str] | None = None,
    ) -> ResponseType:
        """Send an HTTP POST request.

        Args:
            url: The target URL.
            body: The request body.
            headers: Optional HTTP headers.

        Returns:
            The response body of type ResponseType.

        """
        ...

    @abstractmethod
    async def put(
        self,
        url: str,
        body: RequestType | None = None,
        headers: dict[str, str] | None = None,
    ) -> ResponseType:
        """Send an HTTP PUT request.

        Args:
            url: The target URL.
            body: The request body.
            headers: Optional HTTP headers.

        Returns:
            The response body of type ResponseType.

        """
        ...

    @abstractmethod
    async def delete(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> ResponseType:
        """Send an HTTP DELETE request.

        Args:
            url: The target URL.
            headers: Optional HTTP headers.

        Returns:
            The response body of type ResponseType.

        """
        ...
