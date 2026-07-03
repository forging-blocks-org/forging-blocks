# Auto-Freeze

The `@auto_freeze` decorator enforces immutability after `__init__` completes — no `frozen=True` dataclass boilerplate needed.

## Usage

Apply to any class:

- `@auto_freeze` — Freezes the entire instance
- `@auto_freeze()` — Equivalent, explicit parens form
- `@auto_freeze(attrs=["_id"])` — Selectively freeze specific attributes only

After `__init__` returns, any attempt to assign a frozen attribute raises `CantModifyImmutableAttributeError`. The decorator handles `__init__` nesting (inheritance chains) and skips abstract classes.

## When to use

`auto_freeze` is an alternative to inheriting from `ValueObject`. If your class already has its own base class and you only need immutability — without value-based equality or hashing — prefer `@auto_freeze`. If you also need equality-by-value, use the [ValueObject](value-objects.md) base class instead. Both are optional; you can use neither.

!!! note "Design"
    `auto_freeze` injects a `__setattr__` override and a freeze flag. It detects existing custom `__setattr__` implementations and avoids double-wrapping.
