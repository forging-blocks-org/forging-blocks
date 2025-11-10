# 🧩 BuildingBlocks

Composable **abstractions and interfaces** for writing clean, testable, and maintainable Python code.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-blue.svg)](https://python-poetry.org/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

---

## 🌱 Overview

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
- Experiment with **Clean**, **Hexagonal**, **DDD**, or **Message-Driven** styles

---

## 🧩 Core Concepts

> Foundations, not frameworks — BuildingBlocks provides the *language* for clean architecture.

This toolkit defines **layer-agnostic foundations** that compose into any design:

- `Result`, `Ok`, `Err` → explicit success/failure handling
- `Port`, `InboundPort`, `OutboundPort` → communication boundaries
- `Entity`, `ValueObject`, `AggregateRoot` → domain modeling
- `Repository`, `UnitOfWork` → persistence contracts
- `Event`, `EventBus`, `CommandHandler` → messaging and orchestration

---

## 🚀 Installation

```bash
poetry add building-blocks-toolkit
# or
pip install building-blocks-toolkit
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

- [📘 Documentation](https://building-blocks-org.github.io/building-blocks/)
- [🚀 Getting Started Guide](docs/guide/getting-started.md)
- [🏗️ Architecture Overview](docs/guide/architecture.md)
- [🧱 Packages & Layers](docs/guide/packages_and_layers.md)
- [🧩 Release Process](docs/guide/release_guide.md)

---

## 🧠 Why It Matters

Most systems fail not because of missing features,
but because of **tight coupling**, **implicit dependencies**, and **unclear responsibilities**.

**BuildingBlocks** helps you *design code intentionally* —
so your system remains testable, extensible, and adaptable as it grows.

---

## 🤝 Contributing

Contributions are welcome! 🎉

1. Fork the repository
2. Install dependencies with Poetry
3. Run tests and lint checks:
   ```bash
   poetry run poe ci:simulate
   ```
4. Submit a pull request with a clear description of your improvement

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## ⚖️ License

MIT — see [LICENSE](LICENSE)

---

_**BuildingBlocks Toolkit** — foundations for clean, testable, and maintainable Python architectures._
