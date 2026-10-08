# Presentation Adapters

## Request Adapter

`RequestAdapter[RawRequest, UseCaseInput]` translates raw transport requests into typed use-case input.

Responsibilities:
- Deserialize transport formats (JSON, form data, query strings)
- Extract and normalize headers, parameters, and body
- Return a typed DTO or command for the use case

Transport-specific implementations may be framework-aware. The protocol itself is
framework-agnostic and stateless — it produces a value without side effects.

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
2. ApplicationServicePort.execute(input)     → declared output type
3a. Success  → ResponseAdapter.adapt(output)
3b. Result.Err or exception → ErrorPresenter → ErrorStatusCodeMapper → ResponseAdapter.adapt_error()
```

Key design:

- Handles raised exceptions and can handle `Result.Err` when the adapter is configured to unwrap use-case results.
- When `ErrorPresenter` is `None`, exceptions propagate unchanged.

See [Error Handling](error-handling.md) for how errors are converted and rendered.
