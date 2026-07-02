"""Tests for the ExternalServicePort outbound port.

These verify the ExternalServicePort contract for HTTP client abstractions.
"""

from typing import Protocol

import pytest

from forging_blocks.application.ports.outbound.external_service_port import ExternalServicePort


@pytest.mark.unit
class TestExternalServicePort:
    """Contract tests for the ExternalServicePort."""

    def test_external_service_is_protocol(self) -> None:
        """ExternalServicePort should be a Protocol."""
        assert isinstance(ExternalServicePort, type(Protocol))

    def test_external_service_has_request_method(self) -> None:
        """ExternalServicePort should define the request method."""
        assert hasattr(ExternalServicePort, "request")

    def test_external_service_has_get_method(self) -> None:
        """ExternalServicePort should define the get convenience method."""
        assert hasattr(ExternalServicePort, "get")

    def test_external_service_has_post_method(self) -> None:
        """ExternalServicePort should define the post convenience method."""
        assert hasattr(ExternalServicePort, "post")

    def test_external_service_has_put_method(self) -> None:
        """ExternalServicePort should define the put convenience method."""
        assert hasattr(ExternalServicePort, "put")

    def test_external_service_has_delete_method(self) -> None:
        """ExternalServicePort should define the delete convenience method."""
        assert hasattr(ExternalServicePort, "delete")
