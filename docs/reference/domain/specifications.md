# Specifications

The **Specification** pattern expresses composable business rules as predicates over candidate objects.

A `Specification` encapsulates a rule evaluated with `is_satisfied_by(candidate)`. Compositions (`&`, `|`, `~`) allow rules to be combined into richer predicates.

Specifications are well-suited for querying, validation, and filtering within domain logic.

!!! note "Where the implementation lives"
    The specification pattern is defined in the **Foundation** block because composable predicates are reusable outside the Domain block. The Domain block re-exports it.

## Domain Errors

Domain Errors represent invalid states or rule violations within the problem space. They express domain meaning, indicate invariant violations, and are not technical failures.

!!! note "On error semantics"
    Domain Errors describe *why* something is invalid in domain terms. They should not encode transport, persistence, or framework concerns.
