# Messages

Messages are immutable, architecture-neutral data carriers — **Command**, **Event**, and **Query**.

## Core types

- **MessageMetadata** — Typed metadata container attached to every message at construction.

Concrete messages are immutable data carriers. Classes decorated with `@message_dataclass` or one of its aliases are frozen dataclasses; manually implemented `Message` subclasses are not required to be dataclasses. Their type communicates intent: a Command asks for action, an Event records a fact, and a Query requests data.

## Types

- **Command** — An intent to do something. Handled by a `CommandHandlerPort`. No return value.
- **Event** — Something that happened. Handled by an `EventHandlerPort`. No return value.
- **Query** — A request for data. Handled by a `QueryHandlerPort`. Returns a typed result.

## Message dataclass decorator

The ``@message_dataclass`` decorator creates boilerplate-free, frozen message types. It also supplies the ``_payload``, ``value``, and ``from_payload_fields`` behavior required by the message base classes.

The role-specific aliases use the same decorator implementation, but make the message's architectural intent visible:

- `@command_dataclass` — an intent to perform an action
- `@event_dataclass` — a fact that something already happened
- `@query_dataclass` — a request for data without changing state

The alias does not change runtime behavior. Its advantage is communication: readers, handlers, and type checkers can see the message role immediately.

## Which option should I use?

| Option | Use it when | Main advantage |
| --- | --- | --- |
| A role-specific alias and base class | The message is clearly a command, event, or query | Makes handler contracts and architectural intent explicit |
| ``@message_dataclass`` with ``Message`` | The message is role-neutral or shared by multiple workflows | Keeps reusable message types independent of CQRS roles |
| A manual ``Message`` subclass | Construction, validation, serialization, or mutation rules do not fit the decorator | Gives complete control, at the cost of more boilerplate |

Prefer the first option for application messages. Use the generic decorator when the message is deliberately role-neutral. Choose a manual subclass only when the generated dataclass construction or reconstruction is not sufficient.

## Inheritance patterns

Inherit the concrete message from the role that owns its handler contract, then decorate the concrete class. The decorator recognizes the abstract message members and supplies their implementations:

```python
from forging_blocks.domain.messages.decorators import command_dataclass
from forging_blocks.domain.messages.command import Command

@command_dataclass
class RegisterCustomer(Command[dict[str, str]]):
    email: str
    name: str
```

This pattern is useful because ``RegisterCustomer`` is both a frozen data carrier and a ``Command``. Command handlers can accept ``Command`` values, while the concrete class keeps its typed fields and automatic payload reconstruction.

Use the matching role for the message's meaning:

```python
from forging_blocks.domain.messages.decorators import event_dataclass, query_dataclass
from forging_blocks.domain.messages.event import Event
from forging_blocks.domain.messages.query import Query

@event_dataclass
class CustomerRegistered(Event[dict[str, str]]):
    customer_id: str

@query_dataclass
class FindCustomer(Query[dict[str, str]]):
    customer_id: str
```

The same decorator can be used without a role-specific base when the message is intentionally neutral:

```python
from forging_blocks.domain.messages.decorators import message_dataclass
from forging_blocks.domain.messages.message import Message

@message_dataclass
class CustomerSnapshot(Message[dict[str, str]]):
    customer_id: str
```

A manual subclass is appropriate when you need behavior such as a custom payload object, non-standard validation, or a special serialization format. In that case, implement the abstract ``_payload``, ``value``, and ``from_payload_fields`` members yourself; the decorator is no longer reducing meaningful boilerplate.

!!! note "Related"
    See [Application Use Cases & Handlers](../application/use-cases.md) for how messages are processed.
