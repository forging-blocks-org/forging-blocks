# Foundation
## Shared abstractions and contracts

The **Foundation** block provides low-level, reusable abstractions shared across the entire system. It contains **no domain logic, no application orchestration, and no infrastructure concerns** — only stable contracts and primitives.

Foundation depends on nothing. All other blocks depend on Foundation.

---
## How it works

Foundation is the bottom layer. Every other block imports from it.

Each abstraction serves one focused purpose:

- `Result` replaces exceptions for predictable control flow.
- `Port` defines boundaries as protocols — what is expected, not how.
- `Error` gives structure to failure with messages and metadata.

These are not patterns you must use everywhere. They are tools you reach for when plain Python types stop communicating intent clearly enough.

---
## How to use

Start with the abstractions that give the most immediate value:

1. **`Result`** — Replace functions that return `None` on failure or raise exceptions for control flow. Return `Ok(value)` or `Err(error)` instead.
2. **`Port`** — Define a protocol for any dependency you might swap later: repositories, event buses, loggers.

The Foundation block is pure Python — standard library only. It introduces no framework dependencies.

---
## Core abstractions

- **[Result](foundation/result.md)** — Explicit Ok/Err outcomes without exceptions for control flow
- **[Ports](foundation/ports.md)** — Boundaries between components (InboundPort, OutboundPort)
- **[Errors](foundation/errors.md)** — Structured error model (message + metadata, validation, rule violation, combined)
- **[Auto Decorators](foundation/auto-decorators.md)** — Immutability, equality, and hashing decorators (auto_freeze, auto_eq, auto_hash)
- **[Mappers](foundation/mappers.md)** — Explicit transformations between types
- **[Identified](foundation/identified.md)** — Protocol for objects carrying an identifier
- **[Meta Utilities](foundation/meta.md)** — Runtime enforcement (final, sealed, abstract)

- **[Rules](foundation/rules.md)** — Composable validation rules (ValidationRule)

---
## What it does not do

- Contain domain logic or business rules
- Orchestrate workflows or use cases
- Perform I/O or persistence
- Depend on any external library

---
## Glossary

!!! note "Result"
    A Protocol representing explicit success (Ok) or failure (Err) without exceptions.

!!! note "Port"
    An ABC defining a boundary — what is expected, not how it is implemented.

!!! note "Error"
    A structured failure with a message and metadata, used across all layers.
