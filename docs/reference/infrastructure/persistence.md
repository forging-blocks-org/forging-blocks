# Persistence

## Repositories

Repositories bridge domain aggregates and persistence.

- **Base Repository** — Shared identity-keyed storage: `get`, `add`, `remove`, `contains`
- **In-Memory Write Repository** — Dictionary-backed append-only store for testing
- **In-Memory Read Repository** — Query-oriented read store for CQRS projections
- **Aggregate Repository** — Integrates with `UnitOfWorkPort` and `EventBusPort`; tracks new/dirty aggregates

## Unit of Work

Manages a transactional boundary around repository operations. Tracks new and dirty aggregates, flushes events on commit, provides `commit`/`rollback` semantics.

Multiple repository operations within a single use case are treated as one atomic unit.
