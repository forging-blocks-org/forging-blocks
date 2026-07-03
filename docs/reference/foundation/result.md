# Result

`Result` models the **explicit outcome** of an operation. It represents either success (`Ok`) or failure (`Err`), without relying on exceptions for control flow.

Result is about **flow**, not about error representation.

## When to use

Use `Result` when failure is part of normal behavior — validation, parsing, rule evaluation, boundary checks. Return `Ok(value)` for success, `Err(error)` for failure.

## Variants

- **Ok[ValueType]** — Wraps a successful value. `is_ok` is `True`, `is_err` is `False`.
- **Err[ErrorType]** — Wraps an error. `is_ok` is `False`, `is_err` is `True`.

Both support structural pattern matching through `__match_args__`.

## Common operations

- `is_ok` / `is_err` — Branch on the variant (property, not method)
- `value` — Unwrap the success payload
- `error` — Unwrap the error payload
- `map(fn)` — Transform success, pass errors through
- `map_error(fn)` — Transform error, pass success through
- `flat_map(fn)` — Chain operations that return `Result`
- `get_value_or(default)` — Fallback on error
- `get_value_or_else(fn)` — Compute fallback from the error

## Design

`Result` is a `Protocol` — `Ok` and `Err` are concrete implementations. You construct `Ok(...)` or `Err(...)` but type-annotate with `Result[ValueType, ErrorType]`.

!!! note "Related"
    See [Errors](errors.md) for the `Error` type used as the error payload in `Err`.
