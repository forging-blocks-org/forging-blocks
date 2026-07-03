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
- `ValueObject` adds immutability, value equality, and hashing.
- `Specification` composes business rules into testable predicates.

These are not patterns you must use everywhere. They are tools you reach for when plain Python types stop communicating intent clearly enough.

---
## How to use

Start with the abstractions that give the most immediate value:

1. **`Result`** — Replace functions that return `None` on failure or raise exceptions for control flow. Return `Ok(value)` or `Err(error)` instead.
2. **`Port`** — Define a protocol for any dependency you might swap later: repositories, event buses, loggers.
3. **`ValueObject`** — Wrap primitive values when validation logic is scattered across functions.

The Foundation block is pure Python — standard library only. It introduces no framework dependencies.

---
## Core abstractions

- **[Result](foundation/result.md)** — Explicit Ok/Err outcomes without exceptions for control flow
- **[Ports](foundation/ports.md)** — Boundaries between components (InboundPort, OutboundPort)
- **[Errors](foundation/errors.md)** — Structured error model (message + metadata, validation, rule violation, combined)
- **[Messages](foundation/messages.md)** — Command, Event, Query (immutable, architecture-neutral)
- **[Value Objects](foundation/value-objects.md)** — Immutable, value-based equality, hashing
- **[Auto-Freeze](foundation/auto-freeze.md)** — Lightweight immutability without inheriting from ValueObject
- **[Specifications](foundation/specifications.md)** — Composable predicates (and/or/not)
- **[Mappers](foundation/mappers.md)** — Explicit transformations between types
- **[Identified](foundation/identified.md)** — Protocol for objects carrying an identifier
- **[Meta Utilities](foundation/meta.md)** — Runtime enforcement (final, sealed, abstract)

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
    A Protocol defining a boundary — what is expected, not how it is implemented.

!!! note "Error"
    A structured failure with a message and metadata, used across all layers.

!!! note "Message"
    An immutable dataclass representing a command, event, or query.

!!! note "ValueObject"
    An immutable object with value-based equality and hashing.

!!! note "Specification"
    A composable predicate over a candidate object for rules, validation, and filtering.
