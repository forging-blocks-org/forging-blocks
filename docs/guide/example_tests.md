# Example Tests
## Putting testing ideas into practice

This page shows larger, more realistic examples that build on the
concepts introduced in the [Testing](testing.md) guide.

The focus here is on **observable behavior**, not on testing the toolkit itself.

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
    result = parse_int(raw)

    if result.is_err:
        return result

    match result:
        case Ok(value):
            return reciprocal(value)
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

from forging_blocks.application import UseCase
from forging_blocks.foundation import Result, Err


@dataclass
class CreateTaskInput:
    title: str


class TaskRepository:
    def save(self, title: str) -> Result[int, str]:
        ...


class CreateTaskUseCase(UseCase):
    def execute(self, data: CreateTaskInput) -> Result[int, str]:
        ...


class CreateTaskService(CreateTaskUseCase):
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def execute(self, data: CreateTaskInput) -> Result[int, str]:
        if not data.title.strip():
            return Err("title required")

        return self._repo.save(data.title)
```

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


def test_create_task_when_valid_title_then_succeeds() -> None:
    repo = InMemoryTaskRepository()
    service = CreateTaskService(repo)

    result = service.execute(CreateTaskInput(title="Write docs"))

    assert result.is_ok
    assert len(repo.tasks) == 1


def test_create_task_when_duplicate_title_then_reuses_task() -> None:
    repo = InMemoryTaskRepository()
    service = CreateTaskService(repo)

    first = service.execute(CreateTaskInput(title="Write docs"))
    second = service.execute(CreateTaskInput(title="Write docs"))

    assert first.is_ok
    assert second.is_ok
    assert len(repo.tasks) == 1


def test_create_task_when_missing_title_then_fails() -> None:
    repo = InMemoryTaskRepository()
    service = CreateTaskService(repo)

    result = service.execute(CreateTaskInput(title=" "))

    assert result.is_err
```

---

## Key takeaway

Tests should describe **what happened**, not **how the toolkit represents it**.

Use pattern matching when you need data.
Otherwise, assert success or failure and move on.
