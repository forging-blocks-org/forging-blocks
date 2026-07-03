# Error Handling

## Error Presenter

`ErrorPresenter` converts errors into `ErrorViewModel` instances.

It handles framework `Error` objects, `Result.Err` values, plain exceptions, and unknown types. Aggregate errors like `CombinedErrors` and `FieldErrors` are recursively decomposed into individual messages.

## Error Status Code Mapper

`ErrorStatusCodeMapper` assigns HTTP-like status codes:
- Validation errors → 400
- Rule violations → 409
- Aggregate/field errors → 422
- Unknown → 500

## Error View Model

`ErrorViewModel` holds a list of `ErrorMessageModel` entries. Each message carries:
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
