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

Introduce an Aggregate Root when a group of objects must stay consistent together — for example, an `Order` and its `LineItems`. External code should only reference the root; internal state is accessed through root methods that enforce invariants.

An Aggregate Root is also the right boundary for a transaction. Load it, modify it through the root, and save it as one atomic unit.

!!! note "Influence: Vaughn Vernon"
    The emphasis on consistency boundaries and controlled mutation is inspired by Vaughn Vernon. ForgingBlocks provides aggregates when boundaries matter, without requiring their use everywhere.
