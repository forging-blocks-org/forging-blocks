"""Tests for the CachePort outbound port.

These verify the CachePort protocol contract for caching abstractions.
"""

from typing import Protocol

import pytest

from forging_blocks.application.ports.outbound.cache import CachePort


@pytest.mark.unit
class TestCachePort:
    """Contract tests for the CachePort protocol."""

    def test_cache_is_protocol(self) -> None:
        """CachePort should be a Protocol."""
        assert isinstance(CachePort, type(Protocol))

    def test_cache_has_get_method(self) -> None:
        """CachePort should define the get method."""
        assert hasattr(CachePort, "get")

    def test_cache_has_set_method(self) -> None:
        """CachePort should define the set method."""
        assert hasattr(CachePort, "set")

    def test_cache_has_delete_method(self) -> None:
        """CachePort should define the delete method."""
        assert hasattr(CachePort, "delete")

    def test_cache_has_exists_method(self) -> None:
        """CachePort should define the exists method."""
        assert hasattr(CachePort, "exists")

    def test_cache_has_clear_method(self) -> None:
        """CachePort should define the clear method."""
        assert hasattr(CachePort, "clear")
