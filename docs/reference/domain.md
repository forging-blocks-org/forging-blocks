# Domain
## The problem space

The **Domain** block models the concepts, rules, and constraints of your problem space — independent of frameworks, databases, or delivery mechanisms.

It depends only on **Foundation**. It must not depend on Application, Infrastructure, or Presentation.

---
## How it works

Domain code expresses *meaning* through typed abstractions rather than primitives.

- `Entity` — Carries identity through its lifecycle. Two entities with identical values are still distinct.
- `ValueObject` — Captures a concept by its values alone. Immutable and hashable.
- `AggregateRoot` — Wraps related entities inside a consistency boundary, protecting invariants.
- `Specification` — Composes rules into testable, reusable predicates.

These abstractions are optional tools. You reach for them when plain types stop communicating intent.

---
## How to use

Start small and promote as complexity grows:

1. **`ValueObject`** — When the same validation logic is scattered across functions, wrap it into a typed value.
2. **`Entity`** — When two instances with the same values must be distinguishable, give it an identity.
3. **`AggregateRoot`** — When a group of objects must stay consistent together, define a boundary around them.

The Domain block is the innermost ring. It imports nothing from outer layers. When you change a database or a framework, domain code should not need to change.

---
## Core abstractions

- **[Entity](domain/entities.md)** — Identity matters over time; identity-based equality
- **[Value Object](domain/value-objects.md)** — Immutable, defined by its values; prevents primitive obsession
- **[Aggregate Root](domain/aggregates.md)** — Consistency boundary; controls mutation and invariants
- **[Specification](domain/specifications.md)** — Composable predicates for business rules, querying, and validation
- **[Messages](domain/messages.md)** — Command, Event, Query (immutable, architecture-neutral)
- **[Domain Errors](domain/errors.md)** — Invalid states and rule violations in domain terms
- **[Validators](domain/validators.md)** — Concrete validation rules (RequiredValidator, EmailValidator, LengthValidator, RangeValidator)
- **[Permissions](domain/permissions.md)** — Composable permission checkers (RoleBased, ResourceBased, Composite)

---
## What it does not do

- Orchestrate workflows or use cases
- Perform I/O or persistence
- Depend on frameworks or external systems
- Handle transport or presentation concerns

---
## Glossary

!!! note "Entity"
    A concept with a stable identity that persists over time, even as attributes change.

!!! note "Value Object"
    An immutable concept defined entirely by its values, without independent identity.

!!! note "Aggregate Root"
    A consistency boundary that controls access to related state and protects invariants.

!!! note "Specification"
    A composable predicate over a candidate object for business rules, querying, and validation.
!!! note "Message"
    An immutable dataclass representing a command, event, or query.
