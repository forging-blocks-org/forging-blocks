# Application
## What the system does

The **Application** block defines system behavior by coordinating domain concepts, handling incoming requests, and invoking outbound capabilities.

It depends on **Domain** and **Foundation**. It must not depend on Presentation or Infrastructure implementations.

---
## How it works

The Application block sits between the outside world and the Domain as a behavioral boundary.

**UseCase flow:**
1. Receives a request through an inbound port.
2. Coordinates domain objects.
3. Invokes outbound ports for persistence or side effects.
4. Returns a `Result[OutputType, Error]`.

A `MessageHandler` follows the same pattern but reacts to a single message type — commands, events, or queries.

Ports define *what* the application needs, never *how*. Outbound ports like `RepositoryPort` or `EventBusPort` are contracts. Infrastructure implements them. The Application block composes them without knowing their implementation.

---
## How to use

Wire up a use case step by step:

1. Define an inbound port for each system capability.
2. Implement it as a `UseCase` class.
3. Inject outbound ports through the constructor — repositories, event buses, loggers.
4. Return `Result[OutputType, Error]` so callers handle both paths explicitly.

Keep use cases thin. They orchestrate; domain objects decide. When a use case grows, extract domain logic into value objects or entities. When it needs new I/O, add an outbound port and implement it in Infrastructure.

---
## Core abstractions

- **[Use Cases](application/use-cases.md)** — Cohesive units of application behavior; coordinate domain + outbound
- **[Message Handlers](application/use-cases.md)** — React to commands, events, and queries
- **[Inbound & Outbound Ports](application/ports.md)** — How the system is interacted with and what it depends on
- **[Application Errors](application/errors.md)** — Structured error types for application-level failures

---
## What it does not do

- Enforce domain invariants
- Persist data directly
- Handle transport or frameworks
- Implement infrastructure concerns

---
## Glossary

!!! note "Use Case"
    An inbound port representing a cohesive unit of application behavior. Orchestrates domain operations and outbound interactions.

!!! note "Message Handler"
    An inbound port that reacts to a single message (command, event, or query).

!!! note "Inbound Port"
    An abstraction defining how external actors interact with the application.

!!! note "Outbound Port"
    An abstraction representing a capability the application depends on (persistence, messaging, etc.).

!!! note "Repository Port"
    An outbound port abstracting access to persisted domain objects.

!!! note "Unit of Work"
    An outbound port defining a transactional boundary across multiple persistence operations.
