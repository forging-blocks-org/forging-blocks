# Auto-Hash (`auto_hash`)

The `@auto_hash` decorator generates `__hash__` for class instances based on their fields. Mutable values (lists, dicts) are automatically converted to hashable equivalents (tuples, frozensets) during hashing. It does **not** generate ``__eq__`` — ``__eq__`` in the examples below is provided by ``@dataclass``. Combine with [`@auto_eq`](auto-eq.md) for explicit equality.

## Usage

- `@auto_hash` — Hash on all fields
- `@auto_hash()` — Equivalent, explicit parens form
- `@auto_hash(fields=["x", "y"])` — Hash on specific fields only

After decoration, equal objects produce equal hashes — suitable for use in sets and dict keys. The decorator raises `NonHashableValueError` at hash time if a field value cannot be converted to a hashable type.

## When to use

`@auto_hash` is ideal for value types that need hashing. If you also need equality, use [`@auto_eq`](auto-eq.md) or rely on ``@dataclass`` (which generates ``__eq__`` by default). If you only need immutability without structural comparison, use [`@auto_freeze`](auto-freeze.md).

## Generated members

The decorated class receives:

- `__hash__` — hash computed from the resolved field values, with mutable-to-hashable conversion
- `__auto_hash_fields__` — tuple of field names used in hashing, available for introspection

## Examples

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_hash

@auto_hash
@dataclass
class Point:
    x: int
    y: int

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

assert hash(p1) == hash(p2)
assert hash(p1) != hash(p3)
assert p1 == p2
```

With mutable field conversion:

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_hash

@auto_hash
@dataclass
class Tagged:
    name: str
    tags: list[str]

a = Tagged("item", ["a", "b"])
b = Tagged("item", ["a", "b"])
assert hash(a) == hash(b)  # list converted to tuple automatically
```

Selective fields:

```python
from dataclasses import dataclass
from forging_blocks.foundation import auto_hash

@auto_hash(fields=["id"])
@dataclass
class Entity:
    id: str
    name: str

e1 = Entity("1", "Alice")
e2 = Entity("1", "Bob")
assert hash(e1) == hash(e2)  # only id matters
```
