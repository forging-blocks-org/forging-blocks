# Foundation
## Foundational abstractions and contracts

The **Foundation** block provides low-level, reusable abstractions that are shared
across the entire system.

It contains **no domain logic**, **no application orchestration**, and
**no infrastructure concerns**.

Foundation exists to define **stable contracts and primitives** on top of which
all other blocks are built.

---

## Purpose

- Supply **primitive abstractions** (`Result`, `Port`, `Mapper`, `Identified`, `ValueObject`, `Message`, `Command`, `Event`, `Query`, plus error and meta utilities).
- Enable explicit, intention-revealing boundaries.
- Support structured and predictable error handling.
- Provide a stable base reused by all other blocks.

---

## Dependency position

```mermaid
flowchart TD
    D[Domain] -->|depends on| F[Foundation]
    A[Application] -->|depends on| F
    A -->|depends on| D
    I[Infrastructure] -->|depends on| A
    I -->|depends on| F
    P[Presentation] -->|depends on| A
    P -->|depends on| F
```

Foundation depends on nothing.
All other blocks may depend on Foundation.

---

## Core concepts

### Result

`Result` models the **explicit outcome** of an operation.

It is used when failure is part of normal behavior, such as:

- validation
- parsing
- rule evaluation
- boundary checks

A `Result` represents either success (`Ok`) or failure (`Err`), without relying on
exceptions for control flow.

Result is about **flow**, not about error representation.

In the codebase, `Result` is a `Protocol` that describes the shared shape of both
variants, while `Ok` and `Err` are the concrete implementations you actually
construct and return.

`Result` supports Python's structural pattern matching through `__match_args__`,
so you can write `match` statements directly against `Ok(...)` and `Err(...)`
patterns.

Common operations on a `Result` include:

- `is_ok` and `is_err` for branching on the variant.
- `value` and `error` for unwrapping the carried payload.
- `map` for transforming the success value while passing errors through.
- `map_error` for transforming the error while passing success through.
- `flat_map` for chaining operations that themselves return a `Result`.
- `get_value_or(default)` for supplying a fallback when the result is an error.
- `get_value_or_else(fn)` for computing a fallback from the carried error.

Accessing the wrong side of a `Result` (for example calling `.value` on an `Err`)
raises a `ResultAccessError`, making invalid access explicit and discoverable.

---

### Errors

Foundation defines a structured **error model**.

Errors represent **what went wrong**, not **how control flows**.

They are:

- structured objects (message + metadata)
- debuggable
- composable and aggregatable
- usable both as return values and raised exceptions

Errors are commonly carried inside `Err`, but the two concepts are distinct:

- `Result` answers *whether* an operation succeeded.
- `Error` answers *why* it failed.

#### Error building blocks

Foundation ships small, reusable data structures that compose the error model:

- `ErrorMessage` carries the human-readable message of an error.
- `ErrorMetadata` carries additional context as a `dict` of structured data.
- `FieldReference` identifies the field an error refers to, when applicable.

These types are intentionally minimal so that any block can build on them
without inheriting domain assumptions.

#### Base error

`Error` is the base class for all structured errors. It:

- inherits from both `Exception` and `Debuggable`, so it can be raised like a
  standard exception and inspected like a debuggable object.
- exposes `.message`, `.metadata`, and a convenience `.context` shortcut.
- provides `as_debug_string()` for rich, multi-line diagnostic output.

#### Specialized errors

Foundation provides a small set of reusable error categories that you can use
directly or extend:

- `NoneNotAllowedError` indicates that a `None` value was supplied where it
  was not allowed.
- `CantModifyImmutableAttributeError` signals an attempt to mutate an
  attribute that was meant to stay immutable, such as on a `ValueObject`.
- `ValidationError` and `ValidationFieldErrors` model input validation
  failures, optionally tied to a specific `FieldReference`.
- `RuleViolationError` and `CombinedRuleViolationErrors` model business rule
  violations, with an aggregator for collecting several at once.
- `CombinedErrors` is a generic aggregator for grouping any `Error` subclass
  under a single failure.
- `FieldErrors` is a generic base for errors associated with a specific field
  that can be iterated and counted like a collection.
- `ResultAccessError` is raised when `.value` or `.error` is read from the
  wrong side of a `Result`.

These error types are architecture-neutral and reusable across domains.

---

### Port

A `Port` represents a **boundary between components**.

Ports define *what is expected*, not *how it is implemented*.
They enable replacement, testing, and decoupling without imposing an architecture.

`Port` is intentionally minimal: a generic `Protocol` parameterized by an
input and output type. The concrete meaning of a port is defined by the
components that extend it.

In addition to the base `Port`, Foundation exposes two pairs of role-marking
aliases that you can use to give a boundary a more specific semantic name:

- `InboundPort` and `InputPort` describe boundaries that **accept input** from
  the outside world.
- `OutboundPort` and `OutputPort` describe boundaries that **produce output**
  towards the outside world.

These aliases are intentionally not prescriptive.
You are free to ignore them and use only `Port`, or to invent your own naming
on top of the same generic shape.

---

### Mapper

`Mapper` defines **explicit transformations** between types.

It makes data conversion intentional and observable, avoiding hidden or
implicit mappings.

`Mapper` is a generic `Protocol` parameterized by a source type and a target
type. Variance is inferred automatically by the type checker, so the same
abstraction can be reused in a wide range of contexts.

---

### Debuggable

`Debuggable` is a lightweight contract for exposing structured debug information.

It enables introspection without leaking internal state or implementation details.

---

### ValueObject

`ValueObject` is the base class for **immutable concepts defined by their values**.

A value object:

- is identified entirely by the values of its attributes, not by a unique id.
- is **immutable** after construction: any attempt to modify an attribute after
  initialization raises a `CantModifyImmutableAttributeError`.
- is hashable, so it can be safely used as a dictionary key or set member.
- implements equality based on its `_equality_components`, which subclasses
  define.

`ValueObject` lives in Foundation because immutability and value-based
equality are generic enough to be reused outside the Domain block as well.
The Domain block simply re-exports the same class so that domain code can
import it from a natural location.

In practice, you can import `ValueObject` from either
`forging_blocks.foundation.value_object` (where the implementation lives)
or from `forging_blocks.domain.value_object` (the re-export). It is not
re-exported from the top-level `forging_blocks.foundation` namespace.

#### Why ValueObject over a frozen dataclass?

Python's `@dataclass(frozen=True)` and `ValueObject` both produce immutable
objects, but they differ in a critical way: **when immutability kicks in**.

| Mechanism | Freeze timing | Can set attrs in `__init__`? | Equality / hashing |
|---|---|---|---|
| `@dataclass(frozen=True)` | Before `__init__` runs | No - Must use `object.__setattr__` in `__post_init__` | Based on all fields (automatic) |
| `ValueObject` (`@auto_freeze`) | **After** `__init__` completes | Yes - Natural `self._x = x` works | Based on `_equality_components` (explicit, selective) |

**Frozen dataclass** prevents *all* `__setattr__` from the moment the object is
created, including inside `__init__`. Any validation or transformation during
initialization must work around this by calling `object.__setattr__`, which is
verbose and error-prone:

```python
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email")
        # Already frozen — self.value = ... would raise FrozenInstanceError
        # Must use object.__setattr__ for any transformation:
        object.__setattr__(self, "value", self.value.lower().strip())
```

**ValueObject** keeps the instance mutable during `__init__`, so you can
validate, transform, and assign attributes naturally. Immutability is
enforced *after* construction via `@auto_freeze`:

```python
class Email(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._value = value.lower().strip()  # Natural assignment

    @property
    def value(self) -> str:
        return self._value

    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
```

Beyond timing, `ValueObject` gives you **four things for free** that a frozen
dataclass requires manual wiring for:

1. **Auto-freeze** — `@auto_freeze` is applied automatically, so every concrete
   subclass becomes immutable with zero boilerplate.
2. **Equality** — you control exactly which fields participate via
   `_equality_components`, rather than relying on all fields automatically.
3. **Hashing** — derived from the same components as equality.
4. **Domain-appropriate error** — raises `CantModifyImmutableAttributeError`
   instead of the generic `FrozenInstanceError`.

**When to use each:**

- Use `ValueObject` when you need domain semantics: selective equality,
  natural `__init__` with validation, and a domain-specific error type.
  This covers the vast majority of domain modeling.
- Use `@dataclass(frozen=True)` when you need a simple, throwaway data holder
  where all-field equality is acceptable and you don't need validation
  during construction.
- Use `@auto_freeze` directly on a dataclass or plain class when you want
  post-init immutability but don't need the value-object semantics
  (equality components, hash, etc.).

---

### Auto-freeze

`@auto_freeze` is a decorator that **automatically freezes instances after
`__init__` completes**, enforcing immutability without requiring subclasses
to call `_freeze()` or add any freeze-related code.

`ValueObject` uses `@auto_freeze` internally so that every concrete subclass
gets immutability for free. You can also apply `@auto_freeze` to your own
classes that need automatic immutability but are not `ValueObject`
subclasses.

A class decorated with `@auto_freeze` must satisfy the `SupportsAutoFreeze`
protocol by providing three methods:

- `freeze_instance()` — transition the instance into an immutable state.
- `unfreeze_instance()` — transition back to mutable (intended for test
  setup and transaction rollback; not for normal application code).
- `should_use_internal_freezing()` — classmethod that returns `True` for
  concrete classes and `False` for abstract intermediate classes that
  should stay unfrozen.

Classes that implement `freeze_attributes(attrs)` can also opt into
**partial freezing**, where only specific attributes (e.g. `"_id"`) are
made immutable while others remain writable. This is useful for Entities
where identity must be fixed but other fields may change over time.

Usage:

```python
from forging_blocks.foundation.autofreeze import auto_freeze


@auto_freeze
class MyImmutableClass:
    def __init__(self, name: str) -> None:
        self._name = name

    def freeze_instance(self) -> None:
        object.__setattr__(self, "__frozen", True)

    def unfreeze_instance(self) -> None:
        object.__setattr__(self, "__frozen", False)

    @classmethod
    def should_use_internal_freezing(cls) -> bool:
        return True

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "__frozen", False):
            msg = (
                f"Cannot modify attribute '{name}' on "
                f"frozen instance of '{type(self).__name__}'"
            )
            raise AttributeError(msg)
        object.__setattr__(self, name, value)
```

Most users won't need `@auto_freeze` directly — extending `ValueObject` is
the simpler path. The decorator is available for cases where you want
automatic immutability without value-object semantics.

---

### Meta utilities

Foundation provides a small set of metaclass utilities for **runtime
enforcement of design intent**.

These tools complement static type-checker hints with checks that run
at class creation time.

- `runtime_final` is a decorator that marks a method as final at runtime.
  Any subclass that tries to override the method fails at class creation
  time, not later.
- `FinalMeta` is a metaclass that enforces `@runtime_final` declarations
  across an inheritance hierarchy.
- `FinalABCMeta` combines `FinalMeta` with `ABCMeta`, so a class can be
  both abstract and runtime-final at the same time.

These utilities are **optional**.
You can use them to express intent clearly, but you are never required
to use them in order to follow the rest of the toolkit.

---

### Identified

`Identified` is a protocol for any object that carries an identifier.

It exposes an `id` property that returns the object's identity, which may be `None` for unpersisted instances.

Any object whose `id` returns its identity satisfies this protocol, making it useful for generic contracts across repositories and infrastructure without coupling to a specific block.

---

### Messages

The Foundation block provides **Messages** as reusable abstractions for expressing intent, facts, and queries within the problem space.

Messages are **immutable** and **architecture-neutral**, making them suitable for use across all blocks in the system.

#### Message

A **Message** is the base abstraction for all messages.

It encapsulates:

- An immutable payload, exposed through the `_payload` property that
  subclasses implement.
- A `MessageMetadata` instance with identity, timestamps, and correlation
  information.

`Message` also exposes convenience shortcuts over its metadata:

- `message_id` returns the unique identifier of the message.
- `created_at` returns the timestamp at which the message was created.
- `to_dict()` returns a dictionary that combines the metadata and the
  payload, useful for serialization.

Equality between messages is based on their `message_id`, so two messages
with identical content but different identities are still considered
different.

`Message` is a base class and is meant to be subclassed rather than used
directly. The Foundation block provides three concrete base classes for the
common roles: `Command`, `Event`, and `Query`.

`MessageMetadata` is intentionally separated from data to avoid leaking
technical concerns into foundation logic. It carries:

- `message_id`, the unique identifier of the message.
- `created_at`, the timestamp at which the message was created.
- `message_type`, the name of the message's class by default.
- `correlation_id`, an identifier used to group related messages that
  belong to the same business process.
- `causation_id`, the identifier of the message that immediately
  preceded this one.

#### Command

A **Command** represents an **intent to perform an action**.

Characteristics:

- Imperative meaning
- Expresses a request to change state
- May be accepted or rejected

Commands model *what someone wants to do* in the application.

Commands also expose two convenience properties over their metadata:

- `command_id` is the unique identifier of the command, equal to `message_id`.
- `issued_at` is the timestamp at which the command was issued, equal to
  `created_at`.

These names are provided as **semantic aliases** so that intent is obvious
in places that talk about commands specifically.

#### Event

An **Event** represents a **fact that has already occurred**.

Characteristics:

- Expressed in the past tense
- Immutable and irreversible
- Records something that happened

Events model *what is known to be true* after a state transition.

Events also expose `occurred_at`, a semantic alias for the timestamp at which
the event was created. The name is meant to reflect how events are usually
read: as something that happened at a specific moment.

#### Query

A **Query** represents an **intent to retrieve information**.

Characteristics:

- Does not modify state
- Expresses interest, not behavior
- Side-effect free

Queries model *what someone wants to know*.

!!! note "Influence: CQRS literature"
    The distinction between Commands, Events, and Queries is inspired by CQRS concepts described by multiple authors, including Greg Young and Vaughn Vernon.
    ForgingBlocks treats these as semantic roles, not architectural mandates.

---

## Characteristics

- Pure Python (standard library only).
- Architecture-neutral.
- Stable, low-level abstractions.
- Used by all other blocks.
