# Examples
## Small, architecture-neutral usage snippets

This page collects small, focused examples that show how to use ForgingBlocks concepts in isolation.

Each example is **self-contained** and does not assume any particular project structure.

---

## 1. Validation with Result

```python
from dataclasses import dataclass
from forging_blocks.foundation import Result, Ok, Err


@dataclass(frozen=True)
class RegisterUserInput:
    email: str
    name: str


def validate_registration(data: RegisterUserInput) -> Result[RegisterUserInput, str]:
    if "@" not in data.email:
        return Err("invalid email")
    if not data.name.strip():
        return Err("name required")
    return Ok(data)
```

Usage:

```python
incoming = RegisterUserInput(email="user@example.com", name="Alice")
result = validate_registration(incoming)

match result:
    case Ok(valid):
        print(f"Ready to register: {valid}")
    case Err(error):
        print(f"Validation error: {error}")
```

---

## 2. Simple domain-like type

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    completed: bool = False

    def complete(self) -> "Task":
        return Task(id=self.id, title=self.title, completed=True)
```

This type does not rely on any infrastructure. It can be tested directly, extended easily, and used in a wide range of designs.

---

## 3. Using a port and adapter

```python
from typing import Protocol

from forging_blocks.foundation import Err, Ok, Port, Result


class EmailSender(Port):
    def send(self, to: str, subject: str, body: str) -> Result[None, str]:
        ...
```

A console-based implementation:

```python
class ConsoleEmailSender:
    def send(self, to: str, subject: str, body: str) -> Result[None, str]:
        print(f"To: {to}\nSubject: {subject}\n\n{body}")
        return Ok(None)
```

A small function using the port:

```python
def send_reset_email(sender: EmailSender, email: str) -> Result[None, str]:
    if "@" not in email:
        return Err("invalid email")
    body = "Click here to reset your password."
    return sender.send(to=email, subject="Reset your password", body=body)
```

The design is:

- clear to read,
- easy to test with a fake `EmailSender`,
- independent of any particular mail provider or framework.

---

## 4. What to explore next

Once you are comfortable with these examples, you can:

- read [Principles](principles.md) to understand why the toolkit is structured this way,
- map examples into blocks using [Recommended Blocks Structure](recommended_blocks_structure.md),
- and explore architectural mappings in the **Architectural Styles** section if you want to see how these ideas can appear inside well-known styles.
