# Example Tests
## Putting testing ideas into practice

This page shows larger, more realistic examples that build on the
concepts introduced in the [Testing](testing.md) guide.

---
## Quick summary

This page shows **larger, realistic test examples** building on concepts from the [Testing](testing.md) guide. The focus is on **observable behavior** — testing your code, not the toolkit.

Examples:
1. **Composing behavior with Result** — Chaining `Result`-returning functions, testing success/error paths with pattern matching
2. **Testing a simple use case** — Using a fake repository to test application-layer behavior without real infrastructure

Key takeaway: Tests should describe **what happened**, not how the toolkit represents it. Use pattern matching when you need data; otherwise assert success/failure and move on.

---

## 1. Composing behavior with Result

```python
from forging_blocks.foundation import Result, Ok, Err


def parse_int(value: str) -> Result[int, str]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"invalid integer: {value!r}")


def reciprocal(value: int) -> Result[float, str]:
    if value == 0:
        return Err("division by zero")
    return Ok(1 / value)


def parse_reciprocal(raw: str) -> Result[float, str]:
    return parse_int(raw).flat_map(reciprocal)
```

### Tests

```python
from your_module import parse_reciprocal


def test_parse_reciprocal_when_valid_input_then_succeeds() -> None:
    result = parse_reciprocal("4")

    assert result.is_ok


def test_parse_reciprocal_when_invalid_input_then_fails() -> None:
    result = parse_reciprocal("foo")

    assert result.is_err


def test_parse_reciprocal_when_zero_then_fails() -> None:
    result = parse_reciprocal("0")

    assert result.is_err
```

---

## 2. Testing a simple use case

```python
from dataclasses import dataclass

from forging_blocks.application import ApplicationServicePort
from forging_blocks.foundation import Result, Err


@dataclass
class CreateTaskInput:
    title: str


class TaskRepository:
    def save(self, title: str) -> Result[int, str]:
        ...


class CreateTaskUseCase(ApplicationServicePort[CreateTaskInput, Result[int, str]]):
    async def execute(self, request: CreateTaskInput) -> Result[int, str]:
        ...


class CreateTaskService(CreateTaskUseCase):
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    async def execute(self, request: CreateTaskInput) -> Result[int, str]:
        if not request.title.strip():
            return Err("title required")

        return self._repo.save(request.title)
```

!!! note "Generic type parameters are required"
    Port classes like `ApplicationServicePort` have **no defaults** on their
    generic type parameters. Inheriting as `ApplicationServicePort[Input, Output]`
    is mandatory — omitting the type arguments will trigger pyright errors.

### Fake repository

```python
from forging_blocks.foundation import Result, Ok


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self.tasks: dict[int, str] = {}
        self._next_id = 1

    def save(self, title: str) -> Result[int, str]:
        for task_id, existing in self.tasks.items():
            if existing == title:
                return Ok(task_id)

        task_id = self._next_id
        self._next_id += 1
        self.tasks[task_id] = title
        return Ok(task_id)
```

### Tests

```python
from your_module import CreateTaskService, CreateTaskInput, InMemoryTaskRepository


async def test_create_task_when_valid_title_then_succeeds() -> None:
    repo = InMemoryTaskRepository()
    service = CreateTaskService(repo)

    result = await service.execute(CreateTaskInput(title="Write docs"))

    assert result.is_ok
    assert len(repo.tasks) == 1


async def test_create_task_when_duplicate_title_then_reuses_task() -> None:
    repo = InMemoryTaskRepository()
    service = CreateTaskService(repo)

    first = await service.execute(CreateTaskInput(title="Write docs"))
    second = await service.execute(CreateTaskInput(title="Write docs"))

    assert first.is_ok
    assert second.is_ok
    assert len(repo.tasks) == 1


async def test_create_task_when_missing_title_then_fails() -> None:
    repo = InMemoryTaskRepository()
    service = CreateTaskService(repo)

    result = await service.execute(CreateTaskInput(title=" "))

    assert result.is_err
```

---

## Key takeaway

Tests should describe **what happened**, not **how the toolkit represents it**.

Use pattern matching when you need data.
Otherwise, assert success or failure and move on.
