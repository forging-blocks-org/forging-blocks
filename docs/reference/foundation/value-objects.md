# Value Objects

A **ValueObject** is an immutable object with value-based equality and hashing.

## Characteristics

- Immutable after construction
- Equality determined by all field values, not identity
- Hashable — suitable for use as dict keys or set members
- Optionally serializable via `__dict__` without extra ceremony

## When to use

Use `ValueObject` when the meaning of a concept is fully captured by its values — measurements, identifiers, monetary amounts, ranges. When two instances with the same values should be considered equal.

!!! note "ValueObject vs auto-freeze"
    `ValueObject` gives you immutability, value equality, and hashing. If you only need immutability and already have your own base class, [auto-freeze](auto-freeze.md) is a lighter alternative. Both are optional.

!!! note "Related"
    The Domain block re-exports `ValueObject`. See [Domain Value Objects](../domain/value-objects.md) for domain-specific guidance.
