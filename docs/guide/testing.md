# Testing
## How ForgingBlocks supports testable designs

ForgingBlocks encourages designs where behavior and outcomes are explicit.
This makes your code easier to test without relying on internal details.

This guide focuses on **what to test and why**, not on any specific testing framework.
You can use `pytest`, `unittest`, or any other tool you prefer.

---

## 1. Testing pure functions

Pure functions are the easiest place to start.
When a function returns a `Result`, success and failure are part of the contract.

```python
from forging_blocks.foundation import Result, Ok, Err


def is_even(value: int) -> Result[bool, str]:
    if value < 0:
        return Err("negative value")
    return Ok(value % 2 == 0)
```

### Example tests

Tests should focus on **intent first**, not on how the `Result` is represented.

```python
from your_module import is_even


def test_is_even_when_value_is_even_then_succeeds() -> None:
    result = is_even(4)

    assert result.is_ok


def test_is_even_when_value_is_odd_then_succeeds() -> None:
    result = is_even(3)

    assert result.is_ok


def test_is_even_when_value_is_negative_then_fails() -> None:
    result = is_even(-1)

    assert result.is_err
```

Only inspect returned values when they matter to the test’s intent:

```python
from forging_blocks.foundation import Ok


def test_is_even_returns_false_for_odd_numbers() -> None:
    result = is_even(3)

    assert result.is_ok

    match result:
        case Ok(value):
            assert value is False
```

---

## 2. Testing code that depends on a Port (using fakes)

When code depends on a **Port**, you can replace that dependency in tests.
This lets you verify behavior without involving infrastructure.

```python
from forging_blocks.foundation import Result, Port


class IdGenerator(Port):
    def generate(self) -> Result[str, str]:
        ...
```

Business logic:

```python
def create_user_id(generator: IdGenerator) -> Result[str, str]:
    return generator.generate()
```

A simple fake implementation:

```python
from forging_blocks.foundation import Result, Ok, Err


class FakeIdGenerator:
    def __init__(self, ids: list[str]) -> None:
        self._ids = ids

    def generate(self) -> Result[str, str]:
        if not self._ids:
            return Err("no more ids")
        return Ok(self._ids.pop(0))
```

### Example tests

```python
from your_module import create_user_id, FakeIdGenerator


def test_create_user_id_when_id_is_available_then_succeeds() -> None:
    generator = FakeIdGenerator(["id-1"])

    result = create_user_id(generator)

    assert result.is_ok


def test_create_user_id_when_no_ids_left_then_fails() -> None:
    generator = FakeIdGenerator([])

    result = create_user_id(generator)

    assert result.is_err
```

---

## 3. When to use pattern matching in tests

Pattern matching is useful when:
- the returned value is meaningful to the behavior
- you need to inspect error information
- multiple outcomes must be distinguished

It should **support the test**, not dominate it.

---

## 4. Fakes vs mocks

Both approaches work well with Ports.

- **Fakes** emphasize state and behavior.
- **Mocks** emphasize interactions.

Choose the approach that makes the test’s intent most obvious.

ForgingBlocks does not enforce a testing style — it encourages clarity.
