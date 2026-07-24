# Specifications

The **Specification** pattern expresses composable business rules as predicates over candidate objects.

A `Specification` encapsulates a rule evaluated with `is_satisfied_by(candidate)`. Compositions (`&`, `|`, `~`) allow rules to be combined into richer predicates.

## When to use

Subclass `Specification` and implement `is_satisfied_by(candidate) → bool`. Compose with `&`, `|`, `~` instead of nesting if-statements. Each specification is a single, testable unit of logic.

!!! note "Where the implementation lives"
    The specification pattern is defined in the Domain block alongside Entity and AggregateRoot. It is imported from `forging_blocks.domain.specification`.
