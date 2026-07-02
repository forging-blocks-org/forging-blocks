# Presentation
## Entry points and interaction boundaries

The **Presentation** block translates external inputs (HTTP, CLI, events) into application calls and renders results back. It is the entry point for users and external systems.

Depends on **Application** (for inbound ports). Does not depend on Domain or Infrastructure.

---
## How it works

A `RequestAdapter` deserializes the raw transport request into typed use-case input. A `PresentationAdapter` orchestrates the lifecycle: adapt → execute → respond. On success, the `ResponseAdapter` renders the output. On failure — whether a `Result.Err` or a raised exception — the `ErrorPresenter` converts the error into an `ErrorViewModel`, the `ErrorStatusCodeMapper` assigns a status code, and the `ResponseAdapter` renders the error response.

Middleware wraps the handler in a right-to-left chain. The `Pipeline` pre-builds the chain at construction. Each `Middleware` receives `(request, next_handler)` and may transform, observe, or short-circuit.

---
## How to use

Define a `RequestAdapter` and `ResponseAdapter` for your transport (FastAPI, CLI, message queue). Wire them into a `PresentationAdapter` with your use case and an `ErrorPresenter`. For cross-cutting concerns like logging or auth, compose a `Middleware` chain through a `Pipeline`.

The Presentation block is the outermost ring. It should be thin — translate, delegate, render. Business logic lives in Domain. Coordination lives in Application.

---
## Core abstractions

- **[Adapters](presentation/adapters.md)** — RequestAdapter, ResponseAdapter, PresentationAdapter
- **[Error Handling](presentation/error-handling.md)** — ErrorPresenter, ErrorStatusCodeMapper, ErrorViewModel
- **[Middleware Pipeline](presentation/middleware.md)** — Middleware protocol, Pipeline class

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
