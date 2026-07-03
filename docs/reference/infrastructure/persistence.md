# Persistence

## Repositories

Repositories bridge domain aggregates and persistence.

- **Base Repository** — Shared identity-keyed storage: `get`, `add`, `remove`, `contains`
- **In-Memory Write Repository** — Dictionary-backed append-only store for testing
- **In-Memory Read Repository** — Query-oriented read store for CQRS projections
- **Aggregate Repository** — Integrates with `UnitOfWorkPort` and `EventBusPort`; tracks new/dirty aggregates

## Unit of Work

Manages a transactional boundary around repository operations. Tracks new and dirty aggregates, flushes events on commit, provides `commit`/`rollback` semantics.

## When to use

Use the in-memory implementations for tests and development — no external dependencies. `BaseRepository` gives you `get`/`add`/`remove` for free; extend it for domain-specific queries. Use `AggregateRepository` when you need `UnitOfWorkPort` integration and event publishing.

Multiple repository operations within a single use case are treated as one atomic unit.
