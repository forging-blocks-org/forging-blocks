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
The `Serializable` protocol enables dictionary round-tripping via `to_dict()` and `from_dict()`. Structural — any class with matching signatures satisfies it automatically.
