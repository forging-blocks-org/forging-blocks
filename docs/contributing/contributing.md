# Contributing to ForgingBlocks

Hey there :)

Thank you for your interest in contributing to ForgingBlocks.

This document explains **how to participate** in the project and where to find the rules that apply once you start contributing.

You do not need to read everything before opening a pull request.
This guide is meant to help you orient yourself.

---
## Quick summary

- This file explains **how to contribute**.
- Other documents explain **how things should be written or structured**.
- The [Architecture Overview](../guide/architecture-overview.md) explains the layered design used in the project.

Contributions are welcome as long as they respect the project's emphasis on clarity, boundaries, and intentional design.

---

## What you can contribute

Contributions are welcome in several forms, including:

- Bug fixes and improvements
- Documentation clarifications and examples
- New abstractions that align with the existing design
- Tooling, automation, and developer experience improvements

If you are unsure whether an idea fits, opening an issue for discussion is encouraged.

---

## How the project is structured

ForgingBlocks is organized around **explicit responsibility boundaries**.

The documentation mirrors this structure:

- The **Guide** explains how to read and use the toolkit.
- The **Reference** provides precise details for each block and abstraction.
- The **Architectural Styles** section shows optional interpretations from the literature.

Understanding this separation will make contributing easier.

---

## Documentation contributions

Documentation is a first-class concern in this project.

You have to write expressive docstrings because docstrings generates autodocs.

If you plan to modify or add documentation, please read:

- **Docs Conventions**

That document defines the rules and expectations for documentation changes.

---

## Code contributions

When contributing code:

- Prefer clarity over cleverness.
- Follow existing patterns and style guides.
- All public APIs have to include type annotations and docstrings.
- Keep breaking changes restrained and well-documented.

If a change affects public behavior, documentation updates are expected.

---

## Getting started

### Development Setup

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/<username>/forging-blocks.git`
3. **Install dependencies**: `poetry install`
4. **Set up pre-commit hooks**: `pre-commit install`


### Automation Hooks

The project uses `pre-commit` to automate quality checks.

- **Pre-commit (Linting):** Runs on every commit. It checks for code style, trailing whitespace, and common errors. It is designed to be fast.
- **Pre-push (Pipeline):** Runs on every push. It executes the full pipeline (`poetry run poe ci:simulate`), including type checking, all tests, and security scanning, to ensure the remote branch remains stable.

To install both:
```bash
pre-commit install
pre-commit install --hook-type pre-push
```

### Making Changes

1. **Create a feature branch**: `git checkout -b feat/your-feature`
2. **Make your changes** with clear commit messages
3. **Run tests**: `poetry run poe test`
4. **Open a pull request** against `main`

Small, focused pull requests are easier to review.

### Testing Guidelines

This project uses a **3-tier testing architecture**:

- **Unit Tests** (`@pytest.mark.unit`) - Fast, isolated tests with mocks or fakes for business logic
- **Integration Tests** (`@pytest.mark.integration`) - Real infrastructure in isolated environments. Use fixtures/fakes, not mocks.
- **End-to-End Tests** (`@pytest.mark.e2e`) - Complete workflows (typically skipped)

**During development:**
```bash
# Fast feedback loop - run frequently
poetry run poe test:unit

# Before committing - verify all stable tests pass
poetry run poe test
```

**When adding new functionality:**
- Add unit tests for domain logic and business rules
- Add integration tests for external system interactions
- Use fakes at architectural boundaries; don't mock what you don't own
- Follow the naming pattern: `test_when_condition_then_outcome`

See the [Testing Guide](https://forging-blocks-org.github.io/forging-blocks/dev/guide/testing/) for detailed examples.

### Available Development Commands

```bash
# Testing - Primary Commands
poetry run poe test              # Run ALL tests (stable + conditional)
poetry run poe test:unit         # Run unit tests only (fast feedback)
poetry run poe test:integration  # Run integration tests only

# Testing - Extended Commands
poetry run poe test:e2e          # Run end-to-end tests only
poetry run poe test:debug        # Run tests with verbose output

# Code quality
poetry run poe lint              # Check code style
poetry run poe lint:fix          # Fix code style issues
poetry run poe type              # Type checking
poetry run poe bandit            # Security scanning

# CI simulation
poetry run poe ci:check          # Run full CI suite
poetry run poe ci:simulate       # Include documentation build
```

## Documentation
```bash
poetry run poe docs:build           # Build documentation with strict validation
poetry run poe docs:serve           # Serve the current docs locally
poetry run poe docs:generate        # Generate API reference pages
poetry run poe docs:deploy:dev      # Deploy the dev docs version
poetry run poe docs:deploy:release  # Deploy the current release version and aliases
poetry run poe docs:versions        # List mike-managed documentation versions
```

### Release Process (Maintainers Only)

For maintainers preparing releases, see detailed instructions in [Release Guide](https://forging-blocks-org.github.io/forging-blocks/dev/contributing/release-guide/):

```bash
# Prepare release (simulation)
poetry run poe release patch

# Execute release (creates branch and PR)
poetry run poe release patch --execute
```
