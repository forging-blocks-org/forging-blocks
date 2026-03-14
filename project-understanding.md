# ForgingBlocks Project Understanding

## Overview

**ForgingBlocks** is a Python toolkit providing composable abstractions and interfaces for writing clean, testable, and maintainable Python code. It's explicitly **not a framework** but rather a collection of foundational building blocks that developers can use to implement clean architecture patterns.

## Core Philosophy

The project is built around several key principles:

- **Explicit over implicit** - Clear boundaries and intent rather than magic
- **Composable abstractions** - Small, focused components that work together
- **Framework-agnostic** - Does not dictate architecture, provides foundations
- **Type safety** - Heavy use of Python's type system for clarity and safety
- **Testability by design** - Interfaces and abstractions that make testing natural

## Architecture & Structure

### Package Organization

The project follows a layered architecture with clear separation of concerns:

```
src/forging_blocks/
├── foundation/       # Core foundational types and abstractions
├── domain/          # Domain modeling building blocks
├── application/     # Application layer contracts
├── infrastructure/ # Infrastructure adapters
└── presentation/   # Presentation layer support
```

### Key Components

#### 1. Foundation Layer (`foundation/`)

**Result Type System** (`result.py`):
- Rust-inspired `Result[T, E]` type for explicit error handling
- `Ok[T]` and `Err[E]` variants for success/failure cases
- Type-safe alternative to exceptions for business logic
- Prevents the need to catch generic exceptions

**Ports and Adapters** (`ports.py`):
- `Port[InputType, OutputType]` - Base protocol for interface contracts
- `InboundPort` and `OutboundPort` type aliases
- Foundation for dependency inversion and clean architecture
- Generic protocols for type-safe interface definitions

#### 2. Domain Layer (`domain/`)

**Entity Base Class** (`entity.py`):
- Generic `Entity[TId]` with identity-based equality
- Immutable identifier once set
- Draft vs. persisted entity distinction
- Type-safe entity modeling

**Value Objects** (`value_object.py`):
- Generic `ValueObject[RawValueType]` base class
- Immutable objects defined by their attributes
- Equality based on value components, not identity
- Abstract interface requiring `_equality_components()` implementation

**Aggregate Root** (`aggregate_root.py`):
- Domain-driven design aggregate boundary enforcement
- Event handling and consistency boundaries

#### 3. Application Layer (`application/`)

**Port Definitions**:
- Inbound ports for use case interfaces
- Outbound ports for external service contracts
- Repository and unit of work patterns
- Clear separation of application concerns

### Design Patterns Supported

1. **Clean Architecture** - Ports and adapters with dependency inversion
2. **Hexagonal Architecture** - Clear input/output boundaries
3. **Domain-Driven Design** - Rich domain modeling with entities, value objects, and aggregates
4. **Result Pattern** - Explicit error handling without exceptions
5. **Repository Pattern** - Data access abstraction
6. **Unit of Work Pattern** - Transaction boundary management

## Development Standards

### Type Safety
- Python 3.12+ requirement for latest type system features
- Comprehensive type annotations throughout
- MyPy strict mode enforcement
- Pyright type checking support

### Code Quality
- Ruff for linting and formatting (100 char line length)
- Bandit security scanning
- Pre-commit hooks for consistency
- Poetry for dependency management

### Testing Strategy
Three-tier testing architecture:

1. **Unit Tests** (`@pytest.mark.unit`)
   - Fast, isolated tests with mocks
   - Business logic validation
   - Domain rule enforcement

2. **Integration Tests** (`@pytest.mark.integration`)
   - Real infrastructure in isolated environments
   - External service integration validation
   - Database and file system interactions

3. **End-to-End Tests** (`@pytest.mark.e2e`)
   - Complete workflow validation
   - Typically skipped in regular development

### Documentation
- MkDocs with Material theme
- Auto-generated API reference
- Architectural decision records
- Example-driven guides

## Key Benefits

1. **Explicit Error Handling**: Result types eliminate hidden exceptions
2. **Testable Design**: Interfaces and dependency inversion enable easy mocking
3. **Type Safety**: Comprehensive typing prevents runtime errors
4. **Flexibility**: Framework-agnostic approach works with any Python stack
5. **Maintainability**: Clear boundaries and responsibilities
6. **Learning Tool**: Demonstrates clean architecture principles

## Use Cases

- Building clean, testable applications
- Learning and applying architectural patterns
- Creating decoupled systems that scale safely
- Modeling complex domains with type safety
- Implementing hexagonal/clean architecture patterns
- Migrating from legacy codebases to cleaner designs

## Technical Requirements

- **Python 3.12+** (latest type system features)
- **Poetry** for dependency management
- **Compatible with any web framework** (Flask, FastAPI, Django, etc.)
- **Database agnostic** (uses repository pattern)
- **No runtime dependencies** in core package

The project serves as both a practical toolkit and an educational resource for developers wanting to implement clean architecture patterns in Python while maintaining type safety and testability.
