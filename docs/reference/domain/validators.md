# Validators

Concrete `ValidationRule` implementations for common input constraints. Each validator is a stateless, reusable rule that returns `RuleViolationError` instances when the input fails its constraint.

## RequiredValidator

Fails when the value is `None` or an empty string. Useful for mandatory form fields, API parameters, and command properties.

```python
RequiredValidator("username").validate(None)     # -> [RuleViolationError]
RequiredValidator("username").validate("Alice")  # -> []
```

## EmailValidator

Validates that a string value matches a basic RFC-compatible email pattern. Suitable for client-side and API-level validation — does not check deliverability.

```python
EmailValidator("email").validate("user@example.com")  # -> []
EmailValidator("email").validate("not-an-email")      # -> [RuleViolationError]
```

## LengthValidator

Validates that a string's length falls within a `[minimum_length, maximum_length]` range. Both bounds are inclusive and optional — omit a bound to leave it unconstrained.

```python
LengthValidator("password", minimum_length=8, maximum_length=128).validate("short")  # -> [RuleViolationError]
LengthValidator("password", minimum_length=8).validate("0" * 10)                      # -> []
```

## RangeValidator

Validates that a numeric value (integer or float) falls within a `[minimum_value, maximum_value]` range. Both bounds are inclusive and optional.

```python
RangeValidator("age", minimum_value=0, maximum_value=150).validate(-5)  # -> [RuleViolationError]
RangeValidator("age", minimum_value=0).validate(30)                     # -> []
```

## CompositeValidationRule

Combines multiple validators into a single rule. Evaluates every rule and returns all errors — there is no short-circuit. Every violation is reported.

```python
composite = CompositeValidationRule([
    RequiredValidator("email"),
    EmailValidator("email"),
])
composite.validate("bad")  # -> [RuleViolationError for invalid_email]
```

## When to use

Use individual validators for single-field checks in commands, queries, and API input. Compose them with `CompositeValidationRule` when multiple constraints apply to the same field or when several fields must be validated together. All validators use the foundation `RuleViolationError` type with `ErrorMetadata` carrying field and error-code context.

!!! note "Related"
    See [Foundation Rules](../foundation/rules.md) for the `ValidationRule` base class and [Foundation Errors](../foundation/errors.md) for `RuleViolationError`.
