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

- **`CommandHandlerPort[CommandPayloadType]`** — Handles commands asynchronously with no result payload.

```python
class ShipOrder(CommandHandlerPort[ShipOrderPayload]):
    async def handle(self, command: Command[ShipOrderPayload]) -> None:
        ...
```

- **`EventHandlerPort[EventPayloadType]`** — Handles domain events asynchronously with no result payload.

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
``RuleViolationError`` instances. Parameterized on command and query payload types
(``ValidationPort[CommandPayloadType, QueryPayloadType]``).

```python
class OrderValidator(ValidationPort[dict[str, object], dict[str, object]]):
    async def validate_command(self, command: Command[dict[str, object]]) -> list[RuleViolationError]:
        ...

    async def validate_query(self, query: Query[dict[str, object]]) -> list[RuleViolationError]:
        ...
```

### AuthorizationPort[AuthorizationCheckContext]
Checks permissions, evaluates resource-level access control, and retrieves
effective user roles and permissions for an application-defined context.

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
- **`CommandSenderPort`** — Async command dispatch with no result payload; callers still await completion and errors.
- **`EventPublisherPort`** — Publishes domain events to external consumers.
- **`QueryFetcherPort`** — Asynchronous query dispatch and retrieval.
- **`CachePort`** — Temporary key-value storage.
- **`LoggerPort`** — Abstracted structured logging.
- **`FileSystemPort`** — File read/write/delete operations.
- **`HttpClientPort`** — HTTP requests to external services (GET, POST, PUT, DELETE).
- **`NotifierPort`** — Async notification delivery.

!!! note "Ports and Adapters"
    Outbound ports define *what* the application needs, never *how* it's
    implemented. Infrastructure provides the *how*.

## Generic type parameters

Generic application port classes require their declared type arguments at the point
of inheritance. Non-generic ports include `UnitOfWorkPort`, `LoggerPort`, and
`FileSystemPort`.

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
trigger type-checker errors. Always specify them when inheriting from a generic port class.
