# Inbound and Outbound Ports

Applications define their own ports by extending the foundation base classes —
[`InboundPort`](../foundation/ports.md#inboundport) and
[`OutboundPort`](../foundation/ports.md#outboundport) — which enforce dependency
direction at class-definition time.

## Inbound Ports

Inbound ports define the **driving side** of the application. They describe *what
can be requested* without exposing internal implementation details.

### ApplicationServicePort[RequestType, ResponseType]

(Also available as `UseCasePort`.) A cohesive unit of behavior. Receives a request
DTO, coordinates domain objects and outbound ports, returns a typed response.

```python
class CreateOrder(ApplicationServicePort[CreateOrderRequest, Result[str, OrderError]]):
    async def execute(self, request: CreateOrderRequest) -> Result[str, OrderError]:
        ...
```

### MessageHandlerPort[MessageType, MessageHandlerResultType]

Reacts to a single message type. Specialized concrete subtypes below.

```python
class MyHandler(MessageHandlerPort[MyMessage, MyResult]):
    async def handle(self, message: MyMessage) -> MyResult:
        ...
```

**`CommandHandlerPort[CommandPayloadType]`** — Fire-and-forget commands (result fixed to `None`).

```python
class ShipOrder(CommandHandlerPort[ShipOrderPayload]):
    async def handle(self, command: Command[ShipOrderPayload]) -> None:
        ...
```

**`EventHandlerPort[EventPayloadType]`** — Fire-and-forget domain events.

```python
class OrderShippedHandler(EventHandlerPort[dict[str, object]]):
    async def handle(self, event: Event[dict[str, object]]) -> None:
        ...
```

**`QueryHandlerPort[QueryPayloadType, QueryResultType]`** — Queries with a return value.

```python
class GetOrderHandler(QueryHandlerPort[GetOrderPayload, OrderDTO]):
    async def handle(self, query: Query[GetOrderPayload]) -> OrderDTO:
        ...
```

### ValidationPort

Validates commands and queries against business rules, returning structured
`RuleViolationError` instances. No generic type parameters.

### AuthorizationPort

Checks permissions, evaluates resource-level access control, and retrieves
effective user roles and permissions. No generic type parameters.

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

## Generic type parameters

Application port classes carry generic type parameters with **no defaults**.
Type arguments must be supplied at the point of inheritance:

```python
# ApplicationServicePort — 2 required type args
class MyUseCase(ApplicationServicePort[MyRequest, MyResponse]):
    ...

# MessageHandlerPort — 2 required type args
class MyHandler(MessageHandlerPort[MyMessage, MyResult]):
    ...

# CommandHandlerPort — 1 required type arg (result fixed to None)
class MyCmdHandler(CommandHandlerPort[MyCommandPayload]):
    ...

# RepositoryPort — 2 required type args
class MyRepo(RepositoryPort[MyAggregate, MyId]):
    ...
```

Omitting type arguments (e.g. `class Foo(ApplicationServicePort):`) will
trigger type-checker errors. Always specify them when inheriting from
generic port classes.
