# Messages

Messages are immutable, architecture-neutral data carriers — **Command**, **Event**, and **Query**.

All messages are frozen dataclasses. Their type communicates intent: a Command asks for action, an Event records a fact, a Query requests data. Serialization is handled by codecs in the infrastructure layer (see `DictMessageCodec`).

## Types

- **Command** — An intent to do something. Handled by a `CommandHandlerPort`. No return value.
- **Event** — Something that happened. Handled by an `EventHandlerPort`. No return value.
- **Query** — A request for data. Handled by a `QueryHandlerPort`. Returns a typed result.

## Message dataclass decorator

The ``@message_dataclass`` decorator creates boilerplate-free, frozen message types. Type aliases clarify intent:

- `@command_dataclass` — For commands
- `@event_dataclass` — For domain events
- `@query_dataclass` — For queries

All aliases are the same decorator; the name signals intent. Instances are frozen after construction.

## When to use

Annotate a class with ``@command_dataclass``, ``@event_dataclass``, or ``@query_dataclass``. The decorator handles freezing and wires up reconstruction via ``from_payload_fields``. Choose the alias that matches the message's role — command for intent, event for facts, query for data requests.

!!! note "Related"
    See [Application Use Cases & Handlers](../application/use-cases.md) for how messages are processed.
