# Technical Adapters

Technical adapters implement the outbound ports defined by the Application layer when
such a port exists. Forging Blocks ships standard-library-backed implementations, so
applications can use them without third-party runtime dependencies.

Use these adapters directly in tests or development; in production, replace them
behind the same port interface when a different technology is required.

## Logging
A standard-library logging adapter implementing `LoggerPort`. Provides `debug`, `info`, `warning`, and `error` methods — all accept `*args: str` for ``%``-style formatting (delegates to `logging.Logger`).

## HTTP Client

An `http.client`-backed asynchronous HTTP adapter implementing `HttpClientPort`. It
supports request methods, URLs, headers, and UTF-8 string bodies/responses; it exposes
no timeout option.

## File System
An OS-level filesystem adapter implementing `FileSystemPort`. All operations are `async`. Supports `read`, `write`, `delete`, `exists`, and directory listing.

## Caching
A dictionary-backed key-value cache implementing `CachePort`. Supports `get`, `set`, `delete`, and `clear`.

## Serialization

`MessageCodec` is a standalone abstract codec base that defines `encode` / `decode`
for bidirectional message serialization. `DictMessageCodec` is the concrete
`dict[str, object]` implementation that ships with Forging Blocks.
