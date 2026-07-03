# Meta Utilities

Foundation provides **runtime enforcement** through metaclasses and decorators. Unlike `typing.final` or `ABC`, which are static-analysis hints, these enforce constraints at runtime.

## Metaclasses

- **FinalMeta** — Prevents subclassing at runtime. Inheriting from a class with this metaclass raises `TypeError`.
- **FinalABCMeta** — Combines `FinalMeta` with `ABCMeta`. Prevents subclassing and requires abstract method implementation.

## Decorators

- **@runtime_final** — Prevents a method from being overridden in subclasses. Raises `TypeError` if a child class attempts to override it.

## When to use

Use `FinalMeta` or `FinalABCMeta` when a class must never be subclassed — framework-level base classes, sealed hierarchies, security boundaries. Use `@runtime_final` on methods that subclasses should call but never override.
