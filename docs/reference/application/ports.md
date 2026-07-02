# Inbound and Outbound Ports

Ports define the boundaries of the Application block — how it can be interacted with and what capabilities it depends on.

## Inbound Ports

Inbound ports describe *what can be requested* from the application without exposing internal implementation details. They include `UseCase` and `MessageHandler`.

## Outbound Ports

Outbound ports describe *what the application needs* from the outside world:

- **Repository Port** — Persistence abstraction (read-only, write-only, or read-write)
- **Specification Repository Port** — Read repository with specification-based queries
- **Unit of Work** — Transactional boundary across multiple operations
- **Message Bus** — Dispatches commands, events, and queries
- **Command Sender** — Fire-and-forget asynchronous commands
- **Event Publisher** — Publishes domain events to consumers
- **Event Store** — Append-only storage for event-sourced aggregates
- **Query Fetcher** — Asynchronous data retrieval
- **Cache Port** — Temporary key-value storage
- **Logger Port** — Abstracted logging
- **File System Port** — File read/write/delete operations
- **External Service Port** — HTTP and remote API calls
- **Notifier Port** — Asynchronous notification delivery

!!! note "Ports and Adapters"
    Outbound ports define *what* the application needs, never *how* it's implemented. Infrastructure provides the *how*.
