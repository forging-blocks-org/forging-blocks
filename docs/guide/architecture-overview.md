# ForgingBlocks — Simplified Architecture Overview

This document provides a clear, layered explanation of how applications built with ForgingBlocks are typically structured.
It replaces the previous all-in-one diagram with **three focused diagrams**, each capturing a single conceptual dimension.
---
## Quick summary

This document provides a **clear, layered explanation** of how ForgingBlocks applications are typically structured, using **three focused diagrams** (each capturing one conceptual dimension) instead of one overwhelming diagram.

Diagrams:
1. **High-Level Architectural Layers** — Request flow: Presentation → Application → Domain; Infrastructure implements outbound ports
2. **Domain Composition** — Internal domain structure: Aggregates enforce invariants; Entities hold identity/state; Value Objects are immutable; Events capture changes
3. **Ports & Adapters (Hexagonal View)** — How Application communicates outward: Presentation calls inbound ports; Application owns/defines ports; Infrastructure implements outbound ports; dependencies point inward

Key principle: **Presentation never calls Infrastructure directly**. Application defines ports; Infrastructure implements them.

Includes a minimal TL;DR diagram for quick reference.

---
A macro overview showing how requests flow through the system.

```mermaid
flowchart LR
    P[Presentation Layer<br/>Controllers • Handlers • UI] --> A[Application Layer<br/>Use Cases • Application Services]
    A --> D[Domain Layer<br/>Aggregates • Entities • Value Objects • Events]
    A --> OP[Outbound Ports]
    IP[Inbound Ports] --> A
    OP --> I[Infrastructure Layer<br/>Adapters • Implementations]
```

### Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **Presentation** | Receives input, validates format, invokes use cases. |
| **Application** | Orchestrates workflows, uses the domain, defines ports. |
| **Domain** | Pure business rules and invariants. |
| **Infrastructure** | External concerns (DB, APIs, files, messaging). |

---

# 2. Domain Composition

A focused view of the internal structure of the domain model.

```mermaid
flowchart TB
    AG[Aggregate] --> ENT[Entities]
    ENT --> VO[Value Objects]
    AG --> EVT[Events]
```

### Notes

- Aggregates enforce invariants.
- Entities hold identity and mutable state.
- Value Objects represent immutable validated concepts.
- Events capture domain changes.

---

# 3. Ports & Adapters (Hexagonal View)

Shows how the application communicates with the outside world.

```mermaid
flowchart LR
    P[Presentation] --> IP[Inbound Port]
    IP --> S[Application Service]
    S --> OP[Outbound Port]
    OP --> ADP[Infrastructure Adapter]
```

### Key Principles

- Presentation does not call Infrastructure directly.
- Application owns and defines ports.
- Infrastructure implements outbound ports.
- Dependencies always point inward toward the core.

---

# 4. Summary

These three diagrams together provide a cohesive view of how ForgingBlocks applications are structured:

- **Layers Diagram** → overall system flow
- **Domain Composition Diagram** → internal domain structure
- **Ports & Adapters Diagram** → boundary interactions

This separation reduces cognitive load and clarifies the responsibilities of each part of the system.

---

# 5. Minimal TL;DR Diagram

```mermaid
flowchart LR
    P --> A --> D
    A --> Ports
    Ports --> Infra
```
