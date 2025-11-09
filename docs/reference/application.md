# Application Package ⚙️

The **application** package defines how the system behaves — it orchestrates domain logic through **inbound** and **outbound ports**.

---

## 🧠 Purpose

This layer expresses *what the system does* — coordinating the domain with the outside world through explicit boundaries.

- **Inbound Ports** define *use cases* (entry points).  
- **Outbound Ports** define *dependencies* (repositories, message buses, etc.).

---

## 🧩 Structure

```
application/
├── ports/
│   ├── inbound/
│   │   ├── <action>_use_case.py
│   │   └── <action>_service.py
│   └── outbound/
│       ├── <entity>_repository.py
│       ├── event_publisher.py
│       ├── command_sender.py
│       ├── query_fetcher.py
│       └── message_bus.py
└── services/
```

---

## ⚙️ Inbound Ports

Inbound ports define *use cases* (application entry points).

Each `<action>_use_case.py` file defines a protocol for a specific action.

```python
from dataclasses import dataclass
from typing import Protocol
from building_blocks.application import UseCase
from building_blocks.foundation import Result

@dataclass(frozen=True)
class RegisterUserRequest:
    '''Request DTO containing data required to register a new user.'''
    username: str
    email: str
    password: str

@dataclass(frozen=True)
class RegisterUserResponse:
    '''Response DTO containing the ID of the created user.'''
    user_id: str

@dataclass(frozen=True)
class RegisterUserError:
    '''Represents a failure reason during user registration.'''
    reason: str

RegisterUserResult = Result[RegisterUserResponse, RegisterUserError]

class RegisterUserUseCase(UseCase[RegisterUserRequest, RegisterUserResult], Protocol):
    '''Inbound port representing the "Register User" use case.'''
    async def execute(self, request: RegisterUserRequest) -> RegisterUserResult:
        '''Executes the registration logic.
        Args:
            request: The user registration data.
        Returns:
            A `Result` containing the created user ID or an error.
        '''
        ...
```

---
