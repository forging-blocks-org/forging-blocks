# Application Block

The **application block** orchestrates business workflows, coordinates domain logic, and manages cross-cutting concerns such as transactions and notifications.
It acts as a bridge between the domain block (business logic) and the outside world (presentation, infrastructure, external services).

---

## Directory Structure

```
application/
├── ports/
│   ├── inbound/
│   │   └── application_service_port.py   # Abstract base for use cases/handlers
│   └── outbound/
│       ├── event_publisher.py  # Contract for publishing integration events
│       ├── notifier.py         # Contract for sending notifications
│       └── unit_of_work.py     # Contract for transaction management
└── services/                   # Implementations of application use cases
```

---

## Core Concepts

### 1. **Application Inbound Ports**
- **Purpose:** Orchestrate business workflows by coordinating Domain logic and Infrastructure through ports.
- **What goes here:** Protocol interfaces for commands, queries, and use cases.
- **Example:** ``UseCasePort`` in ``ports/inbound/use_case_port.py``.

### 2. **Application Services**
- **Purpose:** Implement the business workflows and coordinate domain objects, repositories, and outbound ports.
- **What goes here:** Concrete classes that implement inbound port interfaces and orchestrate use cases.
- **Example:** `services/CreateUserService` (you provide your own implementations).

### 3. **Application Outbound Ports**
- **Purpose:** Abstract external systems or cross-cutting concerns that the application interacts with.
- **What goes here:** Interfaces for things like event publishing, notifications, and transaction management.
- **Examples:**
  - `event_publisher.py`: Publish integration/application events
  - `notifier.py`: Send notifications (email, SMS, etc.)
  - `unit_of_work.py`: Coordinate transactional boundaries for use cases

---

## How to Use

> **Best Practice:**
> Application services (use cases) should use DTOs (Data Transfer Objects) as their input and output types, not domain entities.
> This keeps your application blocks decoupled from domain and presentation concerns, and ensures a stable contract between blocks.

### 1. Define Use Case, Request, and Response (with type hints)

```python
from dataclasses import dataclass

from forging_blocks.application import UseCasePort


@dataclass(frozen=True)
class CreateUserRequest:
    email: str
    name: str


@dataclass(frozen=True)
class CreateUserResponse:
    user_id: str


class CreateUserUseCase(UseCasePort[CreateUserRequest, CreateUserResponse]):
    """Use case for creating a new user.

    Args:
        request: The CreateUserRequest DTO with input data.

    Returns:
        CreateUserResponse DTO with the result user_id.
    """

```
> `UseCasePort` is a type alias for `ApplicationServicePort`, an ABC that requires
> explicit inheritance. Use docstrings to document the intent of the execute method.

### 2. Implement the Use Case

```python
from forging_blocks.application import NotifierPort, RepositoryPort, UnitOfWorkPort


class CreateUserService(CreateUserUseCase):
    def __init__(
        self,
        user_repo: RepositoryPort,
        notifier: NotifierPort,
        uow: UnitOfWorkPort,
    ) -> None:
        self._user_repo = user_repo
        self._notifier = notifier
        self._uow = uow

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        async with self._uow:
            user = User(...)

            await self._user_repo.save(user)
            await self._notifier.notify(...)

            return CreateUserResponse(user_id=user.id)
```

---
## Why This Matters

- **Separation of Concerns:** Keeps business workflows free from technical details.
- **Testability:** Use cases can be tested by replacing outbound ports with mocks or fakes.
- **Flexibility:** Infrastructure can be swapped (e.g., different notification services) without changing application logic.
- **Explicit Boundaries:** Makes dependencies and orchestration visible and intentional.
- **Decoupling:** Using DTOs for input/output prevents leaking domain details to the outside world.

---

## Extending the Application Layer

- **Add new inbound ports** for new use cases.
- **Add new outbound ports** for new integrations (e.g., background jobs, analytics, etc.).
- **Implement services** for each use case, orchestrating domain and infrastructure as needed.
