# Technical Adapters

## Logging
A standard-library logging adapter implementing `LoggerPort`. Provides `debug`, `info`, `warning`, and `error` methods.

## HTTP Client
A `urllib`-based HTTP client implementing `ExternalServicePort`. Supports GET, POST, headers, and timeout configuration.

## File System
An OS-level filesystem adapter implementing `FileSystemPort`. Supports `read`, `write`, `delete`, `exists`, and directory listing.

## Caching
A dictionary-backed key-value cache implementing `CachePort`. Supports `get`, `set`, `delete`, and `clear`.

## Serialization
## When to use

These adapters implement the corresponding outbound ports from Application. Use the in-memory versions for tests; swap to real implementations (database, HTTP, filesystem) in production. `Serializable` is structural — any class with `to_dict()`/`from_dict()` satisfies it automatically.
