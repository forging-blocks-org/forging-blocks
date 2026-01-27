# Testing

## Overview

ForgingBlocks encourages designs where behavior and outcomes are explicit.
This makes your code easier to test without relying on internal details.

This guide covers both **testing principles** and the **test structure** used in this project.

---

## Test Structure & Categories

This project uses a **3-tier testing architecture** with clear separation of concerns:

### 🎯 **Unit Tests** (`@pytest.mark.unit`)
Fast, isolated tests that verify individual components using mocks.

```bash
poetry run poe test:unit   # ~1 second
```

**What's included:**
- Domain logic (entities, value objects, aggregates)
- Foundation/framework components
- Application services (with mocked dependencies)
- Infrastructure components (with mocked external systems)
- Presentation layer components (with mocked dependencies)

**Example:**
```python
@pytest.mark.unit
class TestPrepareReleaseService:
    def test_execute_when_tag_exists_then_fails(
        self,
        service: PrepareReleaseService,
        version_control_mock: Mock
    ) -> None:
        # Arrange: Mock the external dependency
        version_control_mock.tag_exists.return_value = True

        # Act: Test the business logic
        result = await service.execute(input_data)

        # Assert: Verify behavior
        assert result.is_err()
```

### 🔧 **Integration Tests** (`@pytest.mark.integration`)
Tests that verify components work with real infrastructure in isolated environments.

```bash
poetry run poe test:integration   # ~2-3 seconds
```

**What's included:**
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

### 🛡️ **End-to-End Tests** (`@pytest.mark.e2e`)
Complete workflow tests that exercise the entire system.

```bash
poetry run poe test:e2e   # All currently skipped
```

**What's included:**
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

### 🚀 **Running Tests**

```bash
# Primary Commands (for daily development)
poetry run poe test              # Run all stable tests (unit + integration)
poetry run poe test:unit         # Run unit tests only (fast feedback)
poetry run poe test:integration  # Run integration tests only

# Extended Commands (for comprehensive testing)
poetry run poe test:all          # Run ALL tests including those needing setup
poetry run poe test:stable       # Run stable tests (excludes GitHub CLI)
poetry run poe test:e2e          # Run end-to-end tests only
poetry run poe test:debug        # Debug mode with verbose output
```

**Understanding Test Results:**
- `poetry run poe test` runs **stable** tests that should always pass (unit + integration)
- `poetry run poe test:all` runs **ALL** tests including those requiring special setup
- Some tests are **conditionally skipped** based on environment configuration
- Skipped tests are still valuable as documentation of system capabilities

### 📊 **Test Results Summary**

| Test Type | Count | Coverage | Speed | When to Use |
|-----------|-------|----------|-------|-------------|
| Unit | 304 | 95.46% | ⚡ Fast (0.96s) | Development, TDD, CI |
| Integration | 60 + 1 skipped | 67.74% | 🔧 Moderate (2.29s) | Integration verification |
| E2E | 4 skipped | N/A | 🛡️ Protected (skipped) | Documentation, manual testing |
| **All Stable** | **364 passed + 1 skipped** | **98.69%** | ✅ **Complete (2.84s)** | **CI, Release** |

**Note:** Some tests are conditionally skipped based on environment:
- 1 GitHub CLI integration test (requires `RUN_GITHUB_CLI_TESTS=1`)
- 4 End-to-end workflow tests (require `RUN_E2E_TESTS=1` and complex setup)

Use `poetry run poe test:all` to attempt running all tests including those requiring setup.

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

### 4. Fakes vs mocks

Both approaches work well with Ports.

- **Fakes** emphasize state and behavior.
- **Mocks** emphasize interactions.

Choose the approach that makes the test's intent most obvious.

ForgingBlocks does not enforce a testing style — it encourages clarity.

---

## Testing Guidelines

### ✅ **Best Practices**

1. **Use appropriate test categories:**
   - Unit tests for business logic and isolated components
   - Integration tests for external system interactions
   - E2E tests for complete workflows (sparingly)

2. **Test intent, not implementation:**
   ```python
   # Good - tests behavior
   assert result.is_ok()

   # Avoid - tests implementation details
   assert isinstance(result, Ok)
   ```

3. **Use descriptive test names:**
   ```python
   def test_prepare_release_when_tag_exists_then_raises_error(self) -> None:
       # Test name tells the complete story
   ```

4. **Mock at the boundaries:**
   - Mock external dependencies (APIs, databases, file systems)
   - Don't mock your own domain objects

5. **Keep tests focused:**
   - One test should verify one behavior
   - Use clear arrange/act/assert structure

### ⚠️ **Common Pitfalls**

1. **Over-mocking:** Don't mock everything - test real object interactions when safe
2. **Testing implementation:** Focus on behavior, not internal structure
3. **Brittle tests:** Avoid testing exact mock call sequences unless critical
4. **Slow feedback:** Run unit tests frequently, integration tests less often

---

## Environment Setup

The test environment automatically handles:

- **Isolated git repositories** for integration tests
- **Temporary directories** for file system tests
- **Mock external services** for unit tests
- **Consistent branch naming** across CI/local environments

Test fixtures provide clean, isolated environments for each test run.
