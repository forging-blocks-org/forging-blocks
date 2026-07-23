# GitHub Copilot Instructions — Forging Blocks Toolkit

**Python Version:** 3.14+
**Project Type:** Python Toolkit/Library — DDD + Hexagonal Architecture + Event Sourcing
**Purpose:** Provide reusable building blocks that applications import to implement domain-driven, hexagonally-structured systems
**Scope:** All PR reviews and code suggestions in `src/forging_blocks/`

---

## What This Project Is

Forging Blocks is a **toolkit**, not an application. It provides:

- Reusable port abstractions (contracts) for applications to depend on
- Domain modeling base classes (Entity, AggregateRoot, ValueObject)
- Foundation utilities (Result, Message, Specification, auto-freeze, errors)
- Concrete infrastructure implementations that are technology-agnostic (in-memory, OS filesystem, stdlib logging)

The toolkit deliberately excludes any integration with third-party dependencies (databases, message brokers, HTTP clients, etc.). Those adapters belong in the applications that consume this toolkit. Applications built with forging-blocks define their **own custom ports** and their own concrete infrastructure adapters.

---

## Port Hierarchy: ABC-Based Abstract Contracts

### How Ports compose in this codebase

Port classes use `ABC(metaclass=FinalABCMeta)` — abstract base classes with
`@abstractmethod` stubs. Explicit inheritance is required; structural
subtyping is not used. In forging-blocks, ports are chained across multiple
levels. Each level is still an ABC, and still has no real implementation.

```
ABC(metaclass=FinalABCMeta)
  └── Port[InputType, OutputType](ABC)           ← foundation marker
        ├── InboundPort[In, Out](Port[In, Out])   ← role marker
        └── OutboundPort[In, Out](Port[In, Out])  ← role marker
              ├── Notifier[T](OutboundPort[T, None])   ← application port
              ├── MessageBus[M, R](OutboundPort[M, R]) ← application port
              ├── Repository[T, Id](...)               ← application port
              └── ...
```

**Key rule:** a class in this chain is a pure abstract contract if and only
if it has `@abstractmethod` stubs and contains only docstrings (no
`__init__`, no instance fields, no real logic).

```python
# CORRECT — abstract port class: has @abstractmethod stubs, no implementation
class Notifier[NotificationType](
    OutboundPort[NotificationType, None],
):
    @abstractmethod
    async def notify(self, message: NotificationType) -> None:
        """Deliver a notification to an external channel."""


# NOT an abstract port — concrete adapter: has __init__ and real method bodies
class EventPublisher[EventPayloadType](OutboundPort[Event[EventPayloadType], None]):
    def __init__(self, message_bus: MessageBus[...]) -> None:
        self._message_bus = message_bus            # ← real field

    async def publish(self, event: Event[EventPayloadType]) -> None:
        await self._message_bus.dispatch(event)   # ← real logic
```

`Port`, `InboundPort`, and `OutboundPort` are **marker ABCs**, not
implementations. They convey semantic intent (this is an inbound/outbound
boundary) and define the lifecycle contract. They do not enforce or provide
behavior.

### Custom ports in application code

Applications importing this toolkit will define their own ports the same way:

```python
# CORRECT — application-defined outbound port (abstract ABC)
from forging_blocks.foundation.ports import OutboundPort
from abc import abstractmethod

class PaymentGateway[PaymentType](OutboundPort[PaymentType, Result[str, PaymentError]]):
    @abstractmethod
    async def charge(self, payment: PaymentType) -> Result[str, PaymentError]:
        """Charge a payment and return the result."""
```

Do **not** flag third-party or application-level `OutboundPort`/`InboundPort`
subclasses as errors. They are the intended usage pattern.

---


## Port Rules

| Characteristic | Pure Port (ABC) | Concrete Adapter |
|---|---|---|
| `@abstractmethod` stubs | ✅ Yes | ❌ No |
| Method bodies | Docstrings only | Real logic |
| `__init__` | Never | Allowed |
| Instance fields | Never | Allowed |
| Purpose | Define contract | Implement contract |

**DO NOT** add implementation to ports.
**DO NOT** add `__init__` to ports.
**DO** flag instance variables on abstract port classes.
**DO** flag real method bodies on abstract ports.

---

## Foundation Block Patterns

### Result Type: Explicit Outcomes

`Result[ValueType, ErrorType]` models explicit success/failure. Never use exceptions for control flow when a `Result` is appropriate.

```python
from forging_blocks.foundation.result import Result, Ok, Err

# Returning explicit outcomes
def parse_email(raw: str) -> Result[Email, str]:
    if "@" not in raw:
        return Err("invalid email")
    return Ok(Email(raw))

# Chaining operations
final: Result[str, MyError] = (
    result
    .map(lambda v: v.upper())
    .flat_map(lambda v: validate(v))
    .map_error(lambda e: wrap_error(e))
)

# Fallback
value = result.get_value_or("default")
value = result.get_value_or_else(lambda err: compute_fallback(err))
```

`Result` is a `Protocol` — `Ok` and `Err` are the concrete variants. Both support `__match_args__` for Python pattern matching.

### Messages: Command / Event / Query

All messages are immutable value objects. Use `@message_dataclass` (or its aliases) to reduce boilerplate:

```python
from forging_blocks.foundation.messages.decorators import event_dataclass, command_dataclass, query_dataclass
from forging_blocks.foundation.messages.event import Event
from forging_blocks.foundation.messages.command import Command
from forging_blocks.foundation.messages.query import Query

@event_dataclass                                    # past tense — something that happened
class OrderShipped(Event[dict[str, object]]):
    order_id: str
    shipped_at: str

@command_dataclass                                  # imperative — intent to act
class ShipOrder(Command[dict[str, object]]):
    order_id: str
    address: str

@query_dataclass                                    # interrogative — request for data
class GetOrder(Query[dict[str, object]]):
    order_id: str
```

Do **not** implement `_payload` manually on decorated classes — the decorator patches it automatically.

### ValueObject: Immutable Domain Values

```python
from forging_blocks.foundation.value_object import ValueObject


class Email(ValueObject[str]):
    __slots__ = ("_value",)      # always include __slots__

    def __init__(self, value: str) -> None:
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email")
        self._value = value

    @property
    def value(self) -> str:
        return self._value
```

Concrete ``ValueObject`` subclasses are automatically frozen and hashable via
`auto_freeze` and `auto_hash` (applied through ``__init_subclass__``).
After ``__init__`` completes, any mutation raises ``CantModifyImmutableAttributeError``.

### Specifications: Composable Predicates

```python
from forging_blocks.foundation.specification import ExpressionSpecification

is_active = ExpressionSpecification(lambda u: u.status == "active", description="is_active")
is_adult  = ExpressionSpecification(lambda u: u.age >= 18)

combined = is_active & is_adult   # AndSpecification
either   = is_active | is_adult   # OrSpecification
negated  = ~is_active             # NotSpecification
```

Composition operators (`&`, `|`, `~`) come from `ComposableSpecification`. Do **not** reimplement them in subclasses.

### Auto-freeze

```python
from forging_blocks.foundation.autofreeze import auto_freeze

@auto_freeze
class Money:
    def __init__(self, amount: int, currency: str) -> None:
        self._amount = amount
        self._currency = currency.upper()
    # Fully immutable after __init__


@auto_freeze(attrs=["_id"])
class User:
    def __init__(self, user_id: str, name: str) -> None:
        self._id = user_id   # frozen — cannot change
        self._name = name    # mutable
```

Abstract classes are skipped by `@auto_freeze`; only concrete leaf classes are frozen.

### Errors

```python
from forging_blocks.foundation.errors.error import Error
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata

class DomainRuleViolated(Error[dict[str, object]]):
    def __init__(self, rule: str) -> None:
        super().__init__(ErrorMessage(f"Rule violated: {rule}"))
```

Errors extend both `Exception` and `Debuggable`. Use `Result[T, E]` to carry errors as values; raise them only when it makes sense at a boundary.

---

## Domain Block Patterns

### Entity: Identity-Based Objects

```python
from forging_blocks.domain.entity import Entity
from uuid import UUID

class User(Entity[UUID]):
    def __init__(self, user_id: UUID, email: str) -> None:
        super().__init__(user_id)
        self._email = email

    @property
    def email(self) -> str:
        return self._email
```

- `_id` is immutable after construction (enforced by `auto_freeze(attrs=["_id"])` applied via `__init_subclass__`)
- Draft entities (`id=None`) are not hashable — check `entity.is_persisted()` before hashing
- Two entities are equal if and only if they have the same type and the same `_id`

### AggregateRoot: Consistency Boundary + Event Sourcing

```python
from forging_blocks.domain.aggregate_root import AggregateRoot
from forging_blocks.foundation.messages.event import Event

class Order(AggregateRoot[UUID]):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(order_id)
        self._items: list[str] = []

    def add_item(self, item_id: str) -> None:
        self.apply(ItemAdded(item_id=item_id))   # records + queues event, increments version

    def _handle(self, event: Event[dict[str, object]]) -> None:
        if isinstance(event, ItemAdded):
            self._items.append(event.item_id)
```

| Method | When to use | Side effects |
|---|---|---|
| `apply(event)` | New command-time transition | Calls `_handle`, increments version, queues event |
| `replay(event)` | Reconstituting from event store | Calls `_handle`, increments version, no queue |
| `record_event(event)` | Integration/non-state events | Queues only, no `_handle`, no version change |
| `collect_events()` | After persistence (Unit of Work) | Drains and returns queue |
| `discard_events()` | On rollback | Clears queue |

`apply`, `replay`, `record_event`, `collect_events`, and `discard_events` are `@runtime_final` — subclasses must not override them. Only `_handle` is `@abstractmethod`.

---

## Application Block Patterns

### Use Cases and Handlers

```python
from forging_blocks.application.ports.inbound.use_case import UseCase

# Inbound port — an ABC
class CreateOrderUseCase(UseCase[CreateOrderRequest, CreateOrderResponse]):
    async def execute(self, request: CreateOrderRequest) -> CreateOrderResponse:
        ...

# Concrete service — implements the port
class CreateOrderService(CreateOrderUseCase):
    def __init__(self, repo: OrderRepository, uow: UnitOfWork) -> None:
        self._repo = repo
        self._uow = uow

    async def execute(self, request: CreateOrderRequest) -> CreateOrderResponse:
        async with self._uow:
            order = Order(order_id=uuid7(), ...)
            self._uow.register_modified(order)
            await self._repo.save(order)
            return CreateOrderResponse(order_id=str(order.id))
```

Use cases accept and return **DTOs** (dataclasses), not domain entities. This keeps the application boundary stable as the domain evolves.

### Unit of Work

```python
async with uow:
    aggregate = await repo.get_by_id(aggregate_id)
    aggregate.add_item(item)
    uow.register_modified(aggregate)
    await repo.save(aggregate)
# On success: commits and publishes collected domain events
# On exception: rolls back and discards events
```

---

## Infrastructure Block

### Concrete Implementations Shipped by the Toolkit

The toolkit ships infrastructure implementations that are **technology-agnostic** — they depend only on the Python standard library and carry no third-party dependencies:

```python
from forging_blocks.infrastructure import (
    InMemoryReadRepository,
    InMemoryWriteRepository,
    InMemoryEventStore,
    InMemoryEventBus,
    InMemoryMessageBus,
    InMemoryUnitOfWork,
    OSFileSystem,       # backed by pathlib + asyncio.to_thread
    StdlibLogger,       # backed by logging module
)
```

These are **first-class implementations**, not test doubles. They exist because the toolkit is technology-agnostic: in-memory is a legitimate runtime strategy (e.g., single-process systems, embedded use), and the OS filesystem and stdlib logger are universal enough to ship without pulling in dependencies.

**What is NOT in this repository:** adapters for specific third-party technologies (SQL databases, Redis, RabbitMQ, S3, HTTP clients, etc.). Those integrations belong in the applications or in separate adapter libraries that consume this toolkit. Do **not** add third-party dependencies to `src/forging_blocks/`.

### Serializable Protocol

```python
from forging_blocks.infrastructure.serialization import Serializable

# Structural — no inheritance needed
class MyMessage:
    def to_dict(self) -> dict[str, object]: ...

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "MyMessage": ...
```

Any class with matching `to_dict` / `from_dict` satisfies `Serializable` structurally.

---

## Modern Python 3.14 Requirements

```python
# CORRECT
class Container[T]:          # PEP 695 — not Generic[T]
    def get(self) -> T | None: ...   # PEP 604 — not Optional[T]

# WRONG
class Container(Generic[T]):
    def get(self) -> Optional[T]: ...
```

- `T | None` not `Optional[T]`
- `A | B` not `Union[A, B]`
- `class Foo[T]:` not `class Foo(Generic[T]):`
- All external I/O must be `async def` with `await`
- Never use bare `Any`

---

## Metaclass Utilities

```python
from forging_blocks.foundation import FinalABCMeta, runtime_final

class MyBase(metaclass=FinalABCMeta):
    @runtime_final
    def sealed_method(self) -> None:
        ...  # subclasses cannot override this

    @abstractmethod
    def required_method(self) -> None: ...
```

`@runtime_final` raises `TypeError` at **class creation time** if a subclass tries to override the method. Used heavily in `AggregateRoot` to protect the event sourcing contract.

---

## Docstrings

All public types and methods must have docstrings with explicit Responsibilities / Non-Responsibilities sections for ports:

```python
from abc import abstractmethod

class MyPort[T](OutboundPort):
    """Contract for sending notifications.

    Responsibilities:
        - Deliver messages to an external channel.

    Non-Responsibilities:
        - Guarantee delivery.
        - Implement retry logic.
    """

    @abstractmethod
    async def send(self, message: T) -> None:
        """Send a notification message.

        Args:
            message: The message to deliver.

        Notes:
            - Fire-and-forget.
            - Delivery semantics are infrastructure-defined.
        """
```

---

## Common Mistakes to Flag

| Pattern | Status | Fix |
|---|---|---|
| `Optional[T]` | ❌ Flag | Use `T \| None` |
| `Union[A, B]` | ❌ Flag | Use `A \| B` |
| `Generic[T]` in class signature | ❌ Flag | Use `class Foo[T]:` |
| Instance variables on an abstract port class | ❌ Flag | Remove — ABCs are contracts, not classes |
| Real method body on an abstract port | ❌ Flag | Replace with docstring-only stub |
| Blocking I/O in async context | ❌ Flag | Add `async def` / `await` |
| Manual `_payload` on `@event_dataclass` class | ❌ Flag | Decorator patches it automatically |
| Missing `__slots__` on ValueObject subclass | ❌ Flag | Add `__slots__ = ("_field",)` |
| `try/except` for control flow | ❌ Flag | Use `Result[T, E]` |
| Overriding `@runtime_final` method | ❌ Flag | `TypeError` at class creation |
| Overriding `apply`, `replay`, `collect_events` in AggregateRoot | ❌ Flag | These are runtime-final |
| Missing docstring on public API | ❌ Flag | Add Google-style docstring |

---

## Do NOT Flag These (Correct Patterns)

- `class Foo[T](OutboundPort):` — valid abstract port class
- `class Foo[T](InboundPort):` — same
- `async def method(self) -> None:` with docstring-only body — valid abstract method
- `ABC` appearing at 2nd, 3rd, or deeper inheritance level — this is intentional
- Applications subclassing `OutboundPort`/`InboundPort` for their own custom ports
- `@abstractmethod` with docstring body on ports — correct abstract stub
- Lazy imports inside composition methods (avoids circular imports)
- `@runtime_final` and `FinalABCMeta` together — standard toolkit metaclass pattern
- `@event_dataclass` / `@command_dataclass` / `@query_dataclass` decorators
- `Message` subclasses without manual `_payload` if decorated with `@message_dataclass`
- `ValueObject` subclasses without explicit `@auto_freeze` — it is applied automatically via `__init_subclass__`
- Multiple ABC inheritance — valid for composing port contracts
