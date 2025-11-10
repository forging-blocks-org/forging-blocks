# Getting Started 🚀

Welcome to **ForgingBlocks** — a toolkit to help you write clean, testable, and maintainable Python code.

---

## 📦 Installation

You can install it via Poetry

```bash
poetry add forging-blocks
```

Using pip

```bash

pip install forging-blocks
```

Using UV

```bash
uv install forging-blocks
```

or any tool that supports PyPI packages.

---

## 🧩 Quick Example

```python
from forging_blocks.foundation import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)

result = divide(10, 2)
if result.is_ok():
    print(result.value)  # → 5
```

---

## 🧠 Why Use ForgingBlocks?

Most Python codebases grow messy because boundaries are not explicit.

**ForgingBlocks** provides abstractions that make intent and responsibility clear and help you to write decoupled applications.

You can use it to:

* Improve code organization
* Enhance testability
* Facilitate maintenance and evolution
* Teach architecture principles
* Structure new projects with clear layers
* Build layered systems (Clean, Hexagonal, DDD, CQRS, etc.)
* Experiment with architecture concepts safely
* Learn decoupling, ports/adapters, and type-safe composition

---

## 🧱 The Core Components

| Component | Role |
|--------|----------|
| **Foundation** | Core utilities (`Result`, `Port`, `Mapper`) that compose the layers below. It is not an architectural layer. |
| **Domain** | The heart of the system; contains the business rules and domain models (`AggregateRoot`, `Entity`, `ValueObject`). |
| **Application** | Defines the use cases ports (e.g., `CreateUser`, `ProcessOrder`), implement them and orchestrates domain logic. |
| **Infrastructure** | *Adapters* for external concerns (Databases, APIs, Emailing, File Systems). |
| **Presentation** | The *entry points* to your system (REST API endpoints, CLI commands, Message Queue listeners). |

---

## 🧭 Next Steps

- Read the [Architecture Guide](architecture.md)
- Explore [Packages & Layers](packages_and_layers.md)
- Check the [Reference](../reference/index.md)
