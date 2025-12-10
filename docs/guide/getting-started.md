# 🚀 Getting Started

This guide walks you through installing **ForgingBlocks** and using a few of its core building blocks in a small, self-contained example.

ForgingBlocks is a **toolkit**, not a framework. You can adopt as little or as much as you like.

---

## 1. Install the Toolkit

You can install it with **Poetry**, **pip**, or **uv**:

```bash
poetry add forging-blocks
# or
pip install forging-blocks
# or
uv add forging-blocks
```

ForgingBlocks supports **Python 3.12+** and depends only on the standard library.

---

## 2. Your First Result

The `Result` type helps you make success and failure explicit.

```python
from forging_blocks.foundation import Result, Ok, Err

def parse_int(value: str) -> Result[int, str]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"Invalid integer: {value!r}")
```

You can then handle outcomes clearly:

```python
result = parse_int("42")

match result:
    case Ok(value):
        print(f"Parsed value: {value}")
    case Err(error):
        print(f"Could not parse: {error}")
```

---

## 3. Defining a Port

A **Port** defines a boundary — for example, between an application rule and an external system.

```python
from typing import Protocol
from forging_blocks.foundation import Result, Ok, Err

class UserNotifier(Protocol):
    def send_welcome(self, email: str) -> Result[None, str]:
        ...
```

A simple implementation:

```python
class ConsoleNotifier:
    def send_welcome(self, email: str) -> Result[None, str]:
        print(f"[welcome] Sent to: {email}")
        return Ok(None)
```

Nothing here depends on frameworks or infrastructure.

---

## 4. A Small Use Case

You can structure simple use cases with clear inputs, outputs, and boundaries:

```python
from dataclasses import dataclass

@dataclass
class RegisterUserInput:
    email: str

class RegisterUser:
    def __init__(self, notifier: UserNotifier) -> None:
        self._notifier = notifier

    def execute(self, data: RegisterUserInput) -> Result[None, str]:
        if "@" not in data.email:
            return Err("invalid email")

        # In a real system, you might persist the user here.
        return self._notifier.send_welcome(data.email)
```

Usage:

```python
use_case = RegisterUser(ConsoleNotifier())
result = use_case.execute(RegisterUserInput(email="user@example.com"))

if isinstance(result, Ok):
    print("User registered.")
else:
    print(f"Error: {result.err}")
```

This small example already demonstrates:

- explicit success/failure
- clear boundaries
- decoupled behavior

---

## 5. Next Steps

From here, you can:

- Explore the [Organizational Blocks](recommended_blocks_structure.md).
- Learn more about the [core principles](principles.md).
- Look at [testing examples](example_tests.md).

ForgingBlocks stays out of your way — you decide how much structure you want to introduce.
