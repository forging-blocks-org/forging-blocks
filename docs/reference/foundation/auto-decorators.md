# Auto Decorators

`@auto_freeze`, `@auto_eq`, and `@auto_hash` are lightweight decorators that add immutability, structural equality, and hashing to plain Python classes — no inheritance from a base class required.

---

## `@auto_freeze`

Enforces immutability after `__init__` completes. After construction, any attempt to assign a frozen attribute raises `CantModifyImmutableAttributeError`.

### Usage

- `@auto_freeze` — Freezes the entire instance
- `@auto_freeze()` — Equivalent, explicit parens form
- `@auto_freeze(attrs=["_id"])` — Selectively freeze specific attributes only

The decorator handles `__init__` nesting (inheritance chains) and skips abstract classes.

```python
from forging_blocks.foundation import auto_freeze

@auto_freeze
class Money:
    __slots__ = ("_amount", "_currency")

    def __init__(self, amount: int, currency: str) -> None:
        self._amount = amount
        self._currency = currency.upper()

m = Money(100, "usd")
m._amount = 200  # raises CantModifyImmutableAttributeError
```

Selective freezing:

```python
from forging_blocks.foundation import auto_freeze

@auto_freeze(attrs=["_id"])
class User:
    __slots__ = ("_id", "_name")

    def __init__(self, user_id: str, name: str) -> None:
        self._id = user_id
        self._name = name

u = User("usr-1", "Alice")
u._name = "Bob"      # ok — not frozen
u._id = "usr-2"      # raises CantModifyImmutableAttributeError
```

`auto_freeze` injects a `__setattr__` override and a freeze flag. It detects existing custom `__setattr__` implementations and avoids double-wrapping.

---

## `@auto_eq`

Generates `__eq__` for class instances based on their fields. Does **not** generate `__hash__` — combine with `@auto_hash` when hashability is required.

### Usage

- `@auto_eq` — Equality on all fields
- `@auto_eq()` — Equivalent, explicit parens form
- `@auto_eq(fields=["x", "y"])` — Equality on specific fields only

Comparison is type-strict: `type(self) is type(other)` must be true, so subclasses are not equal to their parent.

### Generated members

- `__eq__` — structural equality on the resolved fields
- `__auto_eq_fields__` — tuple of field names used in equality, available for introspection

### Examples

```python
from forging_blocks.foundation import auto_eq

@auto_eq
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

assert p1 == p2
assert p1 != p3
```

With explicit field selection:

```python
from forging_blocks.foundation import auto_eq

@auto_eq(fields=["x"])
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

# y is ignored — only x matters
assert Point(1, 2) == Point(1, 999)
assert Point(1, 2) != Point(2, 999)
```

---

## `@auto_hash`

Generates `__hash__` for class instances based on their fields. Mutable values (lists, dicts) are automatically converted to hashable equivalents (tuples, frozensets). Does **not** generate `__eq__` — combine with `@auto_eq` for explicit equality.

### Usage

- `@auto_hash` — Hash on all fields
- `@auto_hash()` — Equivalent, explicit parens form
- `@auto_hash(fields=["x", "y"])` — Hash on specific fields only

Equal objects produce equal hashes — suitable for sets and dict keys. Raises `NonHashableValueError` at hash time if a field value cannot be converted to a hashable type.

### Generated members

- `__hash__` — hash computed from the resolved field values, with mutable-to-hashable conversion
- `__auto_hash_fields__` — tuple of field names used in hashing, available for introspection

### Examples

```python
from forging_blocks.foundation import auto_hash

@auto_hash
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

assert hash(p1) == hash(p2)
assert hash(p1) != hash(p3)
```

With mutable field conversion:

```python
from forging_blocks.foundation import auto_hash

@auto_hash
class Tagged:
    __slots__ = ("name", "tags")

    def __init__(self, name: str, tags: list[str]) -> None:
        self.name = name
        self.tags = tags

a = Tagged("item", ["a", "b"])
b = Tagged("item", ["a", "b"])
assert hash(a) == hash(b)  # list converted to tuple automatically
```

Selective fields:

```python
from forging_blocks.foundation import auto_hash

@auto_hash(fields=["id"])
class Entity:
    __slots__ = ("id", "name")

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

e1 = Entity("1", "Alice")
e2 = Entity("1", "Bob")
assert hash(e1) == hash(e2)  # only id matters
```

---

## Combining Decorators

The three auto decorators compose with each other and with `@dataclass`. Stacking order matters:

| Position | Decorator | Role |
|----------|-----------|------|
| Top (outermost) | `@auto_hash` | Generates `__hash__` |
| | `@auto_eq` | Generates `__eq__` |
| | `@auto_freeze` | Enforces immutability |
| Bottom (innermost) | `@dataclass` | Generates `__init__`, `__repr__`, etc. |

!!! note
    `@auto_freeze` must be applied before `@dataclass` but after `@auto_eq` / `@auto_hash` so that equality and hashing test the frozen fields.

---

### `auto_eq` + `auto_hash` (POPO)

Combining `@auto_hash` and `@auto_eq` on a plain Python class gives both structural equality and hashability:

```python
from forging_blocks.foundation import auto_hash, auto_eq

@auto_hash
@auto_eq
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)

assert p1 == p2                         # structural equality
assert hash(p1) == hash(p2)             # consistent hashing
assert p1 in {p2}                       # usable in sets
```

---

### `auto_freeze` with Other Decorators (POPO)

Add `@auto_freeze` below `@auto_eq` / `@auto_hash` to make the class immutable after construction:

```python
from forging_blocks.foundation import auto_hash, auto_eq, auto_freeze

@auto_hash
@auto_eq
@auto_freeze
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

p = Point(1.0, 2.0)
p.x = 5.0  # raises CantModifyImmutableAttributeError
```

---

### With `@dataclass`

When combining with `@dataclass`, place the auto decorators above it (outermost first). `@dataclass` generates `__eq__` by default, so `@auto_eq` is optional here.

#### `@auto_hash` only

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_hash

@auto_hash
@dataclass
class User:
    id: str
    name: str

u1 = User("1", "Alice")
u2 = User("1", "Alice")
d = {u1: "data"}
assert d[u2] == "data"
```

#### Full stack with `@dataclass`

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_hash, auto_eq

@auto_hash
@auto_eq
@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
assert p1 == p2
assert hash(p1) == hash(p2)
```

#### Full stack with `@auto_freeze`

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_hash, auto_eq, auto_freeze

@auto_hash
@auto_eq
@auto_freeze
@dataclass
class Money:
    amount: int
    currency: str

m = Money(100, "usd")
m.amount = 200  # raises CantModifyImmutableAttributeError
```

---

## Decorator Stacking Order

The decorator order determines how each layer sees the class:

1. `@auto_hash` (top) — receives the class after `@auto_eq` and `@auto_freeze` / `@dataclass` have applied. It generates `__hash__` based on the fields visible at that point.
2. `@auto_eq` — receives the class after `@auto_freeze` / `@dataclass` have applied. It generates `__eq__`.
3. `@auto_freeze` — receives the class after `@dataclass` (if present). It wraps `__setattr__` to prevent mutations.
4. `@dataclass` (bottom) — generates `__init__`, `__repr__`, and optionally `__eq__`.

!!! note "Why `@auto_freeze` goes below `@auto_eq` / `@auto_hash`"
    Placing `@auto_freeze` below `@auto_eq` / `@auto_hash` ensures the equality and hash methods are generated before `@auto_freeze` potentially alters attribute access patterns. The freeze applies after all structural methods are in place.
