# Meta Utilities

Foundation provides **runtime enforcement** through metaclasses and decorators. `ABC` and `ABCMeta` enforce abstract contracts at runtime; `FinalMeta` and `FinalABCMeta` enforce `@runtime_final` method overrides at runtime.

## Metaclasses

- **FinalMeta** — Prevents overriding inherited `@runtime_final` methods at runtime. It does not prevent subclassing.
- **FinalABCMeta** — Combines that method-override check with `ABCMeta`, which still allows concrete subclasses after they implement abstract methods.

## Decorators

- **@runtime_final** — Prevents a method from being overridden in subclasses. Raises `TypeError` if a child class attempts to override it.

## When to use

Use `FinalMeta` or `FinalABCMeta` when a class must protect selected methods from being overridden. Use `@runtime_final` on methods that subclasses should call but never override.
