# ForgingBlocks

Composable **abstractions and interfaces** for writing clean, testable, and maintainable Python code.

[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-blue.svg)](https://python-poetry.org/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![CI](https://github.com/forging-blocks-org/forging-blocks/workflows/CI/badge.svg)](https://github.com/forging-blocks-org/forging-blocks/actions/workflows/ci.yml)

---

## 🌱 Overview

> Not a framework — a **toolkit** of composable contracts and abstractions.

**ForgingBlocks** helps you create codebases that are:
- **Clean** — with clear boundaries and intent
- **Testable** — by design, through explicit interfaces
- **Maintainable** — by isolating concerns and dependencies

It doesn’t dictate your architecture.
Instead, it provides **foundations and reusable** abstractions for **forging** your own **blocks**.

Isolate external concerns from your core logic you will achieve systems that are adaptable and resilient.
If you **forge** your own **block** you will achieve software with intent and clarity
If you use **blocks** you will achieve consistency and reusability.
**ForgingBlocks** helps you build systems that last.

You can use it to:
- Learn and apply **architecture and design principles**
- Build **decoupled applications** that scale safely
- Model systems with **type safety and explicit intent**
- Experiment with **Clean**, **Hexagonal**, **DDD**, or **Message-Driven** styles

---

## 🧩 Core Concepts

> Foundations, not frameworks — ForgingBlocks provides the *language* for clean architecture.

This toolkit defines **layer-agnostic foundations** that compose into any design:

- `Result`, `Ok`, `Err` → explicit success/failure handling
- `Port`, `InboundPort`, `OutboundPort` → communication boundaries
- `Entity`, `ValueObject`, `AggregateRoot` → domain modeling
- `Repository`, `UnitOfWork` → persistence contracts
- `Event`, `EventBus`, `CommandHandler` → messaging and orchestration

---

## 🚀 Installation

```bash
poetry add forging-blocks
# or
pip install forging-blocks
# or
uv add forging-blocks
```

**Requires Python 3.14+**

---

## ⚡ Quick Example

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

## 📚 Learn More

- [📘 Documentation](https://forging-blocks-org.github.io/forging-blocks/)
- [🚀 Getting Started Guide](https://forging-blocks-org.github.io/forging-blocks/guide/getting-started/)
- [🏗️ Architecture Overview](https://forging-blocks-org.github.io/forging-blocks/guide/recommended_blocks_structure/)
- [🧱 Principles & Guidelines](https://forging-blocks-org.github.io/forging-blocks/guide/principles/)
- [🧩 Release Process](RELEASE_GUIDE.md)

---

## 🛠️ Development

### Prerequisites

- Python 3.14+
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

```bash
# Clone the repository
git clone https://github.com/forging-blocks-org/forging-blocks.git
cd forging-blocks

# Install dependencies
poetry install

# Run tests
poetry run poe test

# Run full CI suite
poetry run poe ci:check
```

### Available Commands

```bash
# Testing - Primary Commands
poetry run poe test              # Run ALL tests (recommended)
poetry run poe test:unit         # Run unit tests only (fast feedback)
poetry run poe test:integration  # Run integration tests only
poetry run poe test:e2e          # Run end-to-end tests only

# Testing - Alternative Commands
poetry run poe test:debug        # Run tests with verbose output

# Code quality
poetry run poe lint              # Check code style
poetry run poe lint:fix          # Fix code style issues
poetry run poe type              # Type checking
poetry run poe bandit            # Security scanning

# Documentation
poetry run poe docs:build        # Build documentation
poetry run poe docs:generate     # Generate API reference

# Release (maintainers)
poetry run poe release patch        # Test release (simulation)
poetry run poe release patch --execute  # Execute patch release
```

### 🧪 **Test Architecture**

This project uses a **3-tier testing architecture**:

- **Unit Tests** (`@pytest.mark.unit`) - Fast, isolated tests with mocks
- **Integration Tests** (`@pytest.mark.integration`) - Real infrastructure in isolated environments
- **End-to-End Tests** (`@pytest.mark.e2e`) - Complete workflows (mostly skipped)

**Quick feedback during development:**
```bash
poetry run poe test:unit    # ⚡ Fast (~1s) - run frequently
```

**Verify integrations before commits:**
```bash
poetry run poe test         # 🔍 Complete test suite (~3s) - run before commits
```

See [Testing Guide](https://forging-blocks-org.github.io/forging-blocks/guide/testing/) for detailed information.

---

## 🧠 Why It Matters

Most systems fail not because of missing features,
but because of **tight coupling**, **implicit dependencies**, and **unclear responsibilities**.

**ForgingBlocks** helps you *design code intentionally* —
so your system remains testable, extensible, and adaptable as it grows.

---

## 🤝 Contributing

Contributions are welcome! 🎉

1. Fork the repository
2. Install dependencies: `poetry install`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run the full test suite: `poetry run poe ci:check`
6. Submit a pull request with a clear description

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Release Process

For maintainers preparing releases:

```bash
# Prepare release (safe simulation)
poetry run poe release patch

# Execute release (creates branch and PR)
poetry run poe release patch --execute
```

See [RELEASE_GUIDE.md](RELEASE_GUIDE.md) for complete release instructions.

---

## ⚖️ License

MIT — see [LICENSE](LICENSE)

---

_**ForgingBlocks** — foundations for clean, testable, and maintainable Python architectures._
