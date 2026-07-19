# Presentation
## Entry points and interaction boundaries

The **Presentation** block translates external inputs (HTTP, CLI, events) into application calls and renders results back. It is the entry point for users and external systems.

Depends on **Application** (for inbound ports). Does not depend on Domain or Infrastructure.

---
## How it works

The `PresentationAdapter` orchestrates the full lifecycle:

- **Adapt** — `RequestAdapter` deserializes the raw request into typed use-case input.
- **Execute** — The use case runs and returns a value or a `Result`.
- **Respond** — On success, `ResponseAdapter` renders the output.

On failure, the error pipeline kicks in:

- `ErrorPresenter` converts the error into an `ErrorViewModel`.
- `ErrorStatusCodeMapper` assigns a status code.
- `ResponseAdapter` renders the error response.

This handles both `Result.Err` and raised exceptions, so callers can choose their error style.

Middleware wraps the handler in a right-to-left chain. The `Pipeline` pre-builds the chain at construction. Each `Middleware` receives `(request, next_handler)` and may transform, observe, or short-circuit. The toolkit ships four [built-in middleware](presentation/middleware.md#built-in-middleware) for logging, timing, validation, and error handling.

---
## How to use

1. Define a `RequestAdapter` and `ResponseAdapter` for your transport — FastAPI, CLI, message queue.
2. Wire them into a `PresentationAdapter` with your use case and an `ErrorPresenter`.
3. For cross-cutting concerns like logging or auth, compose a `Middleware` chain through a `Pipeline`.

The Presentation block is the outermost ring. Keep it thin — translate, delegate, render. Business logic lives in Domain. Coordination lives in Application.

---
## Core abstractions

- **[Adapters](presentation/adapters.md)** — RequestAdapter, ResponseAdapter, PresentationAdapter
- **[Error Handling](presentation/error-handling.md)** — ErrorPresenter, ErrorStatusCodeMapper, ErrorViewModel, PresenterPort
- **[Middleware Pipeline](presentation/middleware.md)** — Middleware protocol, Pipeline class, and built-in middleware

---
## What it does not do

- Contain business rules or domain logic
- Implement persistence or I/O directly
- Define transactional boundaries
- Make decisions about system behavior

---
## Glossary

!!! note "Request Adapter"
    Translates raw transport requests into typed use-case input.

!!! note "Response Adapter"
    Translates use-case output (success and error) into transport responses.

!!! note "Presentation Adapter"
    Orchestrator wiring a use case to adapters with error handling. Handles both `Result.Err` and exceptions.

!!! note "Error Presenter"
    Converts errors into display-ready `ErrorViewModel` instances. Decomposes aggregate errors recursively.

!!! note "Error Status Code Mapper"
    Assigns HTTP-like status codes to error messages based on error type.

!!! note "Middleware"
    Cross-cutting interceptor that may transform, observe, or short-circuit requests.

!!! note "Pipeline"
    Immutable right-to-left chain of middleware around a terminal handler.
