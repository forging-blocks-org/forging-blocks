# Presentation Adapters

## Request Adapter

`RequestAdapter[RawRequest, UseCaseInput]` translates raw transport requests into typed use-case input.

Responsibilities:
- Deserialize transport formats (JSON, form data, query strings)
- Extract and normalize headers, parameters, and body
- Return a typed DTO or command for the use case

Framework-aware. Stateless — produces a value, no side effects.

## When to use (RequestAdapter)

Implement `RequestAdapter` for each transport your system supports — HTTP requests, CLI arguments, message queue payloads. The protocol is generic; your implementation handles the specific deserialization.

## Response Adapter

`ResponseAdapter[UseCaseOutput, RawResponse]` translates application output into transport responses.

Two methods:
- `adapt(output)` — successful use-case output → transport response
- `adapt_error(view_model)` — `ErrorViewModel` → transport error response

Handles both happy and error paths. Produces the final transport response.

## Presentation Adapter

`PresentationAdapter` orchestrates the full request/response lifecycle:

```
1. RequestAdapter.adapt(raw)  → use-case input
2. UseCase.execute(input)     → output or Result
3a. Success  → ResponseAdapter.adapt(output)
3b. Err/Exception → ErrorPresenter → ErrorStatusCodeMapper → ResponseAdapter.adapt_error()
```

Key design:

- Handles both `Result.Err` and raised exceptions. Callers choose their style.
- When `ErrorPresenter` is `None`, exceptions propagate unchanged.

See [Error Handling](error-handling.md) for how errors are converted and rendered.
