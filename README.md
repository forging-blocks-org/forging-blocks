# BuildingBlocks 🧩

Composable **abstractions and interfaces** for writing clean, testable, and maintainable Python code.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-blue.svg)](https://python-poetry.org/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

---

## 🌱 What Is BuildingBlocks?

> Not a framework — a **toolkit** of composable contracts and abstractions.

**BuildingBlocks** helps you create codebases that are:
- **Clean** — with clear boundaries and intent
- **Testable** — by design, through explicit interfaces
- **Maintainable** — by isolating concerns and dependencies

It doesn’t dictate your architecture.
Instead, it provides **foundations and reusable building blocks** for designing software with intent and clarity.

You can use it to:
- Learn and apply **architecture and design principles**
- Build **decoupled applications** that scale safely
- Model systems with **type safety and explicit intent**
- Experiment with **Clean**, **Hexagonal**, **DDD**, or **message-driven** styles

---

## 🧩 Core Idea

> Foundations, not frameworks.
> You choose the architecture — BuildingBlocks provides the language.

This toolkit defines **layer-agnostic foundations** that compose into any design:

- `Result`, `Ok`, `Err` → explicit success/failure handling
- `Port`, `InboundPort`, `OutboundPort` → communication boundaries
- `Entity`, `ValueObject`, `AggregateRoot` → domain modeling
- `Repository`, `UnitOfWork` → persistence contracts
- `Event`, `EventBus`, `CommandHandler` → messaging and orchestration

---

## 🚀 Installation

```bash
poetry add building-blocks
# or
pip install building-blocks
```

---

## ⚡ Quick Example

```python
from building_blocks.foundation import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)

result = divide(10, 2)
if result.is_ok():
    print(result.value)  # → 5
```

---

## 📚 Learn More

- [Getting Started Guide](guide/getting-started.md)
- [Architecture Guide](guide/architecture.md)
- [API Reference](reference/index.md)

---

## 🧠 Why It Matters

Most systems fail not because of missing features,
but because of **tight coupling**, **implicit dependencies**, and **unclear responsibilities**.

**BuildingBlocks** helps you *design code intentionally* —
so that your system remains testable, extensible, and adaptable as it grows.

---

## 💡 Examples

Educational examples are being migrated to a dedicated repository (coming soon).
They include both **good practices** and **intentional anti-patterns** to teach design reasoning.

---

## 🤝 Contributing

Contributions are welcome!
See [CONTRIBUTING.md](CONTRIBUTING.md) for environment setup and workflow.

---

## ⚖️ License

MIT — see [LICENSE](LICENSE)

---

_Built with ❤️ by [Glauber Brennon](https://github.com/gbrennon) and the [Building Blocks](https://github.com/building-blocks-org) community._
