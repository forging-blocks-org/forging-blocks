# BuildingBlocks 🧩

Composable **abstractions and interfaces** for clean, testable, and maintainable Python applications.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-blue.svg)](https://python-poetry.org/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

---

## Why Building Blocks?

> Most Python projects start simple but eventually entangle infrastructure and business logic.

**Building Blocks** provides **composable abstractions** — not a framework —
to help you define clear boundaries, separate concerns, and model intent
without enforcing any specific architectural style.

You can use it:
- as a **foundation** for Clean or Hexagonal Architecture
- as **standalone interfaces** (`Result`, `Mapper`, `Port`, `EventBus`)
- or as a **teaching toolkit** for domain-driven, strongly typed design

---

## Overview

This toolkit offers minimal, explicit abstractions for:

- Entities, Value Objects, and Domain Events
- Application Services and Use Cases
- Safe result types for explicit success/failure
- Event buses, Repositories, and Mappers

---

## Features

- 🎯 **Framework Agnostic**: Works with any Python web framework or application type
- 🏛️ **Clean Architecture**: Implements hexagonal architecture patterns
- 🧩 **Domain-Driven Design**: Building blocks for DDD
- 🔒 **Type Safe**: Full type annotations with mypy support
- 🧪 **Well Tested**: Comprehensive test coverage
- ⚡ **Modern Python**: Built for Python 3.9+ with modern syntax

---

## Installation

```bash
poetry add building-blocks
# or
pip install building-blocks
```

---

## Quick Start

```python
from building_blocks.foundation import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)

result = divide(10, 2)
if result.is_ok():
    print(result.value)   # → 5
```

---

## Learn More

- [Architecture Guide](guide/architecture.md)
- [Getting Started](guide/getting-started.md)
- [API Reference](reference/index.md)

---

## Examples

Examples are being migrated to a dedicated repository — link coming soon.

---

## Contributing

Contributions are welcome!
See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions.

---

## License

MIT — see [LICENSE](LICENSE)

---

_Built with ❤️ by [Glauber Brennon](https://github.com/gbrennon) and the [Building Blocks](https://github.com/building-blocks-org) community._
