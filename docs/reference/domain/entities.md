# Entities

An **Entity** represents a concept whose **identity** matters over time.

## Characteristics

- Identity-based equality
- Explicit lifecycle
- Mutable state governed by rules

Entities are appropriate when it is important to distinguish *which* instance is being referred to, even if its attributes change.

!!! note "Influence: Eric Evans"
    The focus on identity as a defining characteristic is inspired by *Domain-Driven Design* by Eric Evans. ForgingBlocks adopts this idea without requiring a full DDD tactical model.
