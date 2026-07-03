# Value Objects

A **Value Object** represents an immutable concept defined entirely by its values.

## Characteristics

- Immutable
- Equality by value
- Hashable
- No independent identity

Value Objects model concepts such as identifiers, measurements, or descriptive values where identity is not meaningful.

## When to use

Choose a Value Object when two instances with equal values are interchangeable. If you need to track a specific instance over time — distinguishing "this order" from "that order" even when they look identical — use an [Entity](entities.md) instead.

A Value Object should enforce its own validity in its constructor.

A `Money(amount=-5)` should never exist. This keeps constraints local and testable.

!!! note "Avoiding Primitive Obsession"
    Value Objects prevent domain rules from being scattered across the codebase. Wrapping meaning in explicit types makes constraints visible, reusable, and testable.

!!! note "Where the implementation lives"
    The `ValueObject` base class lives in the [Foundation](../foundation.md) block because value-based equality and immutability are reusable outside the Domain block.
