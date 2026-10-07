# Infrastructure
## Technical adapters

The **Infrastructure** block provides concrete implementations of outbound ports. It contains all technical details — I/O, serialization, networking, persistence.

Depends on **Application** (for port definitions), **Domain** (for aggregate types), and **Foundation**. Does not depend on Presentation.

---
## How it works

Infrastructure adapters implement the contracts defined by Application outbound ports.

- An `InMemoryWriteRepository` satisfies `WriteOnlyRepositoryPort` with a dictionary.
- An `InMemoryRepository` combines read and write contracts for full CRUD access.
- An `InMemoryEventBus` satisfies `EventBusPort` with in-process publish/subscribe.
- Each adapter encapsulates a technology choice behind a port interface.

---
## How to use

Start with in-memory implementations for fast feedback during development. They require no external services and run in tests. Graduate to real adapters when you need persistence, messaging, or external integration.

Adapters are composable in a consuming application's composition root:

- A Unit of Work can coordinate registered aggregate event publication.
- A Message Bus dispatches messages to registered handlers.

Wire them together at startup and pass the resulting graph into the Application layer.

---
## Core abstractions

- **[Persistence](infrastructure/persistence.md)** — Repositories, Unit of Work.
- **[Messaging & Events](infrastructure/messaging.md)** — Message Buses, Event Stores, Event Buses.
- **[Technical Adapters](infrastructure/adapters.md)** — Logging, HTTP, File System, Caching, Serialization.
- **[Errors](infrastructure/errors.md)** — Repository error types.

---
## What it does not do

- Define business rules or domain logic.
- Orchestrate workflows.
- Make architectural decisions about port shape.
- Depend on Presentation.

---
## Glossary

!!! note "Repository"
    Persists and retrieves domain aggregates. Implements `RepositoryPort`.

!!! note "Unit of Work"
    Coordinates registered aggregate event publication and queue draining; database
    transaction rollback is adapter-specific.

!!! note "Message Bus"
    Dispatches commands, queries, and events to registered handlers.

!!! note "Event Store"
    Append-only event storage with optimistic concurrency for event sourcing.
