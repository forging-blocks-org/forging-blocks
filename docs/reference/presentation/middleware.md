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
