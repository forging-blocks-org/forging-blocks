# Errors

Foundation provides a **structured error model** — every failure carries a message, metadata, and a typed identity.

## Core types

- **Error** — Base class. Carries an `ErrorMessage` and `ErrorMetadata`.
- **ErrorMessage** — A value object representing the human-readable description.
- **ErrorMetadata** — Context dict for extra fields (field name, detail, codes).

## Concrete error types

### Validation
- **ValidationError** — Base for validation failures. Status code: 400.
- **FieldErrors** — Groups errors by field. Carries a field name and child errors.
- **CombinedErrors** — Groups multiple errors from different sources.

### Rule violations
- **RuleViolationError** — Base for business rule failures. Status code: 409.

### Structural errors
- **CantModifyImmutableAttributeError** — Raised when a frozen attribute is reassigned.
- **NoneNotAllowedError** — Raised when `None` is provided where disallowed.
- **NotCallablePredicateError** — Raised when a specification predicate is not callable.
- **ResultAccessError** — Raised when accessing `value` on `Err` or `error` on `Ok`.

All errors extend the `Error` base class and carry structured messages.

## When to use

Subclass `Error` for your own error types. Use `ValidationError` for input failures, `RuleViolationError` for business rule violations. Use `FieldErrors` and `CombinedErrors` to group multiple failures. Every error carries an `ErrorMessage` and `ErrorMetadata` for structured handling.

!!! note "Related"
    See [Domain Errors](../domain/errors.md) and [Application Errors](../application/errors.md) for block-specific error types.
