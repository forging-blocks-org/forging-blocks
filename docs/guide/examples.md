# 📎 Examples

This page contains a small set of **neutral, self-contained examples** that use ForgingBlocks building blocks without assuming any particular architecture, framework, or library.

For examples that demonstrate how ForgingBlocks can be used *inside* classical architectural styles (such as Clean Architecture or Hexagonal Architecture), see the [Optional Architectural Approaches](../optional-architectures/index.md).

---

## 1. Handling Input Validation With Result

```python
from dataclasses import dataclass
from forging_blocks.foundation import Result, Ok, Err

@dataclass
class RegisterUserInput:
    email: str
    name: str

def validate_input(data: RegisterUserInput) -> Result[RegisterUserInput, str]:
    if "@" not in data.email:
        return Err("invalid email")

    if not data.name.strip():
        return Err("name required")

    return Ok(data)
```

Usage:

```python
incoming = RegisterUserInput(email="user@example.com", name="Alice")
result = validate_input(incoming)

match result:
    case Ok(valid):
        print(f"Ready to register: {valid}")
    case Err(error):
        print(f"Validation error: {error}")
```

---

## 2. Modeling a Simple Domain Concept

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

You can combine this with `Result` and ports to build richer behavior, if desired.

---

## 3. Using a Port With a Simple Adapter

```python
from typing import Protocol
from forging_blocks.foundation import Result, Ok, Err

class EmailSender(Protocol):
    def send(self, to: str, subject: str, body: str) -> Result[None, str]:
        ...
```

Console-based adapter:

```python
class ConsoleEmailSender:
    def send(self, to: str, subject: str, body: str) -> Result[None, str]:
        print(f"To: {to}\nSubject: {subject}\n\n{body}")
        return Ok(None)
```

A small routine using the port:

```python
def send_reset_email(sender: EmailSender, email: str) -> Result[None, str]:
    if "@" not in email:
        return Err("invalid email")

    body = "Click here to reset your password."
    return sender.send(to=email, subject="Reset", body=body)
```

This design remains independent of any HTTP, database, or queueing technology.

---

## 4. Where to Go Next

If you want to see how these ideas can be applied in the context of well-known architectural styles, explore:

- [Clean Architecture](../optional-architectures/clean-architecture.md)
- [Hexagonal Architecture](../optional-architectures/hexagonal-architecture.md)
- [Layered Architecture](../optional-architectures/layered-architecture.md)
- [CQRS](../optional-architectures/cqrs.md)
- [Event-Driven Approaches](../optional-architectures/event-driven.md)

These are **optional** examples — ForgingBlocks does not require or depend on any of them.
