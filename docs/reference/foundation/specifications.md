# Specifications

The **Specification** pattern is a composable predicate over candidate objects.

## Core contract

- **Specification** — Abstract base with `is_satisfied_by(candidate) → bool`
- **ComposableSpecification** — Adds `&`, `|`, `~` for fluent logical composition
- **ExpressionSpecification** — Wraps a user-provided callable predicate

## Logical operators

- **AndSpecification** — Satisfied when both specs are satisfied (`a & b`)
- **OrSpecification** — Satisfied when at least one spec is satisfied (`a | b`)
- **NotSpecification** — Satisfied when the wrapped spec is not satisfied (`~a`)

Composed results remain composable. `(a & b) | c` chains naturally.

## When to use

Specifications are ideal for querying, validation, and filtering. Define a predicate once, then compose it with others rather than writing nested if-statements.

!!! note "Related"
    See [Domain Specifications](../domain/specifications.md) for domain-level usage patterns.
