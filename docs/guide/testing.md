# ✅ Testing With ForgingBlocks

ForgingBlocks is designed to make testing straightforward by encouraging clear boundaries and explicit outcomes. This guide focuses on how to test code that *uses* ForgingBlocks, not on any particular testing framework.

You can use `pytest`, the standard library’s `unittest`, or any other testing tool.

---

## 1. Testing Functions That Return Result

A simple function using `Result`:

```python
from forging_blocks.foundation import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)
```

A couple of tests with `pytest`:

```python
from forging_blocks.foundation import Ok, Err
from your_module import divide

def test_divide_when_valid_input_then_returns_ok() -> None:
    result = divide(6, 3)
    assert isinstance(result, Ok)
    assert result.ok == 2

def test_divide_when_division_by_zero_then_returns_err() -> None:
    result = divide(1, 0)
    assert isinstance(result, Err)
    assert "division by zero" in result.err
```

The key idea: **you assert on explicit outcomes**, not on thrown exceptions or side effects.

---

## 2. Testing Code That Depends on a Port

Given a port:

```python
from typing import Protocol
from forging_blocks.foundation import Result

class Notifier(Protocol):
    def send(self, message: str) -> Result[None, str]:
        ...
```

And a use case:

```python
from dataclasses import dataclass
from forging_blocks.foundation import Result, Ok, Err

@dataclass
class SendWelcomeInput:
    email: str

class SendWelcome:
    def __init__(self, notifier: Notifier) -> None:
        self._notifier = notifier

    def execute(self, data: SendWelcomeInput) -> Result[None, str]:
        if "@" not in data.email:
            return Err("invalid email")

        return self._notifier.send(f"Welcome, {data.email}!")
```

You can test behavior by supplying a fake implementation:

```python
from forging_blocks.foundation import Ok, Err
from your_module import SendWelcome, SendWelcomeInput

class FakeNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.should_fail: bool = False

    def send(self, message: str):
        if self.should_fail:
            return Err("send failed")
        self.messages.append(message)
        return Ok(None)

def test_send_welcome_when_valid_email_then_sends_message() -> None:
    notifier = FakeNotifier()
    use_case = SendWelcome(notifier)

    result = use_case.execute(SendWelcomeInput(email="user@example.com"))

    assert isinstance(result, Ok)
    assert notifier.messages == ["Welcome, user@example.com!"]

def test_send_welcome_when_invalid_email_then_returns_err() -> None:
    notifier = FakeNotifier()
    use_case = SendWelcome(notifier)

    result = use_case.execute(SendWelcomeInput(email="invalid"))

    assert isinstance(result, Err)
    assert notifier.messages == []
```

You are not forced into any layering scheme — you simply test behavior at the granularity that makes sense.

---

## 3. Testing Adapters (Optional)

If you introduce an adapter that implements a port, for example:

```python
class ConsoleNotifier:
    def send(self, message: str):
        print(message)
        return Ok(None)
```

You can:

- test it directly, or
- stub or mock it when testing higher-level behavior.

ForgingBlocks does not require a specific testing strategy. It only encourages designs where testing is natural because behavior and boundaries are explicit.

---

## 4. Example Test Layout

One possible (not required) way to organize tests:

- `tests/foundation/` — tests for Result, mappers, and helpers you define.
- `tests/domain/` — tests for domain concepts and rules.
- `tests/application/` — tests for use cases and coordination.
- `tests/infrastructure/` — tests for adapters to external systems.

You can adapt this to your own project structure. The important part is that tests exercise meaningful behavior, not framework wiring.
