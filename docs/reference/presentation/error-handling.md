# Error Handling

The presentation error pipeline converts errors from any source (domain exceptions,
application failures, infrastructure problems) into a consistent, renderable form.
Three components compose to form the pipeline:

1. **ErrorPresenter** adapts errors into view models — it understands framework
   `Error` objects, `Result.Err` values, plain exceptions, and aggregate errors.
2. **ErrorStatusCodeMapper** assigns HTTP-like status codes. Validation errors map
   to 400, rule violations to 409, and generic aggregate/field errors to 422.
3. **ErrorViewModel** carries the structured output — an immutable tuple of messages
   with title, detail, field, code, and status fields.

## Error Presenter

`ErrorPresenter` converts errors into `ErrorViewModel` instances.

It handles framework `Error` objects, `Result.Err` values, plain exceptions, and unknown types. Aggregate errors like `CombinedErrors` and `FieldErrors` are recursively decomposed into individual messages.

## Error Status Code Mapper

`ErrorStatusCodeMapper` assigns HTTP-like status codes:
- Validation errors, including validation field/combined validation errors → 400
- Rule violations → 409
- Generic aggregate/field errors → 422
- Unknown → 500

## Error View Model

`ErrorViewModel` holds an immutable tuple of `ErrorMessageModel` entries. Each message carries:
- `title` — Human-readable summary
- `detail` — Optional longer explanation
- `field` — Optional field reference (e.g. `"username"`)
- `code` — Optional machine-readable error code
- `status_code` — Optional HTTP-like status code

## When to use

Wire `ErrorPresenter`, `ErrorStatusCodeMapper`, and `ErrorViewModel` into a `PresentationAdapter`. Pass an `ErrorPresenter` to catch both `Result.Err` and raised exceptions. Use `ErrorStatusCodeMapper` to attach HTTP codes before rendering.

## Presenter Port

`PresenterPort[ResponseType]` is an orthogonal rendering contract. Extends `InboundPort`. Has `present(response)` for success and `present_error(error)` for failures. An adapter may call both a [Pipeline](middleware.md) for processing and a `PresenterPort` for rendering.

!!! note "Related"
    See [Adapters](adapters.md) for how `PresentationAdapter` wires the error pipeline together. See [Application Ports](../application/ports.md) for the `InboundPort` hierarchy.
