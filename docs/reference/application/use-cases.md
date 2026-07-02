# Use Cases and Message Handlers

## Use Case

A **Use Case** represents a cohesive unit of application behavior.

Characteristics:
- Expresses a system capability
- Coordinates domain operations
- Returns an explicit result
- Does not depend on infrastructure

!!! note "Use cases as coordination"
    A Use Case orchestrates domain behavior and outbound interactions, keeping policy separate from details. It does not contain business rules itself.

!!! note "Influence: Ivar Jacobson"
    The focus on use cases as units of behavior originates from Ivar Jacobson's work. ForgingBlocks provides a structured, type-safe contract for executing them.

## Message Handler

A **Message Handler** represents an inbound port for a single message type.

Specializations:
- **Command Handler** — Handles commands (`MessageHandler[CommandType, None]`)
- **Event Handler** — Handles domain events (`MessageHandler[EventType, None]`)
- **Query Handler** — Handles queries and returns a typed result (`MessageHandler[QueryType, ResultType]`)

!!! note "Message-driven architecture"
    Message Handlers enable CQRS, event-driven, and message-driven patterns by decoupling message types from processing logic.
