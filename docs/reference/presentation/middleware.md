# Middleware Pipeline

## Middleware Protocol

`Middleware[RequestType, ResponseType]` defines cross-cutting interceptors. Each middleware receives the request and a `next_handler` callable. It may:
- Transform the request before delegating
- Transform the response after delegating
- Short-circuit by returning without calling `next_handler`

Middleware does **not** extend `Port` — its shape `(request, next_handler) → response` is a different category.

## Pipeline

`Pipeline` composes middleware into an immutable, right-to-left chain. The first middleware executes first inbound and last outbound:

```
[A, B, C] → A wraps B wraps C wraps handler
Inbound:   A → B → C → handler
Outbound:  A ← B ← C ← handler
```

## When to use

Implement `Middleware` for any cross-cutting concern: logging, authentication, metrics, rate limiting. Compose them in a `Pipeline` and pass it to the `PresentationAdapter`. Order matters — the first middleware wraps the outermost layer.

The chain is pre-built at construction. `execute()` is a single delegation.

## Built-in Middleware

The toolkit ships four ready-to-use middleware implementations:

|Middleware|Purpose|Constructor|
|---|---|---|
|`ValidationMiddleware`|Validates requests and short-circuits with an error response on failure|`validator: Callable[[RequestType], ResponseType \| None]`|
|`LoggingMiddleware`|Logs every request and response at debug level|`logger: LoggerPort`|
|`TimingMiddleware`|Logs wall-clock execution time at info level|`logger: LoggerPort`|
|`ErrorHandlingMiddleware`|Catches exceptions, maps them to responses via a user-supplied `on_error` callable, and optionally logs them|`on_error: Callable[[ErrorViewModel], ResponseType]`, `error_presenter: ErrorPresenter \| None`, `logger: LoggerPort \| None`|

These compose with custom middleware in a `Pipeline` — the built-ins handle common cross-cutting concerns so you can focus on domain-specific interceptors.

### Composed Pipeline Example

```python
from forging_blocks.presentation.builtin import (
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    TimingMiddleware,
    ValidationMiddleware,
)
from forging_blocks.presentation.middleware.pipeline import Pipeline

pipeline = Pipeline[MyRequest, MyResponse](
    [
        ErrorHandlingMiddleware(on_error=map_error, logger=logger),
        ValidationMiddleware(validator=validate),
        LoggingMiddleware(logger=logger),
        TimingMiddleware(logger=logger),
    ],
    handler=my_use_case_handler,
)

response = await pipeline.execute(request)
```
