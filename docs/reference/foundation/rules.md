# Rules

Rules encapsulate reusable, composable predicates for validation and business logic.

## ValidationRule

`ValidationRule` is an abstract base class for synchronous validation rules. Each rule inspects an arbitrary value and returns a list of `RuleViolationError` objects — empty when the value is valid.

### Contract

```python
class ValidationRule(ABC):
    @abstractmethod
    def validate(self, value: Any) -> list[RuleViolationError]:
        ...
```

### Characteristics

- **Stateless** — rules carry no mutable state and can be reused safely across threads and coroutines
- **Side-effect-free** — `validate` must not perform I/O or mutate the input
- **Composable** — rules can be combined into composite chains that report every failure

### When to use

Subclass `ValidationRule` for any synchronous validation check. Return `RuleViolationError` instances carrying `ErrorMessage` and `ErrorMetadata` with a field name and error code. Compose multiple rules with `CompositeValidationRule` to validate several constraints at once.

!!! note "Related"
    See [Domain Validators](../domain/validators.md) for concrete rule implementations like `RequiredValidator`, `EmailValidator`, `LengthValidator`, and `RangeValidator`.
