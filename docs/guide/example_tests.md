# Example Tests 🧩

**For developers using BuildingBlocks** this guide shows *how* to write tests for each layer.

It complements the conceptual [Testing Strategy](testing.md) page.

------------------------------------------------------------------------

## 🧱 Domain Example

Your tests should be written against your domain models to verify their behavior.

Entity methods represents domain logic and should be testedin any possible scenario that may arise.

``` python
from __future__ import annotations

from uuid import UUID

from building_blocks.domain import Entity

class User(Entity[UUID]):
    id: UUID
    name: str

    @classmethod
    def register(cls, id: int, name: str) -> User:
        return cls(id=id, name=name)

class TestUser:
    def test_register_when_called_2_times_same_names_but_different_id(self) -> None:
        # Arrange
        actual_name = "Alice"

        # Act
        created_user_a = User.register(name=actual_name)
        created_user_b = User.register(name=actual_name)

        # Assert
        expected_name = actual_name
        assert created_user_a.name == expected_name
        assert created_user_b.name == expected_name
        assert created_user_a.id != created_user_b.id
```

------------------------------------------------------------------------

## ⚙️ Application Example --- Use Case

``` python
from dataclasses import dataclass

from building_blocks.application import UseCase
from building_blocks.foundation import Error, Ok, Err, Result

@dataclass(frozen=True)
class DivideNumbersRequest:
    dividend: int
    divisor: int

@dataclass(frozen=True)
class DivideNumbersResponse:
    quotient: int

class DivideNumbersError(Error):
    reason: str

DivideNumbersResult = Result[DivideNumbersResponse, DivideNumbersError]

class DivideNumbersUseCase(UseCase[DivideNumbersRequest, DivideNumbersResult]):
    def execute(self, request: DivideNumbersRequest) -> DivideNumbersResult:
        a, b = request.dividend, request.divisor
        if b == 0:
            return Err(DivideNumbersError("division by zero"))
        return Ok(DivideNumbersResponse(a // b))

class TestDivideNumbersUseCase:
    def test_execute_when_divisor_is_zero_then_division_by_zero_error(self) -> None:
        dividend = 10
        divisor = 0
        request = DivideNumbersRequest(dividend, divisor)
        use_case = DivideNumbersUseCase()

        result = use_case.execute(request)

        expected_reason = "division by zero"
        expected_is_err = True
        assert result.is_err() == expected_is_err
        assert result.error.reason == expected_reason

    def test_execute_when_dividend_is_10_and_divisor_is_5_then_2(self) -> None:
        dividend = 10
        divisor = 5
        request = DivideNumbersRequest(dividend, divisor)
        use_case = DivideNumbersUseCase()

        result = use_case.execute(request)

        expected_quotient = 2
        assert result.is_ok()
        assert result.value.quotient == expected_quotient
```

------------------------------------------------------------------------

## 🧩 Infrastructure Example --- Repository Adapter

``` python
from building_blocks.application import Repository
from building_blocks.domain import Entity

class User(Entity):
    id: int
    name: str

class InMemoryUserRepository(Repository[User]):
    def __init__(self, data: dict[int, User]) -> None:
        self._data = data

    async def delete_by_id(self, user_id: int) -> None:
        self._data.pop(user_id, None)

    async def get_by_id(self, user_id: int) -> User | None:
        return self._data.get(user_id)

    async def list_all(self) -> list[User]:
        return list(self._data.values())

    async def save(self, user: User) -> None:
        self._data[user.id] = user

class TestInMemoryUserRepository:
    async def test_save_when_user_is_added_then_persist_data_source(self) -> None:
        data = {}
        user = User(id=1, name="Alice")
        repo = InMemoryUserRepository(data)

        await repo.save(user)

        persisted_user = data.get(1)
        assert retrieved_user == user
```

------------------------------------------------------------------------

> Continue exploring the [Testing Strategy](../guide/testing.md) page for the
> underlying principles behind these examples.
