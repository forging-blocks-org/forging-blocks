# 🧪 Example Tests

This page contains a few self-contained test examples that show how ForgingBlocks can be used in practice. They are illustrative, not prescriptive — adapt them to your own testing style and framework.

All examples use `pytest`, but you can translate them to `unittest` or any other tool.

---

## 1. Testing Result Composition

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
    first = parse_int(raw)
    if isinstance(first, Err):
        return first
    return reciprocal(first.ok)
```

Tests:

```python
from forging_blocks.foundation import Ok, Err
from your_module import parse_reciprocal

def test_parse_reciprocal_when_valid_number_then_returns_ok() -> None:
    result = parse_reciprocal("4")
    assert isinstance(result, Ok)
    assert result.ok == 0.25

def test_parse_reciprocal_when_invalid_number_then_returns_err() -> None:
    result = parse_reciprocal("foo")
    assert isinstance(result, Err)
    assert "invalid integer" in result.err

def test_parse_reciprocal_when_zero_then_returns_err() -> None:
    result = parse_reciprocal("0")
    assert isinstance(result, Err)
    assert "division by zero" in result.err
```

---

## 2. Testing a Simple Use Case

```python
from dataclasses import dataclass
from forging_blocks.foundation import Result, Ok, Err

@dataclass
class CreateTaskInput:
    title: str

class TaskRepository:
    def add(self, title: str) -> Result[int, str]:
        ...

class CreateTask:
    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def execute(self, data: CreateTaskInput) -> Result[int, str]:
        if not data.title.strip():
            return Err("title required")
        return self._repo.add(data.title)
```

A fake repository for tests:

```python
class InMemoryTaskRepository:
    def __init__(self) -> None:
        self.tasks: dict[int, str] = {}
        self._next_id = 1
        self.should_fail: bool = False

    def add(self, title: str):
        if self.should_fail:
            return Err("database down")
        task_id = self._next_id
        self._next_id += 1
        self.tasks[task_id] = title
        return Ok(task_id)
```

Tests:

```python
from forging_blocks.foundation import Ok, Err
from your_module import CreateTask, CreateTaskInput, InMemoryTaskRepository

def test_create_task_when_valid_title_then_persists_and_returns_id() -> None:
    repo = InMemoryTaskRepository()
    use_case = CreateTask(repo)

    result = use_case.execute(CreateTaskInput(title="Write docs"))

    assert isinstance(result, Ok)
    assert result.ok in repo.tasks
    assert repo.tasks[result.ok] == "Write docs"

def test_create_task_when_missing_title_then_returns_err() -> None:
    repo = InMemoryTaskRepository()
    use_case = CreateTask(repo)

    result = use_case.execute(CreateTaskInput(title="  "))

    assert isinstance(result, Err)
    assert "title required" in result.err

def test_create_task_when_repo_fails_then_propagates_err() -> None:
    repo = InMemoryTaskRepository()
    repo.should_fail = True
    use_case = CreateTask(repo)

    result = use_case.execute(CreateTaskInput(title="Write tests"))

    assert isinstance(result, Err)
    assert "database down" in result.err
```

These examples show how ForgingBlocks can fit into ordinary testing practices without requiring a specific structure.
