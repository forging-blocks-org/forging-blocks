# API Stability

This document defines the public API and compatibility policy for ForgingBlocks.

## SemVer Policy

ForgingBlocks follows [Semantic Versioning 2.0.0](https://semver.org/) from v1.0.0 onward.

- **MAJOR** (`1.X.Y` → `2.0.0`): Incompatible API changes:
  removals, signature changes, and breaking behavioral changes.
- **MINOR** (`1.X.Y` → `1.(X+1).0`): Backward-compatible additions:
  new symbols, optional parameters, and modules.
- **PATCH** (`1.X.Y` → `1.X.(Y+1)`): Backward-compatible bug fixes that restore documented
  behavior.

## Public API Definition

The following constitute the public API, covered by these stability guarantees:

- Symbols listed in `forging_blocks.__all__` (currently `__version__`).
- Every symbol listed in `__all__` of:
    - `forging_blocks.foundation`
    - `forging_blocks.domain`
    - `forging_blocks.application`
    - `forging_blocks.application.ports`
    - `forging_blocks.infrastructure`
    - `forging_blocks.presentation`
- Public module-level functions and classes with docstrings that are **not** prefixed with `_`,
  even if absent from `__all__`.

Changes to any `__all__` manifest follow the same SemVer rules: adding an exported symbol is
non-breaking and belongs in a MINOR release, while removing an exported symbol requires a
MAJOR release.

### Frozen Facade Additions

The following symbols are supported through the listed facade paths:

|Facade|Symbols|
|---|---|
|`forging_blocks.foundation`|`Debuggable`|
|`forging_blocks.application`|`TransactionError`|
|`forging_blocks.application.ports`|`AuthorizationPort`, `ValidationPort`|

## Breaking Changes

A change is **breaking** if any of the following occur:

- Removal of a public symbol (class, function, or constant) from the public API.
- Signature change to a public callable: adding a required parameter, removing a parameter,
  changing a parameter type, or changing the return type.
- Behavioral change that breaks a documented contract, such as replacing `None` with an
  exception or replacing `ValueError` with a different exception type.
- Removal of a module from the public import path.

## Non-Breaking Changes

The following are **not** breaking:

- Adding new symbols (classes, functions, constants, modules).
- Adding optional parameters with defaults to existing callables.
- Relaxing type constraints (e.g., widening a parameter type from `str` to `str | int`).
- Fixing bugs that restore behavior to match the documented contract.
- Adding new modules or sub-packages.

## What Is NOT Covered

These are explicitly excluded from the stability guarantee:

- Internal helpers: modules named `_*` or under directories containing `helpers/`.
- `_`-prefixed members, even on public classes.
- Undocumented behavior: observed behavior not described in docstrings or reference
  documentation.
- Experimental features marked as such. None currently exist; if introduced, they will carry
  explicit opt-in warnings.

## Deprecation Process

When a public symbol must be removed or its contract changed incompatibly:

1. **Deprecation release** (MINOR): The symbol emits a `DeprecationWarning` when used. Its
   docstring is updated with a `.. deprecated:: X.Y` directive pointing to the replacement.
   The symbol remains fully functional.
2. **Removal release** (next MAJOR, at least one minor version later): The symbol is removed.

At least **one minor version** must elapse between deprecation and removal. This guarantees
downstream consumers a full release cycle to migrate.
