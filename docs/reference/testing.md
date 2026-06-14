# Testing Reference

This document provides a comprehensive reference for testing in the ForgingBlocks project.

## Quick Reference

### Test Commands

| Command | Purpose | Speed | Use Case |
|---------|---------|-------|----------|
| `poe test` | Run ALL tests | ~1.2s | CI, pre-commit, complete confidence |
| `poe test:unit` | Unit tests only | ~0.8s | Development, TDD, fast feedback |
| `poe test:integration` | Integration tests only | ~0.4s | Verify external integrations |
| `poe test:e2e` | E2E tests only | ~0.3s | Complete workflow validation |
| `poe test:debug` | Verbose output | Variable | Debugging failures |

### Test Categories

| Marker | Count | What to Test | Example |
|--------|-------|--------------|---------|
| `@pytest.mark.unit` | 360 | Business logic, domain objects, isolated components | Domain entities, value objects, application services with fakes |
| `@pytest.mark.integration` | 84 | External system interactions, real infrastructure | Git operations, file system, subprocess calls |
| `@pytest.mark.e2e` | 16 skipped | Complete workflows, full system behavior | CLI workflows, release processes |

## Test Architecture Principles

### 1. **Isolation Boundaries**

Tests are organized by isolation level, not by code structure:

- **Unit**: Pure business logic, no external dependencies. Mocks are acceptable for owned contracts.
- **Integration**: Infrastructure adapters and external system interactions. Use fixtures/fakes that simulate real behavior, not mocks.
- **E2E**: Presentation layer and complete workflows. Full system, real entry points.

### 2. **Fast Feedback Loops**

```bash
# Inner loop - rapid iteration
poe test:unit     # <1 second

# Validation loop - before commits
poe test          # <4 seconds - includes all tests (stable + conditional)
```

### 3. **Clear Test Intent**

Every test follows this structure:
```python
def test_when_condition_then_outcome(self) -> None:
    # Arrange: Set up test conditions

    # Act: Execute the behavior under test

    # Assert: Verify the expected outcome
```

## Detailed Guidelines

### Unit Tests (`@pytest.mark.unit`)

**Purpose:** Verify business logic and component behavior in isolation.

**Characteristics:**
- Fast execution (< 1 second total)
- No external dependencies
- Test pure business logic you own
- High coverage of business rules

**Example:**
```python
@pytest.mark.unit
class TestPrepareReleaseService:
    def test_execute_when_tag_exists_then_returns_error(
        self,
        service: PrepareReleaseService,
        fake_version_control: FakeVersionControl,
    ) -> None:
        # Arrange: Use a fake that simulates real behavior
        fake_version_control.add_existing_tag(TagName("v1.0.0"))
        input_data = PrepareReleaseInput(level=ReleaseLevel.PATCH)

        # Act
        result = await service.execute(input_data)

        # Assert
        assert result.is_err
        assert "already exists" in str(result.error)
```

**When to add unit tests:**
- New domain objects (entities, value objects)
- Business rules and validations
- Pure application coordination logic
- Foundation components

### Integration Tests (`@pytest.mark.integration`)

**Purpose:** Verify components work with real external systems in controlled environments.

**Characteristics:**
- Moderate execution time (~2-3 seconds total)
- Real external dependencies (git, filesystem, etc.)
- Isolated test environments (temporary directories, test repositories)
- Focus on boundary interactions

**Example:**
```python
@pytest.mark.integration
class TestGitVersionControlIntegration:
    def test_branch_lifecycle_when_created_then_exists_and_deleted(
        self,
        git_repo: GitTestRepository,
    ) -> None:
        # Arrange
        version_control = GitVersionControl(SubprocessCommandRunner())
        branch = ReleaseBranchName("release/v1.2.0")

        # Act & Assert
        assert not version_control.branch_exists(branch)

        version_control.create_branch(branch)
        assert version_control.branch_exists(branch)

        version_control.delete_local_branch(branch)
        assert not version_control.branch_exists(branch)
```

**When to add integration tests:**
- Infrastructure adapters (repositories, message buses, external APIs)
- External system interactions (git, GitHub API, file system)
- CLI tools and process execution
- Cross-boundary data flow

### End-to-End Tests (`@pytest.mark.e2e`)

**Purpose:** Document and verify complete system workflows.

**Characteristics:**
- Conditionally skipped based on environment configuration
- Require full system setup (GitHub tokens, poetry config, etc.)
- Test complete user workflows
- Serve as living documentation

**Example:**
```python
@pytest.mark.e2e
class TestReleaseWorkflow:
    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup"
    )
    def test_complete_release_workflow(self, git_repo: GitTestRepository) -> None:
        # This test documents the full release process
        # Only run when environment is configured
        ...
```

**When to add E2E tests:**
- Presentation layer entry points (CLI, HTTP handlers)
- Complete CLI workflows
- Full business processes
- Cross-system integration scenarios
- Documentation of system behavior

## Test Environment & Fixtures

### Git Test Repository

The `GitTestRepository` fixture provides isolated git repositories:

```python
def test_git_operation(git_repo: GitTestRepository) -> None:
    # Automatic cleanup, isolated from real repo
    git_repo.write_file("test.txt", "content")
    git_repo.commit("Add test file")
```

### Faking Strategy

**Don't mock what you don't own.** External systems should be wrapped behind a Port and replaced with a fake that simulates real behavior using captured input/output data.

**Use fakes for external dependencies:**

```python
class FakeVersionControl:
    """Simulates real version control behavior with captured data."""
    def __init__(self) -> None:
        self.tags: set[str] = set()
        self.branches: set[str] = set()

    def tag_exists(self, tag: TagName) -> bool:
        return tag.value in self.tags

    def create_tag(self, tag: TagName) -> None:
        self.tags.add(tag.value)

    def add_existing_tag(self, tag: TagName) -> None:
        self.tags.add(tag.value)
```

**Avoid mocking what you don't own:**

```python
# Don't mock external systems you don't own
# version_control_mock = create_autospec(VersionControl, instance=True)

# Don't fake your own domain objects - test them directly
# domain_entity_fake = FakeEntity()
```

## Common Patterns

### Result Testing

```python
# Test success/failure state
assert result.is_ok
assert result.is_err

# Extract values when needed
match result:
    case Ok(value):
        assert value.version == "1.2.3"
    case Err(error):
        assert "validation" in str(error)
```

### Async Testing

```python
@pytest.mark.asyncio
async def test_async_operation(self) -> None:
    result = await service.execute(input_data)
    assert result.is_ok
```

### Parametrized Tests

```python
@pytest.mark.parametrize("level,expected", [
    (ReleaseLevel.MAJOR, "2.0.0"),
    (ReleaseLevel.MINOR, "1.2.0"),
    (ReleaseLevel.PATCH, "1.1.1"),
])
def test_version_increment(level: ReleaseLevel, expected: str) -> None:
    current = ReleaseVersion(1, 1, 0)
    result = current.increment(level)
    assert str(result) == expected
```

## Troubleshooting

### Common Issues

**1. Test Collection Errors**
```bash
# Check for syntax errors in test files
poetry run pytest --collect-only
```

**2. Slow Test Suite**
```bash
# Profile test execution
poetry run pytest --durations=10
```

**3. Flaky Integration Tests**
```bash
# Run integration tests multiple times
poetry run pytest -m integration --count=5
```

**4. Missing Test Markers**
```bash
# Find unmarked tests
poetry run pytest --strict-markers
```

### Environment Issues

**Git Configuration**
Integration tests require git to be configured:
```bash
git config --global user.email "test@example.com"
git config --global user.name "Test User"
```

**Temporary Directory Cleanup**
Test artifacts are automatically cleaned up, but manual cleanup:
```bash
# Clean pytest cache
rm -rf .pytest_cache

# Clean temporary test files
find /tmp -name "pytest-*" -type d -exec rm -rf {} +
```

## Coverage Guidelines

**Target Coverage:**
- Unit tests: >95%
- Integration tests: >60%
- Overall: >90% (currently 98.51%)

**Coverage Exclusions:**
- `__init__.py` files
- Development/debug utilities
- Platform-specific code
- External library wrappers

**Generate Coverage Report:**
```bash
# HTML report
poetry run pytest --cov-report=html

# Terminal report
poetry run pytest --cov-report=term-missing
```

## Best Practices Summary
### **Do**

- Use descriptive test names that explain intent
- Test behavior, not implementation
- Choose the right test level: unit for logic, integration for adapters, E2E for presentation
- Don't mock what you don't own
- Keep tests focused and independent
- Use appropriate test categories
- Run unit tests frequently during development

### **Avoid**

- Testing private methods directly
- Mocking what you don't own - wrap external systems behind Ports and use fakes
- Coupling tests to implementation details
- Sharing state between tests
- Complex test setup that obscures intent
- Running integration tests unnecessarily

---

*For more examples and principles, see the [Testing Guide](testing.md).*
