# Messaging and Events

The messaging layer routes commands, queries, and events between application and
domain components. Its contracts remain separate because they provide different
delivery semantics:

- **Message Bus** — Asynchronous dispatch for commands, queries, or events.
  `MessageBusCommandSender`, `MessageBusEventPublisher`, and `MessageBusQueryFetcher`
  are role-specific wrappers around `MessageBusPort`.
- **Event Store** — An append-only log that records domain events chronologically.
  It enables rebuilding aggregate state from history.
- **Event Bus** — Publish/subscribe delivery through `EventBusPort`.
  `EventPublisherPort` is a separate publication contract; its shipped adapter
  delegates to a `MessageBusPort`.

## Message Bus

- **In-Memory Message Bus** — In-process asynchronous dispatcher routing messages to registered handlers.
- **Command Sender** — Thin adapter implementing `CommandSenderPort`; callers await dispatch completion without a result payload.
- **Event Publisher** — Thin adapter implementing `EventPublisherPort`; delegates event publication to a `MessageBusPort`.
- **Query Fetcher** — Thin adapter implementing `QueryFetcherPort`; dispatches queries and returns typed results.

## Event Store

Append-only event log storing domain events chronologically. Supports
`append_events` with optimistic concurrency and `get_events` for aggregate rebuilding.

## Event Bus

Publish/subscribe mechanism delivering domain events to registered handlers through
`EventBusPort`. The in-memory implementation exposes an asynchronous API and awaits
handlers sequentially.

## When to use

Use the in-memory message and event buses for tests and development. Register handlers
at startup, dispatch messages at runtime, and select `EventPublisherPort` when a
Unit of Work should publish aggregate events through a separate publisher boundary.
