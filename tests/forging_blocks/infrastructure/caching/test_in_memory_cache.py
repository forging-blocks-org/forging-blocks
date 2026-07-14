"""Tests for the InMemoryCache adapter."""

import asyncio

import pytest

from forging_blocks.infrastructure.caching.in_memory_cache import InMemoryCache


@pytest.mark.unit
class TestInMemoryCache:
    """Tests for InMemoryCache implementation."""

    @pytest.fixture
    def cache(self) -> InMemoryCache[str, str]:
        """Create a fresh InMemoryCache instance."""
        return InMemoryCache[str, str]()

    async def test_get_nonexistent_key_returns_none(self, cache: InMemoryCache[str, str]) -> None:
        """Get on a nonexistent key should return None."""
        result = await cache.get("missing")
        assert result is None

    async def test_set_and_get(self, cache: InMemoryCache[str, str]) -> None:
        """Set a value and retrieve it."""
        await cache.set("key1", "value1")
        result = await cache.get("key1")
        assert result == "value1"

    async def test_set_overwrites_existing(self, cache: InMemoryCache[str, str]) -> None:
        """Setting an existing key should overwrite the value."""
        await cache.set("key1", "value1")
        await cache.set("key1", "value2")
        result = await cache.get("key1")
        assert result == "value2"

    async def test_delete(self, cache: InMemoryCache[str, str]) -> None:
        """Delete should remove a key."""
        await cache.set("key1", "value1")
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    async def test_delete_nonexistent_is_noop(self, cache: InMemoryCache[str, str]) -> None:
        """Deleting a nonexistent key should be a no-op."""
        await cache.delete("missing")
        assert await cache.get("missing") is None

    async def test_exists(self, cache: InMemoryCache[str, str]) -> None:
        """exists should return True for existing keys and False otherwise."""
        await cache.set("key1", "value1")
        assert await cache.exists("key1") is True
        assert await cache.exists("missing") is False

    async def test_clear(self, cache: InMemoryCache[str, str]) -> None:
        """Clear should remove all entries."""
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.clear()
        assert await cache.get("key1") is None
        assert await cache.get("key2") is None
        assert await cache.exists("key1") is False

    async def test_multiple_keys(self, cache: InMemoryCache[str, str]) -> None:
        """Multiple keys should coexist independently."""
        await cache.set("a", "1")
        await cache.set("b", "2")
        await cache.set("c", "3")
        assert await cache.get("a") == "1"
        assert await cache.get("b") == "2"
        assert await cache.get("c") == "3"

    async def test_generic_types(self) -> None:
        """InMemoryCache should work with non-string types."""
        cache: InMemoryCache[int, dict[str, int]] = InMemoryCache()
        await cache.set(42, {"answer": 42})
        result = await cache.get(42)
        assert result == {"answer": 42}

    async def test_ttl_expiration(self, cache: InMemoryCache[str, str]) -> None:
        """TTL should cause entries to expire."""
        await cache.set("key1", "value1", ttl=0.1)

        assert await cache.exists("key1") is True
        assert await cache.get("key1") == "value1"

        await asyncio.sleep(0.15)

        assert await cache.exists("key1") is False
        assert await cache.get("key1") is None

    async def test_no_ttl_does_not_expire(self, cache: InMemoryCache[str, str]) -> None:
        """Entries without TTL should not expire."""
        await cache.set("key1", "value1")

        await asyncio.sleep(0.05)

        assert await cache.exists("key1") is True
        assert await cache.get("key1") == "value1"
