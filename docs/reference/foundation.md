# Foundation Package 🧩

The **foundation** package provides minimal, architecture‑neutral primitives.
Nothing in this package assumes Domain‑Driven Design, Hexagonal Architecture,
Clean Architecture, MVC, CQRS, Event Sourcing, or any other structural pattern.

It is intentionally generic and reusable in *any* Python application.

---

## 🧠 Purpose

The goal of the foundation layer is to define **core low‑level contracts** that
support:

- type‑safe communication interfaces
- result handling without exceptions
- structured error representations
- generic data transformation
- optional rich debugging output

These abstractions impose **no architectural boundaries** and can be used
with any style of software design.

---

## ⚙️ Components

---

## Result

A generic type representing either success (**Ok**) or failure (**Err**).
Inspired by Rust's `Result`, but intentionally minimal.

**Key properties:**

- `is_ok` — whether the result is successful
- `is_err` — whether it is an error
- `value` — the underlying success value (raises if accessed on an Err)
- `error` — the underlying error (raises if accessed on an Ok)

### Example

```python
from forging_blocks.foundation import Ok, Err

def divide(a: int, b: int):
    if b == 0:
        return Err("division by zero")
    return Ok(a // b)
```

---

## Mapper

A generic protocol for transforming one type into another.

```python
class Mapper(Generic[SourceType, TargetType], Protocol):
    def map(self, source: SourceType) -> TargetType:
        ...
```

This is entirely architectural‑agnostic: it is just a typed transformation.

---

## ResultMapper

A specialization of `Mapper` for mapping `Result` objects.

This is useful when crossing boundaries such as:

- converting domain outputs into HTTP responses
- converting validation outputs into DTOs
- converting infrastructural results into application results

But the abstraction itself does **not** depend on any architectural layering.

```python
class ResultMapper(
    Generic[AIn, EIn, AOut, EOut],
    Mapper[Result[AIn, EIn], Result[AOut, EOut]],
    Protocol,
):
    ...
```

---

## Port

A minimal protocol representing an interface.

No assumptions are made about what kind of port it is.
No behavior is prescribed.
There is **no requirement** for application/domain layers.

```python
class Port(Generic[InputType, OutputType], Protocol):
    ...
```

Aliases exist only for readability:

- `InboundPort`
- `OutboundPort`
- `InputPort`
- `OutputPort`

These aliases **do not enforce** inbound/outbound concepts — they are just names.

---

## Debuggable

A protocol for exposing a safe string representation for debugging.

This is **not** tied to any architecture and does not prescribe formatting.

```python
class Debuggable(Protocol):
    def as_debug_string(self) -> str:
        ...
```

**Guidelines** (not requirements):

- deterministic output
- no I/O or side effects
- avoid leaking secrets
- use multi‑line formats when helpful

Errors implement this for richer diagnostics.

---

## Error System

The foundation includes a structured error system that supports:

- immutable error messages
- optional metadata
- multi‑error aggregation
- field‑level error grouping
- debuggability through `as_debug_string()`

### Core types

- `ErrorMessage` — immutable wrapper around a string
- `ErrorMetadata` — structured context
- `FieldReference` — identifies a specific field

### Base Error

All structured errors derive from:

```python
class Error(Exception, Debuggable):
    ...
```

Common behavior includes:

- structured message
- optional metadata
- readable `__str__` and `__repr__`
- detailed debug output

### FieldErrors and CombinedErrors

These allow grouping multiple errors:

- errors for a *single field*
- aggregations of multiple errors

They support iteration and debug string introspection.

### Specializations

Examples include:

- `ValidationError`
- `ValidationFieldErrors`
- `CombinedValidationErrors`
- `RuleViolationError`
- `CombinedRuleViolationErrors`
- `CantModifyImmutableAttributeError`

Each one builds on the generic error primitives,
without dictating any usage pattern.

---

## 📦 Public API (Recommended)

```python
from forging_blocks.foundation import (
    Result, Ok, Err,
    Mapper, ResultMapper,
    Port, InboundPort, OutboundPort,
    Debuggable,
    Error, ErrorMessage, ErrorMetadata, FieldReference,
    FieldErrors, CombinedErrors,
    ValidationError, ValidationFieldErrors, CombinedValidationErrors,
    RuleViolationError, CombinedRuleViolationErrors,
    CantModifyImmutableAttributeError,
)
```

This exposes the full foundation without imposing any structural model.

---

## 🧾 Summary

| Aspect | Description |
|--------|-------------|
| **Nature** | Generic, architecture‑neutral primitives |
| **Purpose** | Reusable abstractions for any Python project |
| **Dependencies** | None |
| **Coupling** | Zero architectural assumptions |
| **Usage** | Anywhere in the codebase |

---

This package forms a small, stable core upon which *any* architecture can be built — or none at all.
It provides clarity and consistency without enforcing boundaries.
