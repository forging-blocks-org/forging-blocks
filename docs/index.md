# 🧩 ForgingBlocks

**ForgingBlocks** provides a set of small, composable **foundational contracts** that help you design software with **clarity**, **intent**, and **expressiveness**.

It doesn’t enforce any framework, library, or organizational approach.

Instead, it gives you a **vocabulary** and **building blocks** for shaping ideas in a way that fits your project and your style.

ForgingBlocks relies only on standard features available in **Python 3.12+** (such as `Protocols`, `Generics`, and Type Hints), keeping it lightweight and broadly compatible.

---

## 🚀 Getting Started

Install using Poetry, pip or UV:

```bash
pip install forging-blocks
# or
poetry add forging-blocks
# or
uv add forging-blocks
```

**Quick example**:

```python
from forging_blocks.foundation import Result, Ok, Err

def divide_quotient_only(dividend: int, divisor: int) -> Result[int, str]:
    if divisor == 0:
        return Err("Division by zero")

    quotient = dividend // divisor

    return Ok(quotient)
```

Or that operation with a remainder:

```python
def divide_with_remainder(dividend: int, divisor: int) -> Result[tuple[int, int], str]:
    if divisor == 0:
        return Err("Division by zero")

    quotient = dividend // divisor
    remainder = dividend % divisor

    return Ok((quotient, remainder))
```

---

🛠️ How can ForgingBlocks help me?

ForgingBlocks helps you keep your project's structure clear, intentional, and easy to reason about.

It provides small, composable abstractions that support writing clean, testable, and maintainable Python code — without tying you to any framework or architectural pattern.

**Not a framework. Not an architecture. A toolkit for forging your own building blocks.**

ForgingBlocks doesn't prescribe how your system must be structured.
Instead, it works alongside your preferred style and supports practices like:

- Making success and failure explicit
- Creating clear boundaries between components
- Modeling domain concepts that express intent
- Keeping core logic independent of infrastructure concerns

**You remain in control.**

You define the guidelines and conventions that fit your project.

ForgingBlocks simply provides the building blocks that help you write decoupled, testable, high-quality code — free from framework lock-in.

---

## 🧠 Core Concepts

| Concept | Purpose |
|----------|----------|
| **Result / Ok / Err** | Represents success or failure explicitly. |
| **Mapper / ResultMapper** | Transforms values or Results into another type. |
| **Debuggable** | Protocol ensuring an object exposes a clear, consistent debug representation. |
| **Port / InboundPort / OutboundPort** | Define explicit communication boundaries. |

---

## 🏗️ Organizational Blocks

Each block represents a **boundary of responsibility**.

ForgingBlocks provides small abstractions that help you keep these boundaries intentional and easy to understand.

- The **Foundation** block offers the core building blocks reused throughout the system.
- The **Domain** block defines the concepts and rules that model your problem space.
- The **Application** block expresses use cases and coordinates domain behavior.
- The **Infrastructure** block supplies adapters to external systems.
- The **Presentation** block handles incoming interactions with your application.

!!! note "Block vs Layer"
    In ForgingBlocks, the term *block* is intentionally architecture-neutral.
    You may interpret a block as a *layer* if that mental model helps, but this toolkit does not require or enforce any structural pattern.

---

## 🧭 Why It Matters

Many systems become difficult to evolve not because of missing features, but due to **coupling**, **implicit assumptions**, and **unclear responsibilities**.

ForgingBlocks helps you shape software that is **clear**, **testable**, and **maintainable** by encouraging intentional structure — block by block.

---

## 📚 Learn More

- [Getting Started](guide/getting-started.md)
- [Blocks Overview](guide/recommended_blocks_structure.md)
- [Organizing Your Project](guide/principles.md)
- [Reference Index](reference/index.md)
- [Release Guide](RELEASE_GUIDE.md)
