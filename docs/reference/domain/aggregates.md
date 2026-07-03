# Aggregate Roots

An **Aggregate Root** defines a consistency boundary. It controls access to related state and ensures invariants are always satisfied.

## Characteristics

- Defines a transactional consistency boundary
- Controls mutation of internal state
- Protects invariants across related entities
- Tracks version via `AggregateVersion` for optimistic concurrency
- Collects domain events for publishing on commit

The `AggregateRoot` base class provides identity-based equality (via [Entity](entities.md)), domain event collection, and an abstract `apply(event)` method for event sourcing.

## When to use

Inherit from `AggregateRoot` when you need a consistency boundary with version tracking (`AggregateVersion`) and automatic domain event collection. The base class provides identity equality (via `Entity`) and an `apply(event)` hook for event sourcing.

!!! note "Influence: Vaughn Vernon"
    The emphasis on consistency boundaries and controlled mutation is inspired by Vaughn Vernon. ForgingBlocks provides aggregates when boundaries matter, without requiring their use everywhere.
