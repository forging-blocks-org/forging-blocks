# Domain Errors

Domain Errors represent invalid states or rule violations within the problem space.

They express domain meaning, indicate invariant violations, and are not technical failures. They extend the [Foundation](../foundation.md) `Error` base class.

## Concrete error types

- **EntityIdNoneError** — Raised when an entity's identifier is `None` but should be set
- **EntityIdModificationError** — Raised when attempting to change an entity's identifier after it has been assigned
- **EntityIdDeletionError** — Raised when attempting to delete an entity's identifier
- **DraftEntityIsNotHashableError** — Raised because draft (unsaved) entities are not hashable

## When to use

Raise these errors from domain code when an entity's identity contract is violated. They extend the [Foundation](../foundation.md) `Error` base class, so they carry structured messages and metadata consistent with the rest of the system.

All entity errors protect the identity lifecycle — IDs are assigned once, never deleted, and never modified.

!!! note "On error semantics"
    Domain Errors describe *why* something is invalid in domain terms. They should not encode transport, persistence, or framework concerns.
