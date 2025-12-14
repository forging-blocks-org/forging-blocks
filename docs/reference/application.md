# Application
## Reference

The **Application** block defines **what the system does**.

It expresses system behavior by coordinating domain concepts, handling incoming requests, and invoking outbound capabilities.
It does **not** contain business rules themselves, nor technical details.

The Application block sits between the outside world and the Domain, acting as a **behavioral boundary**.

---

## Purpose of the Application block

The Application block exists to:

- Represent system behaviors (use cases)
- Coordinate domain operations
- Define inbound and outbound ports
- Delegate technical concerns to Infrastructure

The Application block depends on **Domain** and **Foundation**.
It must not depend on Presentation or Infrastructure implementations.

---

!!! note "On architectural neutrality"
    The Application block does not assume a specific architecture.
    It can be used in layered, hexagonal, clean, CQRS, or message-driven systems.
    The abstractions provided here define boundaries, not control flow.

---

## Responsibilities

The Application block is responsible for:

- Receiving intent from the outside (inbound ports)
- Validating and coordinating operations
- Invoking domain behavior
- Interacting with outbound capabilities
- Defining transactional boundaries

It is **not** responsible for:

- Enforcing domain invariants
- Persisting data directly
- Handling transport or frameworks
- Implementing infrastructure concerns

---

## Inbound Ports

Inbound ports define **how the system can be interacted with**.

They describe *what can be requested* from the application,
without exposing internal implementation details.

---

### Use Case

A **Use Case** represents a cohesive unit of application behavior.

Characteristics:

- Expresses a system capability
- Coordinates domain operations
- Returns an explicit result
- Does not depend on infrastructure

Use Cases describe *what the system does*, not *how it is triggered*.

---

!!! note "Use cases as coordination"
    A Use Case does not contain business rules.
    It orchestrates domain behavior and outbound interactions,
    keeping policy separate from details.

---

### Message Handler

A **Message Handler** represents an inbound boundary for handling messages
such as commands, events, or queries.

Characteristics:

- Reacts to a single message type
- Coordinates application behavior
- Delegates domain logic
- May invoke other outbound ports

Message Handlers allow the application to participate in message-driven or asynchronous workflows.

---

!!! note "Message handling vs use cases"
    Use Cases and Message Handlers serve similar coordination roles.
    The distinction is about *how intent arrives*, not about behavior.

---

## Outbound Ports

Outbound ports define **capabilities the application depends on**.

They allow the Application block to request external actions without knowing how those actions are implemented.

---

### Repository Ports

Repository ports abstract persistence concerns.

Available variants:

- **ReadOnlyRepository** — query-side access
- **WriteOnlyRepository** — command-side persistence
- **Repository** — combined read/write access

Repositories:

- Persist and retrieve aggregates
- Abstract storage mechanisms
- Do not enforce business rules

---

!!! note "CQRS compatibility"
    Separate read and write repositories support CQRS-style designs,
    but using a combined repository is equally valid in simpler systems.

---

### Unit of Work

A **Unit of Work** defines a transactional boundary for application operations.

Responsibilities include:

- Managing a transactional context
- Coordinating multiple repositories
- Committing or rolling back changes
- Publishing domain events upon success

The Unit of Work ensures **consistency across operations**, without embedding domain logic.

---

!!! note "Transactional consistency"
    The Unit of Work coordinates persistence and side effects.
    It does not execute business logic or manipulate aggregates directly.

---

### Message Bus

A **Message Bus** provides a generic mechanism for dispatching messages.

It acts as a connector between the Application block and message-based infrastructure such as in-memory routers, queues, brokers, or external services.

The Message Bus defines *dispatch*, not delivery semantics.

---

### Command Sender

A **Command Sender** allows the application to send commands asynchronously.

Characteristics:

- Fire-and-forget semantics
- Delegates transport to a Message Bus
- Decouples command issuance from handling

Used when the application needs to trigger command-side behavior elsewhere.

---

### Event Publisher

An **Event Publisher** allows the application to publish domain events.

Characteristics:

- Publishes facts that occurred
- Delegates delivery to a Message Bus
- Does not guarantee ordering or durability

Event publishing enables integration and eventual consistency.

---

### Query Fetcher

A **Query Fetcher** allows the application to retrieve data by dispatching queries through a Message Bus.

Characteristics:

- Asynchronous execution
- Result shape defined by the query handler
- No consistency guarantees between read and write models

---

!!! note "Outbound ports and Infrastructure"
    Outbound ports define *what the application needs*.
    Infrastructure provides *how those needs are fulfilled*.

---

## What the Application block does not do

The Application block does **not**:

- Define domain rules
- Manipulate infrastructure directly
- Expose transport-specific APIs
- Depend on frameworks or databases

Those responsibilities belong to Domain, Infrastructure, or Presentation.

---

## Relationship to other blocks

- **Presentation** invokes inbound ports.
- **Application** coordinates behavior.
- **Domain** enforces business rules and invariants.
- **Infrastructure** implements outbound ports.

The Application block remains stable even as delivery mechanisms and infrastructure change.

---

## Summary

The Application block defines **behavioral boundaries**.

It coordinates domain logic through clear inbound and outbound ports, keeping business rules isolated and technical details replaceable.

Its purpose is orchestration, not computation.

---

## Glossary

!!! note "Application Block"
    The part of the system responsible for coordinating behavior.
    It defines what the system does by orchestrating domain logic and invoking external capabilities through ports.

!!! note "Inbound Port"
    An abstraction that defines how external actors can interact with the application, without exposing internal details.

!!! note "Use Case"
    An inbound port that represents a cohesive unit of application behavior.
    A use case coordinates domain operations and outbound interactions, but does not contain business rules itself.

!!! note "Message Handler"
    An inbound port that reacts to a single incoming message (such as a command, event, or query) and coordinates application behavior.

!!! note "Outbound Port"
    An abstraction that represents a capability the application depends on, such as persistence, messaging, or notification, without specifying how that capability is implemented.

!!! note "Repository"
    An outbound port that abstracts access to persisted domain objects.
    Repositories provide retrieval and storage operations without embedding domain rules or storage details.

!!! note "Unit of Work"
    An outbound port that defines a transactional boundary.
    It coordinates multiple persistence operations and ensures consistency across application-level changes.

!!! note "Message Bus"
    An outbound port that dispatches messages to handlers.
    It defines routing and dispatch semantics without prescribing transport, delivery, or infrastructure mechanisms.

!!! note "Command Sender"
    An outbound port used to send commands asynchronously, decoupling command issuance from command handling.

!!! note "Event Publisher"
    An outbound port used to publish domain events, allowing the system to communicate facts that occurred without coupling to consumers or delivery mechanisms.

!!! note "Query Fetcher"
    An outbound port used to retrieve data by issuing queries and receiving responses, typically without mutating state.
