# Hexagonal Architecture

Hexagonal Architecture, also known as Ports and Adapters, emphasizes separation between core behavior and external systems.

This page shows how **ForgingBlocks concepts can be projected** onto a hexagonal arrangement.

!!! note "Important"
    ForgingBlocks does **not** enforce Hexagonal Architecture.
    This page presents it as an **interpretation** of responsibilities defined in the Reference section.

---

## Quick summary

Hexagonal Architecture (Ports and Adapters) emphasizes separation between core behavior and external systems. This page shows how **ForgingBlocks concepts can be projected** onto this arrangement — **not enforced**.

Mapping:
- **Core** — Domain (business rules) + Application (Use Cases, Handlers)
- **Inbound Ports** — Define how behavior is triggered (UseCasePort, MessageHandlerPort)
- **Outbound Ports** — Define required external capabilities (RepositoryPort, MessageBusPort, UnitOfWorkPort)
- **Adapters** — Implement ports (Infrastructure: SQL repos, message brokers, HTTP clients)
- **Dependencies point toward the core**

Fits when: external systems change frequently; testing without infrastructure matters; inbound/outbound isolation needed.

---

## Conceptual mapping

- The core contains Domain and Application logic.
- Inbound ports define how behavior is triggered.
- Outbound ports define required external capabilities.
- Adapters implement those ports.
- Dependencies point toward the core.

The diagram below shows a **canonical hexagonal view** from the literature, independent of ForgingBlocks.

```mermaid
---
title: Hexagonal Architecture
---
graph LR
    InboundAdapters[Inbound Adapters<br/>HTTP, CLI, Events] -->|execute/handle| ApplicationCore[Application Core<br/>Use Cases & Handlers]
    ApplicationCore -->|dispatch/persist/notify| OutboundAdapters[Outbound Adapters<br/>Repositories, Message Bus]
```

---

## When this style fits

- External systems change frequently.
- Testing without infrastructure is important.
- Inbound and outbound interactions must be isolated.
