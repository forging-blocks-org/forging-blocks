# Example Tests 🧩

Practical examples of how to test each layer using **BuildingBlocks**.

---

## 🧱 Domain Example — Entity Behavior

```python
from __future__ import annotations

from building_blocks.domain import Entity

class User(Entity):
    id: str
    name: str

    @classmethod
    def register(cls, id: str, name: str) -> User:
        return cls(id=id, name=name)

def test_user_identity_equality() -> None:
    user_a = User(id=1, name="Alice")
    user_b = User(id=1, name="Alice")
    assert user_a == user_b
```

---

## ⚙️ Application Example — Use Case

```python
from dataclasses import dataclass

from building_blocks.application import UseCase
from building_blocks.foundation import Error
from building_blocks.foundation import Ok, Err, Result

@dataclass(frozen=True)
class DivideNumbersRequest:
    dividend: int
    divisor: int

@dataclass(frozen=True)
class DivideNumbersResponse:
    quotient: int

class DivideNumbersError(Error):
    reason: str

class DivideNumbersResult = Result[DivideNumbersResponse, DivideNumbersError]

class DivideNumbersUseCase(UseCase[DivideNumbersRequest DivideNumbersResult]):
    def execute(self, request: DivideNumbersRequest) -> DivideNumbersResult:
        a, b = data
        if b == 0:
            return Err("division by zero")
        return Ok(a // b)

class DivideNumbersService(DivideNumbersUseCase):
    def execute(self, request: DivideNumbersRequest) -> DivideNumbersResult:
        a, b = data
        if b == 0:
            return Err(DivideNumbersError("division by zero"))
        return Ok(DivideNumbersResponse(a // b))

def test_divide_numbers_use_case_success() -> None:
    use_case = DivideNumbers()
    result = use_case.execute((10, 2))
    assert result.is_ok()
    assert result.value.quotient == 5
```

---

## 🧩 Infrastructure Example — Repository Adapter

```python
from building_blocks.application import Repository
from building_blocks.domain import Entity

class User(Entity):
    id: int
    name: str

class InMemoryUserRepository(Repository[User]):
    def __init__(self) -> None:
        self._data: dict[int, User] = {}

    def add(self, user: User) -> None:
        self._data[user.id] = user

    def get(self, user_id: int) -> User | None:
        return self._data.get(user_id)

def test_in_memory_user_repository() -> None:
    repo = InMemoryUserRepository()
    user = User(id=1, name="Alice")
    repo.add(user)
    assert repo.get(1) == user
```

---

## ✅ Summary

Each layer can be tested independently:

- Domain: pure business logic
- Application: behavior via ports
- Infrastructure: technical correctness

Testing with BuildingBlocks reinforces **clean boundaries** and **explicit contracts**.
