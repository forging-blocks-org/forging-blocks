# 🧭 Architecture Guide — Composable, Not Enforced

`building_blocks` is a **toolkit**, not a framework.
It provides small, composable abstractions that let you *build* layered or unlayered systems — Clean Architecture, Hexagonal, or your own composition.

---

## 🔧 Core Philosophy

- **Composable Building Blocks** — you choose how to connect them.
- **Framework Agnostic** — the core never depends on FastAPI, Django, etc.
- **Direction of Dependencies** — always explicit, never hidden.
- **Optional Layers** — domain and application helpers are provided, but not mandatory.
- **Interface First** — protocols and abstract base classes over inheritance.

---

## 🧩 Package Overview

| Package | Intent / Responsibility | Architectural Context |
|----------|-------------------------|------------------------|
| **`foundation`** | Core primitives, interfaces, and result types. | Universal — always safe to use. |
| **`domain`** | Optional base classes for DDD-style modeling (Entities, ValueObjects, Aggregates). | Clean / DDD architectures. |
| **`application`** | Optional orchestration layer (UseCase, Repository, UnitOfWork). | Clean / Hexagonal architectures. |

---

### 🏗️ Foundation — Universal Interfaces

`building_blocks.foundation` defines the *language of composition*:
protocols and helpers that describe how components interact, without prescribing layers.

Includes:
- `Port`, `InboundPort`, `OutboundPort` — direction-agnostic communication contracts
- `Mapper`, `ResultMapper` — value transformations across boundaries
- `Result`, `Ok`, `Err` — functional-style error handling
- `RuleViolationError`, `ValidationError`, etc. — reusable error primitives

✅ **Use this layer anywhere**: monoliths, microservices, CLI tools, or scripts.

---

### 🧱 Domain — Modeling the Core

`building_blocks.domain` helps you express *what your system is*, not *what it does.*

Includes:
- `Entity` — uniquely identified objects
- `AggregateRoot` — clusters of entities with invariant consistency
- `ValueObject` — immutable value semantics
- Domain events and errors

💡 **Optional** — only needed if you model a domain explicitly (e.g., DDD or rich domain design).

---

### ⚙️ Application — Orchestrating Behavior

`building_blocks.application` defines *how* your system interacts.

Includes:
- `UseCase` — an application service or command handler
- `Repository` — persistence abstraction
- `UnitOfWork` — transactional coordination
- Ports (`InboundPort`, `OutboundPort`) — boundary definitions for infrastructure

💡 **Optional** — only needed if you want to organize actions around “use cases” or “ports and adapters.”

---

## 🧭 Suggested Layer Responsibilities

Below are recommended roles when you *choose* to structure your project in layers.
You can omit or merge any depending on your needs.

| Layer | Responsibility | Depends On |
|--------|----------------|-------------|
| **Presentation** | Receives input (API, CLI, UI) and calls the Application layer. | Application |
| **Application** | Orchestrates business rules, coordinates ports and domain services. | Domain + Foundation |
| **Domain** | Core business rules, entities, invariants, events. | Foundation |
| **Infrastructure** | Implements outbound ports, connects to DB, external APIs, queues. | Application / Domain interfaces |

🧠 **Dependency direction:**
Presentation → Application → Domain → Foundation

---

## 🏗️ Architectural Style Recommendations

| Style | How to Apply Building Blocks | Notes |
|--------|------------------------------|--------|
| **Hexagonal (Ports & Adapters)** | Use `InboundPort` for use cases and `OutboundPort` for infrastructure. Implement adapters separately. | Most natural fit; all interfaces already exist. |
| **Clean Architecture** | Use `UseCase`, `Repository`, and `UnitOfWork` to define concentric layers. | Keep dependencies inward. Domain stays pure. |
| **Layered Architecture (Classic)** | Map foundation ports to service/repository boundaries. | Looser boundaries, simpler for smaller apps. |
| **Functional / Lightweight Apps** | Use `Result`, `Mapper`, `Error` primitives directly without layers. | Ideal for scripts, workers, or single-file tools. |
| **Event-Driven / CQRS** | Combine `Result` and `Event` primitives; treat each use case as a handler. | Works with asynchronous or message-based systems. |

---

## 🔍 Visual Overview

```
+------------------------------------------------------------+
|                     Presentation Layer                     |
|    (CLI, Web API, UI, etc.)                                |
+------------------------------------------------------------+
                ↓ calls InboundPort
+------------------------------------------------------------+
|                  Application Layer                         |
|    UseCases, Services, Repositories (Interfaces)            |
+------------------------------------------------------------+
                ↓ depends on
+------------------------------------------------------------+
|                       Domain Layer                         |
|   Entities, ValueObjects, Aggregates, Domain Events         |
+------------------------------------------------------------+
                ↓ uses
+------------------------------------------------------------+
|                     Foundation Layer                       |
|   Result, Port, Mapper, Error, Utility Interfaces           |
+------------------------------------------------------------+
```

---

## 🧩 Takeaways

- **`foundation`** is the universal toolkit — always neutral, always safe.
- **`domain`** and **`application`** are *optional blueprints* for architectural consistency.
- The toolkit adapts to your style: you define how deep your layering goes.
- Clean and Hexagonal are *examples*, not requirements.
- All dependencies and contracts are explicit and type-safe.
