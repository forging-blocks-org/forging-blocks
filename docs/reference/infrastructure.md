# Infrastructure
## Technical adapters

The **Infrastructure** block provides concrete implementations of outbound ports. It contains all technical details — I/O, serialization, networking, persistence.

Depends on **Application** (for port definitions), **Domain** (for aggregate types), and **Foundation**. Does not depend on Presentation.

---
## How it works

Infrastructure adapters implement the contracts defined by Application outbound ports.

- An `InMemoryWriteRepository` satisfies `RepositoryPort` with a dictionary.
- An `InMemoryEventBus` satisfies `EventBusPort` with in-process publish/subscribe.
- Each adapter encapsulates a technology choice behind a port interface.

The Application block only sees the port. You swap the adapter without touching application or domain code. A test injects an in-memory store. Production injects a PostgreSQL adapter. Same port, different implementation.

---
## How to use

Start with in-memory implementations for fast feedback during development. They require no external services and run in tests. Graduate to real adapters when you need persistence, messaging, or external integration.

Adapters are composable:

- A `UnitOfWork` wraps multiple repositories.
- A `MessageBus` dispatches to multiple handlers.

Wire them together at startup — a composition root — and pass the resulting graph into the Application layer.

---
## Core abstractions

- **[Persistence](infrastructure/persistence.md)** — Repositories, Unit of Work
- **[Messaging & Events](infrastructure/messaging.md)** — Message Buses, Event Stores, Event Buses
- **[Technical Adapters](infrastructure/adapters.md)** — Logging, HTTP, File System, Caching, Serialization

---
## What it does not do

- Define business rules or domain logic
- Orchestrate workflows
- Make architectural decisions about port shape
- Depend on Presentation

---
## Glossary

!!! note "Repository"
    Persists and retrieves domain aggregates. Implements `RepositoryPort`.

!!! note "Unit of Work"
    Coordinates multiple repository operations within a transactional boundary.

!!! note "Message Bus"
    Dispatches commands, queries, and events to registered handlers.

!!! note "Event Store"
    Append-only event storage with optimistic concurrency for event sourcing.
