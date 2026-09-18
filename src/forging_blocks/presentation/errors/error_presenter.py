"""Pure transformation that converts errors into display-ready view models.

``ErrorPresenter`` handles framework ``Error`` instances, ``Result.Err``
values, plain ``Exception`` objects, and unknown types via a fallback.
"""

from dataclasses import replace
from typing import cast

from forging_blocks.foundation.errors import CombinedErrors, Error, FieldErrors
from forging_blocks.foundation.result import Err
from forging_blocks.presentation.errors.error_message_model import ErrorMessageModel
from forging_blocks.presentation.errors.error_view_model import ErrorViewModel


class ErrorPresenter:
    """Converts errors into a user-facing ``ErrorViewModel``.

    This presenter is a pure transformation — it produces data that
    presentation adapters (CLI, web, etc.) can render in their own
    medium. It does not depend on any transport or I/O.

    Example:
        ```python
        class SuccessValue:
            def __init__(self, value: object) -> None:
                self.value = value


        class FailureValue:
            def __init__(self, error: object) -> None:
                self.error = error


        class SomeError(Exception):
            pass


        presenter = ErrorPresenter()

        # Idiomatic: handle a Result with structural pattern matching
        result = FailureValue(SomeError())
        match result:
            case SuccessValue(value):
                ...  # handle success
            case FailureValue(error):
                view_model = presenter.to_view_model(error)
                for msg in view_model.messages:
                    print(f"  {msg.title}")

        # Alternative: exception-based handling
        try:
            raise SomeError()
        except SomeError as exc:
            view_model = presenter.to_view_model(exc)
            for msg in view_model.messages:
                print(f"  {msg.title}")
        ```
    """

    __slots__ = ()

    def to_view_model(self, error: object) -> ErrorViewModel:
        """Convert any error into a display-ready view model.

        Args:
            error: An error object — a framework ``Error``, a
                ``Result.Err``, an ``Exception``, a string, or any
                other representation.

        Returns:
            An ``ErrorViewModel`` with one or more ``ErrorMessageModel``
            entries suitable for presentation.

        """
        return ErrorViewModel(messages=tuple(self._to_message_models(error)))

    def _from_composite_error(
        self, error: CombinedErrors[Error[object]] | FieldErrors[Error[object]]
    ) -> list[ErrorMessageModel]:
        if isinstance(error, CombinedErrors):
            return self._from_combined_errors(error)
        return self._from_field_errors(error)

    def _to_message_models(self, error: object) -> list[ErrorMessageModel]:
        """Dispatch *error* to the appropriate converter.

        Aggregate error types (``CombinedErrors``, ``FieldErrors``) are
        checked before the generic ``Error`` branch because they
        subclass it.
        """
        if isinstance(error, (CombinedErrors, FieldErrors)):
            return self._from_composite_error(
                cast(CombinedErrors[Error[object]] | FieldErrors[Error[object]], error)
            )
        if isinstance(error, Error):
            return self._from_framework_error(cast(Error[object], error))
        if isinstance(error, Err):
            return self._from_result_err(cast(Err[object, object], error))
        if isinstance(error, Exception):
            return self._from_exception(error)
        return self._from_unknown(error)

    def _from_framework_error(self, error: Error[object]) -> list[ErrorMessageModel]:
        """Convert a framework ``Error`` whose ``ErrorMetadata`` may hold
        *detail* and *field* context.
        """
        title = error.message.value
        detail = self._extract_detail(error)
        field = self._extract_field(error)
        code = type(error).__name__
        return [ErrorMessageModel(title=title, detail=detail, field=field, code=code)]

    def _from_result_err(self, err: Err[object, object]) -> list[ErrorMessageModel]:
        """Convert a ``Result.Err`` by re-dispatching its wrapped error."""
        return self._to_message_models(err.error)

    def _from_exception(self, exc: Exception) -> list[ErrorMessageModel]:
        """Convert a plain exception using ``str(exc)`` as the title."""
        return [
            ErrorMessageModel(
                title=str(exc),
                code=type(exc).__name__,
            )
        ]

    def _from_unknown(self, error: object) -> list[ErrorMessageModel]:
        """Fallback for any type not explicitly handled."""
        return [
            ErrorMessageModel(
                title=str(error),
                code="UnknownError",
            )
        ]

    def _from_combined_errors(
        self, error: CombinedErrors[Error[object]]
    ) -> list[ErrorMessageModel]:
        """Decompose ``CombinedErrors`` into its individual child messages.

        Each child is recursively dispatched so nested aggregate types
        (e.g. ``FieldErrors`` inside ``CombinedErrors``) decompose
        correctly.

        The wrapper's own summary message (e.g. "3 errors occurred.")
        is discarded — individual child messages are more actionable.
        """
        messages: list[ErrorMessageModel] = []
        for child in error.errors:
            messages.extend(self._to_message_models(child))
        if not messages:
            messages.append(
                ErrorMessageModel(
                    title="No errors specified",
                    code=type(error).__name__,
                )
            )
        return messages

    def _from_field_errors(self, error: FieldErrors[Error[object]]) -> list[ErrorMessageModel]:
        """Decompose ``FieldErrors`` into per-field messages.

        The parent field name is applied only when a child does not
        already carry a more specific field reference.  This preserves
        granular paths when inner errors specify their own field.
        """
        messages: list[ErrorMessageModel] = []
        parent_field = error.field.value
        for child in error.errors:
            child_messages = self._to_message_models(child)
            for msg in child_messages:
                if msg.field is None:
                    msg = replace(msg, field=parent_field)
                messages.append(msg)
        return messages

    @classmethod
    def _extract_detail(cls, error: Error[object]) -> str | None:
        """Pull a human-readable detail string from the error metadata."""
        detail = error.metadata.context.get("detail")
        return detail if isinstance(detail, str) else None

    @classmethod
    def _extract_field(cls, error: Error[object]) -> str | None:
        """Pull a field reference from the error metadata."""
        field = error.metadata.context.get("field")
        return field if isinstance(field, str) else None
