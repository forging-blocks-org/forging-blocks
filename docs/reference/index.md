# Reference Index 🧩

Welcome to the **BuildingBlocks Reference** —
a detailed look at each architectural layer and its responsibilities.

This section provides **layer-by-layer documentation** of the toolkit’s design,
illustrating how **clean boundaries**, **ports**, and **contracts** work together
to create maintainable and framework-agnostic systems.

---

## 🧱 Layer Overview

| Layer | Responsibility | Depends On |
|--------|----------------|------------|
| [Foundation](foundation.md) | Core abstractions and contracts (`Result`, `Port`, `Mapper`) | None |
| [Domain](domain.md) | Business rules, Entities, Value Objects, Domain Events | Foundation |
| [Application](application.md) | Use cases, orchestration, inbound/outbound ports | Domain, Foundation |
| [Infrastructure](infrastructure.md) | Adapters and integrations (DB, messaging, I/O) | Application, Domain |
| [Presentation](presentation.md) | Entry points (API, CLI, events) | Application |

---

## 🧩 Architecture Diagram

```mermaid
graph TD
    A[Presentation Layer] -->|Invokes| B[Application Layer]
    B -->|Uses| C[Domain Layer]
    C -->|Depends on| D[Foundation Layer]
    B -->|Delegates to| E[Infrastructure Layer]
    style A fill:#2a2a2a,stroke:#555,color:#fff
    style B fill:#333,stroke:#555,color:#fff
    style C fill:#444,stroke:#555,color:#fff
    style D fill:#555,stroke:#777,color:#fff
    style E fill:#222,stroke:#666,color:#fff
```

---

## 🧠 How to Read This Section

- Each page in this reference documents **a single architectural layer**.
- Use it to explore dependencies, principles, and examples of real-world composition.
- The **Foundation** package defines reusable primitives.
  Higher layers build on top of these abstractions, never the other way around.

---

## 🔗 Quick Links

- [Foundation](foundation.md)
- [Domain](domain.md)
- [Application](application.md)
- [Infrastructure](infrastructure.md)
- [Presentation](presentation.md)

---

## ✅ Summary

Each layer plays a distinct role in your architecture.
By following the dependency direction (downward arrows in the diagram),
you maintain **clarity**, **testability**, and **modularity** throughout your project.

> “Architecture is the shape of intent — code is just the execution of that intent.”
