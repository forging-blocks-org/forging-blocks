# Clean Architecture

Clean Architecture organizes software around **behavioral boundaries** and dependency rules that protect core policies from external details.

This page shows how **ForgingBlocks concepts can be projected** onto a Clean Architecture arrangement.

!!! note "Important"
    ForgingBlocks does **not** enforce Clean Architecture.
    This page presents it as an **interpretation**, not a required structure.

---

## Quick summary

Clean Architecture organizes software around **behavioral boundaries** and dependency rules that protect core policies from external details. This page shows how **ForgingBlocks concepts can be projected** onto this arrangement — **not enforced**.

Mapping:
- **Inner layers** — Domain (Entities, Value Objects) + Application (Use Cases, Handlers)
- **Outer layers** — Delivery mechanisms, technical details (Frameworks, Drivers, Interface Adapters)
- **Dependencies always point inward**

Fits when: long-term maintainability matters; strict policy/detail separation needed; multiple delivery mechanisms expected.
Consider alternatives when: simplicity > flexibility; strict rules add overhead; system is small/short-lived.

---

## Conceptual mapping

- The inner layers contain Domain and Application policies.
- The outer layers contain delivery mechanisms and technical details.
- Dependencies always point inward.

The diagram below shows the **canonical Clean Architecture view** from the literature, independent of ForgingBlocks.

```mermaid
---
title: Clean Architecture
---
graph TD
    Frameworks[Frameworks & Drivers<br/>DB, Web, External APIs] -->|implement| Adapters[Interface Adapters<br/>Controllers, Presenters, Gateways]
    Adapters -->|execute/handle| Application[Application Business Rules<br/>Use Cases, Handlers]
    Application -->|coordinate| Domain[Enterprise Business Rules<br/>Entities, Value Objects]
```

---

## When this style fits

- Long-term maintainability is a priority.
- Strict separation between policy and details is required.
- Multiple delivery mechanisms are expected.

---

## When to consider alternatives

- Simplicity outweighs flexibility.
- Strict dependency rules add unnecessary overhead.
- The system is small or short-lived.
