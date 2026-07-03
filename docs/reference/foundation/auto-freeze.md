# Auto-Freeze

The `@auto_freeze` decorator enforces immutability after `__init__` completes — no `frozen=True` dataclass boilerplate needed.

## Usage

Apply to any class:

- `@auto_freeze` — Freezes the entire instance
- `@auto_freeze()` — Equivalent, explicit parens form
- `@auto_freeze(attrs=["_id"])` — Selectively freeze specific attributes only

After `__init__` returns, any attempt to assign a frozen attribute raises `CantModifyImmutableAttributeError`. The decorator handles `__init__` nesting (inheritance chains) and skips abstract classes.

!!! note "Design"
    `auto_freeze` injects a `__setattr__` override and a freeze flag. It detects existing custom `__setattr__` implementations and avoids double-wrapping.
