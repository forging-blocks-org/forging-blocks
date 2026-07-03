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

## When to use

Implement `UseCase` for any system capability that coordinates domain objects and outbound ports. Return `Result[OutputType, Error]` so callers handle both outcomes. Keep the class thin — it orchestrates, domain objects decide.

!!! note "Influence: Ivar Jacobson"
    The focus on use cases as units of behavior originates from Ivar Jacobson's work. ForgingBlocks provides a structured, type-safe contract for executing them.

## Message Handler

A **Message Handler** represents an inbound port for a single message type.

Specializations:
- **Command Handler** — Handles commands (`MessageHandler[CommandType, None]`)
- **Event Handler** — Handles domain events (`MessageHandler[EventType, None]`)
- **Query Handler** — Handles queries and returns a typed result (`MessageHandler[QueryType, ResultType]`)

## When to use

Implement a `MessageHandler` when a single message type needs dedicated processing. Use the type aliases — `CommandHandler`, `EventHandler`, `QueryHandler` — to signal intent at the type level.

!!! note "Message-driven architecture"
    Message Handlers enable CQRS, event-driven, and message-driven patterns by decoupling message types from processing logic.
