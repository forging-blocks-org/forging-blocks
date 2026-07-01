"""Cache port for abstract caching operations.

Defines the ``CachePort`` protocol that application code depends on,
decoupling caching from any specific implementation (in-memory, Redis, etc.).

Responsibilities:
    - Store and retrieve cached values by key.
    - Check cache existence and clear entries.
    - Support optional TTL (time-to-live) for entries.

Non-Responsibilities:
    - Eviction policies (LRU, LFU) — handled by infrastructure.
    - Distributed locking or consistency guarantees.
    - Serialization of cache values.
"""

from typing import Protocol

from forging_blocks.foundation.ports import OutboundPort


class CachePort[KeyType, ValueType](
    OutboundPort[KeyType, ValueType],
    Protocol,
):
    """Protocol for caching operations.

    Any object with the async ``get``, ``set``, ``delete``, ``exists``,
    and ``clear`` methods satisfies this protocol.

    Type Parameters:
        KeyType: The type of cache keys (typically str).
        ValueType: The type of cached values.
    """

    async def get(self, key: KeyType) -> ValueType | None:
        """Retrieve a value from the cache.

        Args:
            key: The cache key.

        Returns:
            The cached value, or ``None`` if not found or expired.
        """
        ...

    async def set(
        self,
        key: KeyType,
        value: ValueType,
        ttl: float | None = None,
    ) -> None:
        """Store a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
            ttl: Optional time-to-live in seconds. ``None`` means no expiration.
        """
        ...

    async def delete(self, key: KeyType) -> None:
        """Remove a value from the cache.

        Args:
            key: The cache key. No-op if the key does not exist.
        """
        ...

    async def exists(self, key: KeyType) -> bool:
        """Check whether a key exists in the cache and has not expired.

        Args:
            key: The cache key.

        Returns:
            ``True`` if the key exists and is not expired, ``False`` otherwise.
        """
        ...

    async def clear(self) -> None:
        """Remove all entries from the cache."""
        ...
