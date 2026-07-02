# Application Errors

Application-level errors represent failures that occur during use case execution.

- **UnitOfWorkError** — Transaction commit or rollback failure
- **EventStoreError** — Event append or retrieval failure
- **ConcurrencyError** — Optimistic concurrency conflict
- **EventBusError** — Event publishing failure

These errors extend the Foundation `Error` base class and carry structured messages and metadata.

!!! note "On error boundaries"
    Application errors describe *what failed* during coordination. They should not encode transport or presentation concerns — those belong to outer layers.
