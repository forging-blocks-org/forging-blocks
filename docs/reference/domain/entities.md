# Entities

An **Entity** represents a concept whose **identity** matters over time.

## Characteristics

- Identity-based equality
- Explicit lifecycle
- Mutable state governed by rules
- Identity is assigned once and protected against modification or deletion

Entities are appropriate when it is important to distinguish *which* instance is being referred to, even if its attributes change.

## Lifecycle

An Entity transitions through three states: draft (no ID), identified (ID assigned), and optionally deleted. The base class enforces that an ID, once set, cannot be changed or removed — violations raise [Domain Errors](errors.md).

## When to use

Choose an Entity when two instances with identical attribute values must be distinguishable. If all values being equal means they are interchangeable, use a [Value Object](value-objects.md) instead.

!!! note "Influence: Eric Evans"
    The focus on identity as a defining characteristic is inspired by *Domain-Driven Design* by Eric Evans. ForgingBlocks adopts this idea without requiring a full DDD tactical model.
