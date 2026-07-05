# Context

Context objects carry metadata through application boundaries — tracing identifiers, user identity, permissions, and transaction state.

## AuthorizationContext

`AuthorizationContext` bundles the information needed for a single authorization decision: the requesting user, their roles, the target resource, and the action being performed.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | `str` | Unique identifier of the user requesting access |
| `roles` | `list[str] \| None` | Roles assigned to the user |
| `resource_id` | `str \| None` | Identifier of the resource being accessed |
| `resource_type` | `str \| None` | Discriminator for the resource kind |
| `action` | `str \| None` | Name of the action being performed |
| `metadata` | `dict[str, Any] \| None` | Arbitrary key-value pairs for cross-cutting concerns |

## ServiceContext

`ServiceContext` carries cross-cutting metadata through every application-service call: a correlation identifier for tracing, the authenticated user, and their permissions.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `correlation_id` | `UUID` | Unique identifier tracing the entire request lifecycle (auto-generated) |
| `user_id` | `str \| None` | Identifier of the authenticated user |
| `permissions` | `list[str]` | Permissions held by the current user |
| `metadata` | `dict[str, Any]` | Arbitrary key-value pairs for tracing and feature flags |

## TransactionContext

`TransactionContext` carries metadata for a single transactional boundary: a unique transaction identifier, the timestamp it began, and the requested isolation level.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `transaction_id` | `UUID` | Unique identifier for the transaction (auto-generated) |
| `started_at` | `datetime` | UTC timestamp when the transaction began |
| `isolation_level` | `IsolationLevel` | Requested isolation level (defaults to `READ_COMMITTED`) |
| `metadata` | `dict[str, Any] \| None` | Arbitrary key-value pairs for cross-cutting concerns |

## When to use

Pass a `ServiceContext` into every application service call for tracing and identity propagation. Use `AuthorizationContext` to bundle the inputs for a permission check. Wrap transactional operations with `TransactionContext` to carry transaction metadata through the boundary.

All context objects are **immutable** — once created, their attributes cannot change. This guarantees that context does not mutate as it passes through layers.

!!! note "Related"
    See [Application Ports](../application/ports.md) for how contexts are consumed by inbound and outbound ports.
