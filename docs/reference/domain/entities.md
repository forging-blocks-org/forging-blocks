# Entities

An **Entity** represents a concept whose **identity** matters over time.

## Characteristics

- Identity-based equality
- Explicit lifecycle
- Mutable state governed by rules
- Identity is assigned once and protected against modification or deletion

Entities are appropriate when it is important to distinguish *which* instance is being referred to, even if its attributes change.

## Lifecycle

An Entity transitions through two states: draft (no ID) and identified (ID assigned). The base class enforces that an ID, once set, cannot be changed or removed — violations raise [Domain Errors](errors.md).

## When to use

Inherit from `Entity` when you need identity-based equality and the built-in lifecycle: draft → identified. Identified entities compare by type-qualified identity and hash by type plus ID. Draft entities compare by object identity and cannot be hashed.

!!! note "Influence: Eric Evans"
    The focus on identity as a defining characteristic is inspired by *Domain-Driven Design* by Eric Evans. ForgingBlocks adopts this idea without requiring a full DDD tactical model.
