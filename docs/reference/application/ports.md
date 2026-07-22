# Inbound and Outbound Ports

Applications define their own ports by extending the foundation base classes —
[`InboundPort`](../foundation/ports.md#inboundport) and
[`OutboundPort`](../foundation/ports.md#outboundport) — which enforce dependency
direction at class-definition time.

## Inbound Ports

Inbound ports define the **driving side** of the application. They describe *what
can be requested* without exposing internal implementation details.

- **`ApplicationServicePort`** (also available as `UseCasePort`) — A cohesive
  unit of behavior. Receives a request DTO, coordinates domain objects and
  outbound ports, returns a typed response.
- **`MessageHandlerPort`** — Reacts to a single message type. Specialized concrete
  subtypes: `CommandHandlerPort` (fire-and-forget commands), `EventHandlerPort`
  (fire-and-forget events), and `QueryHandlerPort` (queries with results).
- **`ValidationPort`** — Validates commands and queries against business rules,
  returning structured `RuleViolationError` instances.
- **`AuthorizationPort`** — Checks permissions, evaluates resource-level access
  control, and retrieves effective user roles and permissions.

## Outbound Ports

Outbound ports define the **driven side** — *what the application needs* from the
outside world. Infrastructure implements these.

- **`ReadOnlyRepositoryPort`**, **`WriteOnlyRepositoryPort`**, **`RepositoryPort`**
  — Persistence abstraction. `RepositoryPort` combines read and write; the
  separated variants support CQRS read/write splitting.
- **`SpecificationRepositoryPort`** — Read repository with specification-based
  queries.
- **`UnitOfWorkPort`** — Transactional boundary across multiple operations.
- **`TransactionManagerPort`** — Explicit transaction control (begin/commit/rollback)
  with transactional function execution.
- **`EventBusPort`** — In-process event publishing (multi-handler fan-out) and
  command sending (single-handler routing).
- **`MessageBusPort`** — Generic async dispatch for commands, queries, or events
  via external transport (queues, brokers, in-memory routers).
- **`EventStorePort`** — Append-only persistence for event-sourced aggregates
  with optimistic concurrency.
- **`CommandSenderPort`** — Async fire-and-forget command dispatch.
- **`EventPublisherPort`** — Publishes domain events to external consumers.
- **`QueryFetcherPort`** — Asynchronous data retrieval from remote sources.
- **`CachePort`** — Temporary key-value storage.
- **`LoggerPort`** — Abstracted structured logging.
- **`FileSystemPort`** — File read/write/delete operations.
- **`HttpClientPort`** — HTTP requests to external services (GET, POST, PUT, DELETE).
- **`NotifierPort`** — Async notification delivery.

!!! note "Ports and Adapters"
    Outbound ports define *what* the application needs, never *how* it's
    implemented. Infrastructure provides the *how*.
