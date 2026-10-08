# Aggregate Roots

An **Aggregate Root** defines a consistency boundary. It controls access to related state and ensures invariants are always satisfied.

## Characteristics

- Defines a transactional consistency boundary
- Controls mutation of internal state
- Protects invariants across related entities
- Tracks version via `AggregateVersion` for optimistic concurrency
- Collects state-changing and publication-only domain events for later dispatch

The `AggregateRoot` base class provides identity-based equality (via [Entity](entities.md)), version tracking, and event queues. The concrete runtime-final `apply(event)` method delegates state mutation to the abstract `_handle(event)` hook.

## When to use

Inherit from `AggregateRoot` when you need a consistency boundary with version tracking (`AggregateVersion`) and event collection. Use `apply()` for a new state transition, `replay()` to restore state from stored events without queuing them, and `record_event()` for a publication-only event that does not mutate aggregate state. The Unit of Work publishes and drains both queues; `AggregateRepository` persists only state-changing events.

!!! note "Influence: Vaughn Vernon"
    The emphasis on consistency boundaries and controlled mutation is inspired by Vaughn Vernon. ForgingBlocks provides aggregates when boundaries matter, without requiring their use everywhere.
