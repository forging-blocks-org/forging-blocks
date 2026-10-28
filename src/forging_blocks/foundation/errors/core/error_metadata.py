from dataclasses import dataclass, field


@dataclass(frozen=True)
class ErrorMetadata[T]:
    """Represents metadata about the error.

    Example:
        ```python
        meta = ErrorMetadata[str](context={"field": "username"})
        assert meta.context == {"field": "username"}
        ```
    """

    context: dict[str, T] = field(default_factory=dict)
