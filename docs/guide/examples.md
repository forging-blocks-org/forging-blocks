# Architecture Examples 🧩

This section illustrates how to apply **BuildingBlocks** in different contexts and architectural styles.

---

## ⚡ Example 1 — Clean Architecture (Typical Web App)

```mermaid
flowchart TD
    A[HTTP Request] --> B[Controller]
    B --> C[Use Case]
    C --> D[Domain Entity]
    C --> E[Repository Port]
    E --> F[Infrastructure Adapter]
    F --> G[(Database)]
```

### Flow
1. The **controller** receives a request and creates a command.
2. The **application use case** executes it through an **inbound port**.
3. The use case manipulates **domain entities**.
4. It calls **outbound ports** (repositories, buses).
5. The **infrastructure layer** fulfills those ports.

---

## ⚙️ Example 2 — Event-Driven Architecture

```mermaid
sequenceDiagram
    participant Domain as Domain Layer
    participant App as Application Layer
    participant Bus as EventBus (Infrastructure)
    participant External as External Service

    Domain->>App: Publish DomainEvent
    App->>Bus: EventHandler sends event
    Bus->>External: Notify via message broker
```

Events decouple the system, allowing **asynchronous workflows** and **CQRS-style read models**.

---

## 🧩 Example 3 — CQRS

```mermaid
flowchart LR
    A[Command] --> B[CommandHandler]
    B --> C[AggregateRoot]
    C --> D[EventBus]
    D --> E[QueryHandler]
    E --> F[(Read Model)]
```

The **command side** updates aggregates and emits events.
The **query side** responds to read requests with dedicated data models.

---

## 🧱 Example 4 — Using Ports and Adapters

```python
# inbound port
class RegisterUserUseCase(UseCase[RegisterUserInput, Result[User, Error]]):
    ...

# outbound port
class UserRepository(Repository[User]):
    ...

# infrastructure adapter
class SqlUserRepository(UserRepository):
    ...
```

---

## ✅ Summary

These examples show that **BuildingBlocks** does not dictate the architecture — it **enables composition** across many styles (Clean, Hexagonal, CQRS, SOA, etc.).
