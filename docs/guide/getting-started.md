# Getting Started

This guide walks through a small, complete example to help you get started with ForgingBlocks.

---
## Quick summary

This guide walks through a **small, complete example** to help you get started with ForgingBlocks. The focus is on **explicit outcomes** and **clear boundaries** — not frameworks or infrastructure.

What you'll learn:
- **Result** — Parse input with explicit success/failure handling (`Ok`/`Err`)
- **ValueObject** — Wrap primitives to make domain rules visible and reusable
- **get_value_or_else** — Handle failures without manual unpacking

No framework setup required — just pure Python with ForgingBlocks abstractions.

---

```python
from forging_blocks.foundation import Result, Ok, Err


def parse_int(value: str) -> Result[int, str]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"invalid integer: {value!r}")
```

### Using the function

```python
from forging_blocks.foundation import Ok, Err

result = parse_int("42")

match result:
    case Ok(number):
        print(f"Parsed number: {number}")
    case Err(error):
        print(f"Error: {error}")
```

---

## Modeling a value with ValueObject

When a value is more than a primitive, you can wrap it in a `ValueObject` to
make its rules visible and reusable.

```python
from forging_blocks.foundation.value_object import ValueObject


class Email(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email")
        self._value = value

    @property
    def value(self) -> str:
        return self._value
```

`ValueObject` gives you value-based equality, hashability, and immutability
automatically via `auto_hash` and `auto_freeze`, so that you
can focus on the rules of *your* value.

---

## Providing a fallback with `get_value_or_else`

`Result` exposes a small set of helpers for handling failures without
unpacking them manually.

```python
from forging_blocks.foundation import Result, Ok, Err


def parse_int(value: str) -> Result[int, str]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"invalid integer: {value!r}")


number = parse_int("foo").get_value_or_else(lambda error: 0)
```

`get_value_or_else` calls the provided function with the carried error and
returns its result. It is useful when you want to log, transform, or
recover from the error before falling back.

---

## What to read next

- The [Examples](examples.md) page collects small, focused snippets for many
  of the Foundation abstractions.
- The [Testing](testing.md) guide explains how these abstractions lead to
  testable designs.
- The [Reference](../reference/foundation.md) section describes each
  Foundation abstraction in detail.
