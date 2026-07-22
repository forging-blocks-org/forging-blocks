# Persistence

## Repositories

Repositories bridge domain aggregates and persistence.

- **InMemory Repository** — Shared identity-keyed storage: `get_by_id`, `save`, `delete_by_id`
- **In-Memory Write Repository** — Dictionary-backed append-only store for testing
- **In-Memory Read Repository** — Query-oriented read store for CQRS projections
- **Aggregate Repository** — Integrates with `UnitOfWorkPort` and `EventBusPort`; tracks new/dirty aggregates

## Unit of Work

Manages a transactional boundary around repository operations. Tracks new and dirty aggregates, flushes events on commit, provides `commit`/`rollback` semantics.

## When to use

Use the in-memory implementations for tests and development — no external dependencies. `InMemoryRepository` gives you `get_by_id`/`save`/`delete_by_id`; extend it for domain-specific queries. Use `AggregateRepository` when you need `UnitOfWorkPort` integration and event publishing.

Multiple repository operations within a single use case are treated as one atomic unit.
