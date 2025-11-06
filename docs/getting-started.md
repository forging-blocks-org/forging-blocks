# Architecture Guide

`building_blocks` embodies the best practices of **Clean Architecture** and **Hexagonal Architecture (Ports & Adapters)**, empowering you to build robust, scalable, and testable applications that are independent of frameworks, databases, or delivery channels.

---

## 🧭 Core Principles

- **Separation of Concerns:** Each layer has a clear, focused responsibility.
- **Dependency Rule:** All dependencies point inward—domain is the core and never knows about application, infrastructure, or presentation.
- **Framework Agnostic:** Core logic is independent of frameworks (FastAPI, Django, etc).
- **Port & Adapter Pattern:** Contracts (ports/interfaces) are defined in the core; implementations (adapters) live in infrastructure or application.

---

## 🏗️ The Layers

### 1. **Domain Layer** (Pure Core Business)

- **What:** Pure business logic—Entities, Value Objects, Aggregates, Domain Services, Domain Events.
- **How:**
  - Use `building_blocks.domain.Entity`, `AggregateRoot` for identity and event tracking.
  - No framework, DB, or technical logic here.

#### **Domain Ports**

Domain ports are **Abstract Base Classes (ABCs)** defining contracts for dependencies and pluggable domain logic.
They are split into:

#### 🔹 **Outbound Domain Ports**

- **What:** Interfaces for dependencies the domain needs (but doesn't implement), such as persistence, messaging, clocks, etc.
- **Where:** `domain/ports/outbound/`
- **Examples:**
  - **Repository Ports:** Persist and retrieve AggregateRoots.
  - **Event Publisher Ports:** Publish domain events.
    - These are typically outbound ports defined in the **domain** layer if publishing events is a core domain requirement, or in the **application** layer if event publication is an application-level orchestration concern.
  - **Clock Ports:** Access system time.
- **Typical Example:**

  ```python
  # domain/ports/outbound/async_repository.py
  from abc import ABC, abstractmethod
  from typing import Generic, TypeVar

  TAggregateRoot = TypeVar("TAggregateRoot")
  TId = TypeVar("TId")

  class AsyncRepository(ABC, Generic[TAggregateRoot, TId]):
      """
      Generic async repository interface for aggregate roots.

      Example:
          class OrderRepository(AsyncRepository[Order, UUID]):
              async def find_by_id(self, order_id: UUID) -> Order | None: ...
              async def save(self, order: Order) -> None: ...
              async def delete(self, order: Order) -> None: ...
              async def find_all(self) -> list[Order]: ...
              async def find_by_customer_id(self, customer_id: str) -> list[Order]: ...
      """
      @abstractmethod
      async def find_by_id(self, aggregate_id: TId) -> TAggregateRoot | None: ...
      @abstractmethod
      async def save(self, aggregate: TAggregateRoot) -> None: ...
      @abstractmethod
      async def delete(self, aggregate: TAggregateRoot) -> None: ...
      @abstractmethod
      async def find_all(self) -> list[TAggregateRoot]: ...
  ```

  ```python
  # domain/ports/outbound/event_publisher.py (if event publishing is domain concern)
  from abc import ABC, abstractmethod
  from typing import Any

  class EventPublisher(ABC):
      """
      Outbound port for publishing domain events.
      """
      @abstractmethod
      async def publish(self, event: Any) -> None:
          """Publish a domain event."""
  ```

  > **Note:** If event publishing is more of an application-level concern, define `EventPublisher` in `application/ports/outbound/`.

#### 🔹 **Inbound Domain Ports**

- **What:** Interfaces for pluggable domain logic/policies that are injected into the domain (e.g., strategies, business rules).
- **Where:** `domain/ports/inbound/`
- **Examples:**
  - **Policy Ports:** Discount calculation, authorization, shipping calculation, etc.
  - **Specification/Strategy:** Custom validation, calculation, or selection strategies.
- **Typical Example:**

  ```python
  # domain/ports/inbound/discount_policy.py
  from abc import ABC, abstractmethod

  class DiscountPolicy(ABC):
      """
      Inbound domain port for calculating discounts.
      """
      @abstractmethod
      def calculate_discount(self, customer_id: str, total: float) -> float:
          """Return the discount amount for a given customer and order total."""
  ```

---

### 2. **Application Layer** (Use Cases & Orchestration)

- **What:** Orchestrates business workflows and defines how external requests enter the system.
- **How:**
  - **UseCase Ports:** Abstract base classes (interfaces) for each use case (inbound application ports).
    - **Location:** `application/ports/inbound/use_case.py`
    - **Every UseCase must be defined here.**
  - **Async Support:** For IO-bound operations, use `AsyncUseCase` as your inbound port:

    ```python
    # application/ports/inbound/use_case.py
    from abc import ABC, abstractmethod
    from typing import Generic, TypeVar

    TRequest = TypeVar("TRequest")
    TResponse = TypeVar("TResponse")

    class AsyncUseCase(ABC, Generic[TRequest, TResponse]):
        """
        Application inbound port for asynchronous use cases.

        Use cases orchestrate interactions between domain services, repositories,
        and other components to fulfill application-specific operations.

        This base class is for asynchronous use cases—implementations should define
        'async def execute(self, request: TRequest) -> TResponse'.
        """

        @abstractmethod
        async def execute(self, request: TRequest) -> TResponse:
            """
            Asynchronous execution of the use case with the provided request.

            This method should be implemented by concrete use case classes to
            perform the necessary operations and return a response.

            Args:
                request: The request object containing input data for the use case.
            Returns:
                TResponse: The response object containing the result of the use case
                execution.
            Raises:
                Exception: Any exceptions that occur during execution should be
                handled appropriately, such as validation errors or service failures.
            """
    ```
  - **Application Services:** Concrete classes implement these ports.
  - **Request/Response:** All requests/responses are `@dataclass(frozen=True)` for immutability and clarity.
  - **Implements Domain Inbound Ports:** Application layer can implement inbound domain ports (e.g., `LoyaltyDiscountPolicy`) if logic is purely business or composed from domain/application services.
  - **Application Outbound Ports:** For cross-cutting concerns (e.g., notification, external systems), define ports such as `Notifier`, `EventPublisher` in `application/ports/outbound/` if they are not domain requirements.

#### Example: Application Implementation of a Domain Inbound Port

```python
# application/services/loyalty_discount_policy.py
from application.ports.inbound.discount_policy import DiscountPolicy

class LoyaltyDiscountPolicy(DiscountPolicy):
    """
    Loyalty-based discount policy implementation.

    - VIP customers get 20% off.
    - All others get 5%.
    """
    def calculate_discount(self, customer_id: str, total: float) -> float:
        if customer_id.startswith("VIP"):
            return total * 0.20
        return total * 0.05
```

---

### 3. **Infrastructure Layer** (Adapters & Implementations)

- **What:** Implements all outbound ports—repositories, messaging, storage, and more.
- **Directory Structure:**
  - **Persistence Adapters:**
    - `infrastructure/persistence/models/`: ORM, ODM, or other persistence models.
      - **Models must always have `created_at` and `updated_at` fields:** These should be automatically managed (e.g., SQLAlchemy defaults, Pydantic, or framework support).
      - Models are responsible for mapping to/from domain objects when possible.
    - `infrastructure/persistence/repositories/`: Implements the domain outbound repository ports (e.g., `AsyncRepository`) with concrete classes.
      - **Each adapter here must explicitly implement the corresponding domain outbound port (interface) defined in `domain/ports/outbound/`.**
      - Mapping between persistence models and AggregateRoots can be handled in repository methods or helper functions.
  - **Messaging Adapters:** `infrastructure/messaging/`
  - **Other Adapters:** External APIs, notifications, caching, etc.

- **Rule:** Infrastructure only depends on interfaces from application/domain, never the other way around.

#### Example: Repository Adapter

```python
# infrastructure/persistence/repositories/order_repository.py
from application.ports.outbound.async_repository import AsyncRepository
from domain.aggregates.order import Order

class SQLAlchemyOrderRepository(AsyncRepository[Order, UUID]):
    def __init__(self, session):
        self.session = session
    async def find_by_id(self, order_id):
        # ORM logic, mapping from OrderModel to Order (AggregateRoot)
        ...
    async def save(self, order: Order) -> None:
        # ORM logic, mapping from Order (AggregateRoot) to OrderModel
        ...
    async def delete(self, order: Order) -> None:
        ...
    async def find_all(self) -> list[Order]:
        ...
```
*Note: The adapter's implementation must be explicit about which domain outbound port it implements.*

---

### 4. **Presentation Layer** (User Interfaces & Entry Points)

- **What:** REST APIs, CLI, GUIs, GRPC, etc.
- **How:** Calls application layer use cases via their ports (never accessing domain or infra directly).

```python
@router.post("/orders")
async def create_order(req: CreateOrderRequest, use_case: CreateOrderUseCase = Depends()):
    return await use_case.execute(req)
```

---

## 🧩 Layered Visual Overview

```plaintext
+-------------------- Presentation Layer ----------------------+
|  REST API / CLI / gRPC / UI                                 |
|     |                                                       |
|     | calls                                                 |
v     v                                                       |
+---------------- Application Layer ---------------------------+
|  [Use Case Inbound Port]                                    |
|    - e.g., AsyncUseCase (application/ports/inbound/)        |
|    | implements                                             |
|    v                                                        |
|  [Application Service]                                      |
|    - e.g., CreateOrderService                               |
|    | calls                                                  |
|    v                                                        |
|  [Domain Inbound Port] (policy/strategy)                    |
|    - e.g., DiscountPolicy (domain/ports/inbound/)           |
|    |                                                        |
|    v                                                        |
|  [Domain Service or Aggregate]                              |
|    - e.g., Cart, Order, etc.                                |
|    | uses                                                   |
|    v                                                        |
|  [Domain Outbound Port]                                     |
|    - e.g., AsyncRepository (domain/ports/outbound/)         |
+-------------------------------------------------------------+
      | implements
      v
+------------------ Infrastructure Layer ----------------------+
| [Repository Adapter]                                         |
|   - e.g., SQLAlchemyOrderRepository (infra/...)              |
|   - implements domain outbound port                          |
| [Messaging Adapter, etc.]                                    |
|   - EventPublisher, Notifier, etc.                           |
+--------------------------------------------------------------+
```

---

## 🚦 Port & Adapter Details

- **Domain Outbound Ports (Repositories, EventPublisher, etc):**
  - *Define* in `domain/ports/outbound/` (e.g., `AsyncRepository`, `EventPublisher`)
  - *Implement* in `infrastructure/persistence/repositories/` (for repositories) or other infra folders.
  - **Repositories persist and retrieve AggregateRoots.**
  - **Persistence models** are in `infrastructure/persistence/models/` and must have `created_at`/`updated_at` fields auto-managed.
  - Mapping from AggregateRoot <--> persistence model is the repository’s responsibility.

- **Domain Inbound Ports (Policies/Strategies):**
  - *Define* as ABCs in `domain/ports/inbound/` (e.g., `DiscountPolicy`, `ShippingCostCalculator`)
  - *Implement* in `application/services/` (for logic that is pure or business-specific), or in `infrastructure/` if it needs external systems.

- **Application Inbound Ports (UseCases):**
  - *Define* in `application/ports/inbound/use_case.py` (e.g., `AsyncUseCase`)
  - *Implement* in `application/services/` (concrete application services)
  - **All requests and responses should be immutable dataclasses** (`@dataclass(frozen=True)`).

- **Application Outbound Ports:** (if the concern is not strictly domain, e.g., notifications)
  - *Define* in `application/ports/outbound/`.
  - *Implement* in infrastructure adapters.

- **Adapters:**
  - Messaging adapters live in `infrastructure/messaging/`
  - Persistence adapters live in `infrastructure/persistence/repositories/`
  - Other infra (e.g., HTTP, file, cache) in their own subfolders.

---

## 🏆 Why This Matters

- **Testability:** Business rules can be tested without DBs or frameworks.
- **Flexibility:** Swap DBs, frameworks, or messaging platforms with zero changes to core logic.
- **Maintainability:** Modular code, clear contracts, and explicit boundaries.
- **Async First:** Native support for async use cases and repositories enables scalable, modern Python apps.

---

## 🔑 Key Takeaways

- **All dependencies point inward (toward domain).**
- **Domain is pure and unaware of frameworks/infra.**
- **Domain ports are clearly separated into inbound (`domain/ports/inbound/`) and outbound (`domain/ports/outbound/`).**
- **Repositories are defined as outbound ports in the domain and persist AggregateRoots.**
- **Persistence adapters implement repository ports and live in `infrastructure/persistence/repositories/`, always explicitly implementing the outbound port.**
- **Persistence models (with auto-managed `created_at`/`updated_at`) live in `infrastructure/persistence/models/`.**
- **Messaging adapters live in `infrastructure/messaging/`.**
- **Application inbound ports (UseCases) are defined in `application/ports/inbound/use_case.py`.**
- **Application outbound ports (e.g., Notifier) are defined in `application/ports/outbound/` if not a core domain concern.**
- **Requests and responses for use cases are frozen dataclasses (immutable and explicit).**
- **Async ports like `AsyncUseCase` and `AsyncRepository` are first-class for modern Python.**
- **Adapters implement interfaces defined in the core.**
- **Application layer can implement inbound domain ports for strategies/policies if logic is business-focused and pure.**
- **You can swap infra/frameworks with zero changes to business rules.**

---

*Build for today, evolve for tomorrow. Future-proof your business logic with Building Blocks!*
