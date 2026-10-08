# Persistence

Persistence bridges domain aggregates and storage. Forging Blocks ships in-memory
implementations so applications can run without external databases — useful for tests,
development, and single-process deployments. The in-memory store uses identity-keyed
dictionaries; swap in a real database adapter behind the same `RepositoryPort` for production.

## Repositories

- **InMemory Repository** — Shared identity-keyed storage: `get_by_id`, `save`, `delete_by_id`
- **In-Memory Write Repository** — Dictionary-backed identity-keyed store for testing
- **In-Memory Read Repository** — Query-oriented read store for CQRS projections
- **Aggregate Repository** — Appends state-changing aggregate events to an event store and
  caches aggregate snapshots. It does not own Unit of Work or event-publisher state.

## Unit of Work

`InMemoryUnitOfWork` tracks aggregates explicitly registered with `register_modified()`.
On commit it publishes both state-changing and publication-only events through its
`EventPublisherPort`, then drains their queues. On publication failure it discards
queued events and clears tracking before raising `UnitOfWorkError`; already published
events cannot be undone.

Rollback discards queued aggregate events and tracking. It does not undo repository
writes, so database-level atomicity remains the responsibility of a different adapter.

## When to use

Use the in-memory repositories for tests and development — no external services are
required. Use `AggregateRepository` for event-store append plus snapshot caching.
Use `InMemoryUnitOfWork` when an application needs one event-publication boundary for
registered aggregates.
