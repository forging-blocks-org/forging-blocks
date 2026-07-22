# CQRS

Command Query Responsibility Segregation separates write behavior from read behavior.

This page shows how **ForgingBlocks concepts can be projected** to support a CQRS-style design.

!!! note "Important"
    ForgingBlocks does **not** require CQRS.
    This page presents it as an **architectural pattern**, not a requirement.

---

## Quick summary

Command Query Responsibility Segregation (CQRS) separates **write behavior** from **read behavior**. This page shows how **ForgingBlocks concepts can be projected** to support CQRS — **not required**.

Mapping:
- **Commands** — Express intent to change state (`Command`, `CommandHandlerPort`, `WriteOnlyRepositoryPort`)
- **Queries** — Retrieve information (`Query`, `QueryHandlerPort`, `ReadOnlyRepositoryPort`)
- **Models may diverge** over time (separate read/write stores with replication)

Fits when: read/write workloads differ significantly; scalability dominates; eventual consistency acceptable.

---

## Conceptual mapping

- Commands express intent to change state.
- Queries retrieve information.
- Read and write responsibilities are separated.
- Models may diverge over time.

The diagram below shows a **canonical CQRS view** from the literature.

```mermaid
---
title: CQRS (Command Query Responsibility Segregation)
---
graph LR
    Client -->|send| CommandHandlerPort[Command Handler]
    Client -->|fetch| QueryHandlerPort[Query Handler]
    CommandHandlerPort -->|save| WriteStore[Write Store<br/>RepositoryPort]
    QueryHandlerPort -->|get_by_id/list_all| ReadStore[Read Store<br/>ReadOnlyRepositoryPort]
    WriteStore -.->|replicate| ReadStore
```

---

## When this style fits

- Read and write workloads differ significantly.
- Scalability concerns dominate.
- Eventual consistency is acceptable.
