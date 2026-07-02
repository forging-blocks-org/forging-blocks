# Value Objects

A **Value Object** represents an immutable concept defined entirely by its values.

## Characteristics

- Immutable
- Equality by value
- Hashable
- No independent identity

Value Objects model concepts such as identifiers, measurements, or descriptive values where identity is not meaningful.

!!! note "Avoiding Primitive Obsession"
    Value Objects prevent domain rules from being scattered across the codebase. Wrapping meaning in explicit types makes constraints visible, reusable, and testable.

!!! note "Where the implementation lives"
    The `ValueObject` base class lives in the [Foundation](../foundation.md) block because value-based equality and immutability are reusable outside the Domain block.
