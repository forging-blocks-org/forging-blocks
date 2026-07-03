# Meta Utilities

Foundation provides **runtime enforcement** decorators. Unlike `typing.final` or `ABC`, which are static-analysis hints, these decorators enforce constraints at runtime.

## Utilities

- **@runtime_final** — Prevents subclassing. Raises `TypeError` if a subclass attempts to inherit.
- **@runtime_sealed** — Prevents instantiation. Raises `TypeError` if the class is constructed directly.
- **@runtime_abstract** — Requires subclassing. Raises `TypeError` if the class itself is instantiated (stronger than `ABC`).

All three are class decorators that modify `__init_subclass__` and `__init__` to enforce the constraint at the moment of misuse rather than at type-checking time.

## When to use

Use when you need guarantees, not suggestions — for framework-level base classes, sealed hierarchies, or security-sensitive boundaries.
