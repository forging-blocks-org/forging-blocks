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

Inherit from `Entity` when you need identity-based equality (`__eq__` / `__hash__` by ID) and the built-in lifecycle: draft → identified. The base class enforces that an ID, once set, cannot be changed or removed.

!!! note "Influence: Eric Evans"
    The focus on identity as a defining characteristic is inspired by *Domain-Driven Design* by Eric Evans. ForgingBlocks adopts this idea without requiring a full DDD tactical model.
