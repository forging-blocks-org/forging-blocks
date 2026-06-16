# Testing

## Overview

ForgingBlocks encourages designs where behavior and outcomes are explicit.
This makes your code easier to test without relying on internal details.

---
## Quick summary

This guide covers **testing principles** and the **3-tier test structure** used in ForgingBlocks. ForgingBlocks designs make behavior explicit, making code easier to test without relying on internal details.

Test tiers:
- **Unit** (`@pytest.mark.unit`) — Fast, isolated tests for pure business logic (Domain, Value Objects, Aggregates). Mocks/fakes OK for owned contracts.
- **Integration** (`@pytest.mark.integration`) — Real/simulated external dependencies (repositories, message buses, APIs). Use fixtures/fakes, **not mocks**.
- **E2E** (`@pytest.mark.e2e`) — Complete workflows from entry points (CLI, HTTP). Conditionally skipped; document full system behavior.

Key principles:
- **Test intent first** — Focus on behavior, not `Result` representation
- **Use fakes for Ports** — Replace Port dependencies with fakes to verify behavior without infrastructure
- **Don't mock what you don't own** — Wrap external systems behind Ports, use fakes in tests
- **Pattern matching supports, doesn't dominate** — Use when returned value matters to intent

Commands: `poe test:unit` (fast), `poe test` (all), `poe test:e2e` (conditional).

---

This project uses a **3-tier testing architecture** with clear separation of concerns:

### **Unit Tests** (`@pytest.mark.unit`)
Fast, isolated tests that verify pure business logic and components you own.

```bash
poetry run poe test:unit   # ~1 second
```

**What's included:**
- Domain logic (entities, value objects, aggregates)
- Foundation/framework components
- Application services (pure coordination logic, not infrastructure adapters)

**Example:**
```python
@pytest.mark.unit
class TestPrepareReleaseService:
    def test_execute_when_tag_exists_then_fails(
        self,
        service: PrepareReleaseService,
        fake_version_control: FakeVersionControl,
    ) -> None:
        # Arrange: Use a fake that simulates real behavior
        fake_version_control.add_existing_tag(TagName("v1.0.0"))

        # Act: Test the business logic
        input_data = PrepareReleaseInput(level=ReleaseLevel.PATCH)
        result = await service.execute(input_data)

        # Assert: Verify behavior
        assert result.is_err
```

### **Integration Tests** (`@pytest.mark.integration`)
Tests that verify components against real or simulated external dependencies.

```bash
poetry run poe test:integration   # ~2-3 seconds
```

**What's included:**
- Infrastructure adapters (repositories, message buses, external APIs)
- Git operations (using real git in temporary repositories)
- Process/subprocess execution
- File system operations
- External CLI tools (when safe)

**Example:**
```python
@pytest.mark.integration
class TestGitVersionControlIntegration:
    def test_branch_lifecycle_when_created_then_exists_and_deleted(
        self,
        git_repo: GitTestRepository,  # Real git repo fixture
    ) -> None:
        # Test with real git operations
        version_control = GitVersionControl(SubprocessCommandRunner())

        version_control.create_branch(ReleaseBranchName("release/v1.2.0"))
        assert version_control.branch_exists(ReleaseBranchName("release/v1.2.0"))
```

### **End-to-End Tests** (`@pytest.mark.e2e`)
Complete workflow tests that exercise the entire system from entry points.

```bash
poetry run poe test:e2e   # All currently skipped
```

**What's included:**
- Presentation layer entry points (CLI, HTTP handlers)
- Full CLI workflows
- Complete release processes
- Multi-component integration scenarios

**Note:** E2E tests are **conditionally skipped** in normal runs since they require complex setup (real GitHub tokens, complete project structure, etc.). They serve as documentation for full system behavior.

```python
@pytest.mark.e2e
class TestMain:
    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup"
    )
    async def test_main_when_called_then_creates_release(
        self, git_repo: GitTestRepository
    ) -> None:
        # Full workflow test - only run in special environments
        ...
```

### **Running Tests**

```bash
# Primary Commands (for daily development)
poetry run poe test              # Run ALL tests (recommended default)
poetry run poe test:unit         # Run unit tests only (fast feedback)
poetry run poe test:integration  # Run integration tests only

# Extended Commands (for comprehensive testing)
poetry run poe test:e2e          # Run end-to-end tests only
poetry run poe test:debug        # Debug mode with verbose output
```

**Understanding Test Results:**
- `poetry run poe test` runs **ALL** tests including E2E (complete confidence)
- Some tests are **conditionally skipped** based on environment configuration
- Skipped tests are still valuable as documentation of system capabilities

### **Test Results Summary**

| Test Type | Count | Coverage | Speed | When to Use |
| Test Type | Count | Coverage | Speed | When to Use |
|-----------|-------|----------|-------|-------------|
| Unit | 360 | — | Fast | Development, TDD, CI |
| Integration | 84 | — | Moderate | Integration verification |
| E2E | 16 skipped | N/A | Protected (skipped) | Documentation, manual testing |
| **All** | **460 passed, 17 skipped** | **98.51%** | **Complete** | **CI, Release** |
**Note:** Some tests are conditionally skipped based on environment:
- GitHub CLI integration tests (require `RUN_GITHUB_CLI_TESTS=1`)
- End-to-end workflow tests (require `RUN_E2E_TESTS=1` and complex setup)

Use `poetry run poe test` to run all tests including those requiring setup (with environment variables).

---

## Testing Principles

This project focuses on **what to test and why**, not on any specific testing framework.
You can use `pytest`, `unittest`, or any other tool you prefer.

### 1. Testing pure functions

Pure functions are the easiest place to start.
When a function returns a `Result`, success and failure are part of the contract.

```python
from forging_blocks.foundation import Result, Ok, Err


def is_even(value: int) -> Result[bool, str]:
    if value < 0:
        return Err("negative value")
    return Ok(value % 2 == 0)
```

#### Example tests

Tests should focus on **intent first**, not on how the `Result` is represented.

```python
from your_module import is_even


def test_is_even_when_value_is_even_then_succeeds() -> None:
    result = is_even(4)

    assert result.is_ok


def test_is_even_when_value_is_odd_then_succeeds() -> None:
    result = is_even(3)

    assert result.is_ok


def test_is_even_when_value_is_negative_then_fails() -> None:
    result = is_even(-1)

    assert result.is_err
```

Only inspect returned values when they matter to the test's intent:

```python
from forging_blocks.foundation import Ok


def test_is_even_returns_false_for_odd_numbers() -> None:
    result = is_even(3)

    assert result.is_ok

    match result:
        case Ok(value):
            assert value is False
```

---

### 2. Testing code that depends on a Port (using fakes)

When code depends on a **Port**, you can replace that dependency in tests.
This lets you verify behavior without involving infrastructure.

```python
from forging_blocks.foundation import Result, Port


class IdGenerator(Port):
    def generate(self) -> Result[str, str]:
        ...
```

Business logic:

```python
def create_user_id(generator: IdGenerator) -> Result[str, str]:
    return generator.generate()
```

A simple fake implementation:

```python
from forging_blocks.foundation import Result, Ok, Err


class FakeIdGenerator:
    def __init__(self, ids: list[str]) -> None:
        self._ids = ids

    def generate(self) -> Result[str, str]:
        if not self._ids:
            return Err("no more ids")
        return Ok(self._ids.pop(0))
```

#### Example tests

```python
from your_module import create_user_id, FakeIdGenerator


def test_create_user_id_when_id_is_available_then_succeeds() -> None:
    generator = FakeIdGenerator(["id-1"])

    result = create_user_id(generator)

    assert result.is_ok


def test_create_user_id_when_no_ids_left_then_fails() -> None:
    generator = FakeIdGenerator([])

    result = create_user_id(generator)

    assert result.is_err
```

---

### 3. When to use pattern matching in tests

Pattern matching is useful when:
- the returned value is meaningful to the behavior
- you need to inspect error information
- multiple outcomes must be distinguished

It should **support the test**, not dominate it.

---

### 4. Mocks vs fakes

**Unit tests** can use **mocks** or **fakes** for owned contracts (Ports, interfaces you control). Either approach is fine as long as the test remains focused on behavior.

**Integration tests** should use **fixtures/fakes**, not mocks. Fixtures provide real or simulated infrastructure (e.g., temporary git repos, in-memory databases), while fakes simulate real behavior with captured input/output data.

**Don't mock what you don't own.** External systems (APIs, databases, file systems) should be wrapped behind a Port and replaced with a fake in tests.

ForgingBlocks encourages designing with Ports so that dependencies can be replaced with fakes in tests.

---

## Testing Guidelines

### **Best Practices**

1. **Use appropriate test categories:**
   - Unit tests for pure business logic you own
   - Integration tests for infrastructure adapters and external system interactions
   - E2E tests for presentation layer and complete workflows

2. **Test intent, not implementation:**
   ```python
   # Good - tests behavior
   assert result.is_ok

   # Avoid - tests implementation details
   assert isinstance(result, Ok)
   ```

3. **Use descriptive test names:**
   ```python
   def test_prepare_release_when_tag_exists_then_raises_error(self) -> None:
       # Test name tells the complete story
   ```

4. **Choose the right test level:**
   - Unit tests for pure business logic you own
   - Integration tests for infrastructure adapters and external system interactions
   - E2E tests for presentation layer and complete workflows
   - Don't mock what you don't own - use integration tests instead

5. **Keep tests focused:**
   - One test should verify one behavior
   - Use clear arrange/act/assert structure

### **Common Pitfalls**

1. **Unit-testing external integrations:** Infrastructure adapters and presentation should have integration/E2E tests, not unit tests with mocks
2. **Testing implementation:** Focus on behavior, not internal structure
3. **Brittle tests:** Avoid coupling tests to internal call sequences
4. **Slow feedback:** Run unit tests frequently, integration tests less often

---

## Environment Setup

The test environment automatically handles:

- **Isolated git repositories** for integration tests
- **Temporary directories** for file system tests
- **Fake external services** for integration tests
- **Consistent branch naming** across CI/local environments

Test fixtures provide clean, isolated environments for each test run.
