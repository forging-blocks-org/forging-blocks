# 🧩 ForgingBlocks

**ForgingBlocks** provides a set of small, composable **foundational contracts** that help you design software with **clarity**, **intent**, and **expressiveness**.

It doesn’t enforce any framework, library, or architectural approach.

Instead, it gives you a **vocabulary** and **building blocks** for structuring ideas in a way that fits your project and your style.

ForgingBlocks relies only on standard features available in **Python 3.12+** (such as Protocols, Generics, and Type Hints), keeping it lightweight and broadly compatible.

---

## 🚀 Getting Started

Install using Poetry, pip or UV:

```bash
poetry add forging-blocks
# or
pip install forging-blocks
# or
uv add forging-blocks
```

**Quick example**:

```python
from forging_blocks.foundation import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)
```

## 🛠️ How can ForgingBlocks help me?

ForgingBlocks helps you keep your project’s structure **clear, intentional, and easy to reason about**.

It offers small, composable **abstractions and interfaces** that support writing clean, testable, and maintainable **Python** code — without tying you to any framework, architecture, or library.

> Not a framework and not an architecture — a **toolkit** you use to forge your own blocks of organization and behavior.

ForgingBlocks does not prescribe how your system must be structured.
Instead, it works alongside whatever style you prefer and can assist with ideas such as:

- Making success and failure **explicit**.
- Creating **clear boundaries** between parts of your system.
- Modeling concepts in ways that express **intent and behavior**.
- Keeping your core logic **independent of technical details**.

You remain in control.

You set the guidelines and conventions that fit your project.

ForgingBlocks simply provides **building blocks** that help you learn, evolve, and write **clean, testable, decoupled, and high-quality** code — fully independent from frameworks or architectural rules.

---

## 🧠 Core Concepts

| Concept | Purpose |
|----------|----------|
| **Result / Ok / Err** | Represents success or failure explicitly. |
| **Mapper / ResultMapper** | Represents a type to map the return into another type. |
| **Debuggable** | Protocol (interface) to force **consistency in how an object's internal state is represented for debugging and logging purposes.**
| **Port / InboundPort / OutboundPort** | Define clear communication boundaries. |

---

## 🏗️ Organizational Blocks

Each block represents a **boundary of responsibility**.

ForgingBlocks provides small abstractions that help you keep these boundaries intentional and easy to understand.

- The **Foundation** block offers the core building blocks reused throughout the system.
- The **Domain** block defines the concepts and rules that model your problem space.
- The **Application** block expresses use cases and coordinates domain behavior.
- The **Infrastructure** block supplies adapters to external systems.
- The **Presentation** block handles incoming interactions with your application.

!!! abstract "Block vs Layer"
    In ForgingBlocks, the term *block* is intentionally architecture-neutral.

    You may interpret a block as a *layer* if that mental model helps, but this toolkit does not require or enforce any architectural style.

---

## 🧭 Why It Matters

Many systems become difficult to evolve not because of missing features, but due to **coupling**, **implicit assumptions**, and **unclear responsibilities**.

ForgingBlocks helps you shape software that is **clear**, **testable**, and **maintainable** by encouraging intentional structure — block by block.

---

## 📚 Learn More

- [Getting Started](guide/getting-started.md)
- [Architecture Overview](guide/architecture.md)
- [Packages & Layers](guide/packages_and_layers.md)
- [Reference Index](reference/index.md)
- [Release Guide](guide/release_guide.md)
