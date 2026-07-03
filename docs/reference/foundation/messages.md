# Messages

Messages are immutable, architecture-neutral data carriers — **Command**, **Event**, and **Query**.

All messages are frozen dataclasses with automatic serialization support (`to_dict`). Their type communicates intent: a Command asks for action, an Event records a fact, a Query requests data.

## Types

- **Command** — An intent to do something. Handled by a `CommandHandler`. No return value.
- **Event** — Something that happened. Handled by an `EventHandler`. No return value.
- **Query** — A request for data. Handled by a `QueryHandler`. Returns a typed result.

## Message dataclass decorator

The `@message_dataclass` decorator creates boilerplate-free, frozen message types with automatic `to_dict()` and `from_dict()` support. Type aliases clarify intent:

- `@command_dataclass` — For commands
- `@event_dataclass` — For domain events
- `@query_dataclass` — For queries

All aliases are the same decorator; the name signals intent. Instances are frozen after construction.

!!! note "Related"
    See [Application Use Cases & Handlers](../application/use-cases.md) for how messages are processed.
