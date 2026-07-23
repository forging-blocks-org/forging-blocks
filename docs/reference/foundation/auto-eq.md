# Auto-Equality (`auto_eq`)

The `@auto_eq` decorator generates `__eq__` for class instances based on their fields. It does **not** generate `__hash__` — combine with [`@auto_hash`](auto-hash.md) when hashability is required.

## Usage

- `@auto_eq` — Equality on all fields
- `@auto_eq()` — Equivalent, explicit parens form
- `@auto_eq(fields=["x", "y"])` — Equality on specific fields only

After decoration, instances compare equal when all selected fields match. Comparison is type-strict: `type(self) is type(other)` must be true, so subclasses of the same type are not equal to their parent.

## When to use

`@auto_eq` is useful when you need structural equality without hashability — for example, mutable objects where hashing would be incorrect. For immutable value types that need both equality and hashing, use [`@auto_hash`](auto-hash.md) or the [`ValueObject`](value-objects.md) base class instead.

## Generated members

The decorated class receives:

- `__eq__` — structural equality on the resolved fields
- `__auto_eq_fields__` — tuple of field names used in equality, available for introspection

## Examples

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_eq

@auto_eq
@dataclass
class Point:
    x: int
    y: int

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

assert p1 == p2
assert p1 != p3
```

With explicit field selection:

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_eq

@auto_eq(fields=["x"])
@dataclass
class Point:
    x: int
    y: int

# y is ignored — only x matters
assert Point(1, 2) == Point(1, 999)
assert Point(1, 2) != Point(2, 999)
```

Combined with `@auto_hash` for hashability:

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_eq, auto_hash

@auto_hash
@auto_eq
@dataclass
class Money:
    amount: int
    currency: str

m1 = Money(100, "USD")
m2 = Money(100, "USD")
s = {m1, m2}
assert len(s) == 1  # hashing works
assert m1 == m2      # equality works
```
