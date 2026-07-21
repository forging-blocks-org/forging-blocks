"""Tests for the HttpClientPort outbound port.

These verify the HttpClientPort contract for HTTP client abstractions.
"""

import pytest

from forging_blocks.application.ports.outbound.http_client_port import HttpClientPort


@pytest.mark.unit
class TestHttpClientPort:
    """Contract tests for the HttpClientPort."""

    def test_http_client_is_abc(self) -> None:
        """HttpClientPort should be an ABC."""
        from abc import ABC as _ABC

        assert issubclass(HttpClientPort, _ABC)

    def test_http_client_has_request_method(self) -> None:
        """HttpClientPort should define the request method."""
        assert hasattr(HttpClientPort, "request")

    def test_http_client_has_get_method(self) -> None:
        """HttpClientPort should define the get convenience method."""
        assert hasattr(HttpClientPort, "get")

    def test_http_client_has_post_method(self) -> None:
        """HttpClientPort should define the post convenience method."""
        assert hasattr(HttpClientPort, "post")

    def test_http_client_has_put_method(self) -> None:
        """HttpClientPort should define the put convenience method."""
        assert hasattr(HttpClientPort, "put")

    def test_http_client_has_delete_method(self) -> None:
        """HttpClientPort should define the delete convenience method."""
        assert hasattr(HttpClientPort, "delete")
