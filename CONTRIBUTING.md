# Contributing to ForgingBlocks

Thank you for your interest in contributing to ForgingBlocks.

This document explains **how to participate** in the project and where to find the rules that apply once you start contributing.

You do not need to read everything before opening a pull request.
This guide is meant to help you orient yourself.

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
- The **Reference** defines responsibilities and terminology.
- **Architectural Styles** show optional interpretations.
- **Examples** demonstrate usage without prescribing structure.

Understanding this separation will make contributing easier.

---

## Documentation contributions

Documentation is a first-class concern in this project.

If you plan to modify or add documentation, please read:

- **Docs Conventions**
  `docs/contributing/docs_conventions.md`

That document defines the rules and expectations for documentation changes.

---

## Code contributions

When contributing code:

- Prefer clarity over cleverness.
- Keep responsibilities explicit.
- Avoid introducing architectural enforcement.
- Add tests where behavior is non-trivial.

If a change affects public behavior, documentation updates are expected.

---

## Getting started

### Development Setup

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/YOUR-USERNAME/forging-blocks.git`
3. **Install dependencies**: `poetry install`
4. **Set up pre-commit hooks** (optional): `pre-commit install`

### Making Changes

1. **Create a feature branch**: `git checkout -b feature/your-feature`
2. **Make your changes**
3. **Add tests** for new functionality
4. **Run the full test suite**:
   ```bash
   poetry run poe ci:check
   ```
5. **Submit a pull request** with a clear, concise description

Small, focused pull requests are easier to review.

### Available Development Commands

```bash
# Testing
poetry run poe test              # Run tests
poetry run poe test:debug        # Run tests with verbose output

# Code quality
poetry run poe lint              # Check code style
poetry run poe lint:fix          # Fix code style issues
poetry run poe type              # Type checking
poetry run poe bandit            # Security scanning

# CI simulation
poetry run poe ci:check          # Run full CI suite
poetry run poe ci:simulate       # Include documentation build

# Documentation
poetry run poe docs:build        # Build documentation
poetry run poe docs:generate     # Generate API reference
```

### Release Process (Maintainers Only)

For maintainers preparing releases, see detailed instructions in [Release Guide](release-guide.md):

```bash
# Prepare release (simulation)
poetry run poe release:dry-run

# Execute release (creates branch and PR)
poetry run poe release:patch   # or release:minor / release:major
```

---

## In short

- This file explains **how to contribute**.
- Other documents explain **how things should be written or structured**.
- When in doubt, ask questions early.

Contributions are welcome as long as they respect the project’s emphasis on clarity, boundaries, and intentional design.
