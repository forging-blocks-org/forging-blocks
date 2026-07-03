# Messaging and Events

## Message Bus

- **In-Memory Message Bus** — Synchronous dispatcher routing commands, queries, and events to registered handlers
- **Command Sender** — Thin adapter implementing `CommandSenderPort`; fire-and-forget
- **Event Publisher** — Thin adapter implementing `EventPublisherPort`; publishes domain events
- **Query Fetcher** — Thin adapter implementing `QueryFetcherPort`; dispatches queries, returns typed results

## Event Store

Append-only event log storing domain events chronologically. Supports `append` with optimistic concurrency (expected version check) and `get_events` for aggregate rebuilding.

## Event Bus

## When to use

Use the in-memory message bus for tests and development. Register handlers at startup, dispatch messages at runtime. Use `CommandSender`, `EventPublisher`, and `QueryFetcher` as thin wrappers that satisfy the corresponding port protocols.

Publish/subscribe mechanism delivering domain events to registered handlers. Synchronous delivery to all subscribers.
