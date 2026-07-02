"""In-memory cache implementation of the CachePort."""

import time

from forging_blocks.application.ports.outbound.cache_port import CachePort


class InMemoryCache[KeyType, ValueType](CachePort[KeyType, ValueType]):
    """Cache implementation backed by an in-memory dictionary.

    Supports optional TTL (time-to-live) for cache entries.
    Expired entries are removed lazily on access.
    """

    def __init__(self) -> None:
        self._store: dict[KeyType, tuple[ValueType, float | None]] = {}

    def _get_entry(self, key: KeyType) -> tuple[ValueType, float | None] | None:
        """Retrieve a cache entry, clearing it if expired.

        Returns:
            The ``(value, expire_at)`` tuple or ``None`` if the key is
            absent or the entry has expired.
        """
        entry = self._store.get(key)
        if entry is None:
            return None
        _, expire_at = entry
        if self._is_expired(expire_at):
            del self._store[key]
            return None
        return entry

    async def get(self, key: KeyType) -> ValueType | None:
        """Retrieve a value from the cache.

        Returns ``None`` if the key does not exist or the entry has expired.
        """
        entry = self._get_entry(key)
        if entry is None:
            return None
        return entry[0]

    async def set(
        self,
        key: KeyType,
        value: ValueType,
        ttl: float | None = None,
    ) -> None:
        """Store a value with optional TTL in seconds."""
        expire_at: float | None = time.monotonic() + ttl if ttl is not None else None
        self._store[key] = (value, expire_at)

    async def delete(self, key: KeyType) -> None:
        """Remove a key from the cache. No-op if key does not exist."""
        self._store.pop(key, None)

    async def exists(self, key: KeyType) -> bool:
        """Check whether a key exists and has not expired."""
        return self._get_entry(key) is not None

    async def clear(self) -> None:
        """Remove all entries from the cache."""
        self._store.clear()

    @staticmethod
    def _is_expired(expire_at: float | None) -> bool:
        """Check whether an entry with the given expiration time has expired."""
        if expire_at is None:
            return False
        return time.monotonic() >= expire_at
