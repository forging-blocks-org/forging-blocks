# Application Errors

Application-level errors represent failures that occur during use case execution.

- **UnitOfWorkError** — Transaction commit or rollback failure
- **EventStoreError** — Event append or retrieval failure
- **ConcurrencyError** — Optimistic concurrency conflict
- **EventBusError** — Event publishing failure

## When to use

Raise these errors from application code when a use case fails due to infrastructure or coordination issues. They extend the [Foundation](../foundation.md) `Error` base class, so they carry structured messages and work with the presentation error pipeline.

!!! note "On error boundaries"
    Application errors describe *what failed* during coordination. They should not encode transport or presentation concerns — those belong to outer layers.
