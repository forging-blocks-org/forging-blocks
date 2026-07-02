"""Pure transformation that converts errors into display-ready view models.

``ErrorPresenter`` handles framework ``Error`` instances, ``Result.Err``
values, plain ``Exception`` objects, and unknown types via a fallback.
"""

from collections.abc import Mapping
from dataclasses import replace
from typing import TYPE_CHECKING, cast

from forging_blocks.presentation.error_message_model import ErrorMessageModel
from forging_blocks.presentation.error_view_model import ErrorViewModel

if TYPE_CHECKING:
    from forging_blocks.foundation.errors import CombinedErrors, Error, FieldErrors
    from forging_blocks.foundation.result import Err


class ErrorPresenter:
    """Converts errors into a user-facing ``ErrorViewModel``.

    This presenter is a pure transformation — it produces data that
    presentation adapters (CLI, web, etc.) can render in their own
    medium. It does not depend on any transport or I/O.

    Usage::

        presenter = ErrorPresenter()

        try:
            result = await use_case.execute(request)
        except Error as exc:
            view_model = presenter.to_view_model(exc)
            for msg in view_model.messages:
                print(f"  {msg.title}")
    """

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
        return ErrorViewModel(messages=self._to_message_models(error))

    def _to_message_models(self, error: object) -> list[ErrorMessageModel]:
        """Dispatch *error* to the appropriate converter.

        Aggregate error types (``CombinedErrors``, ``FieldErrors``) are
        checked before the generic ``Error`` branch because they
        subclass it.
        """
        from forging_blocks.foundation.errors import CombinedErrors, Error, FieldErrors
        from forging_blocks.foundation.result import Err

        if isinstance(error, CombinedErrors):
            return self._from_combined_errors(
                cast("CombinedErrors[Error[dict[str, object]]]", error)
            )
        if isinstance(error, FieldErrors):
            return self._from_field_errors(cast("FieldErrors[Error[dict[str, object]]]", error))
        if isinstance(error, Error):
            return self._from_framework_error(cast("Error[Mapping[str, object]]", error))
        if isinstance(error, Err):
            return self._from_result_err(cast("Err[object, object]", error))
        if isinstance(error, Exception):
            return self._from_exception(error)
        return self._from_unknown(error)

    def _from_framework_error(
        self, error: "Error[Mapping[str, object]]"
    ) -> list[ErrorMessageModel]:
        """Convert a framework ``Error`` whose ``ErrorMetadata`` may hold
        *detail* and *field* context.
        """
        title = error.message.value
        detail = self._extract_detail(error)
        field = self._extract_field(error)
        code = type(error).__name__
        return [ErrorMessageModel(title=title, detail=detail, field=field, code=code)]

    def _from_result_err(self, err: "Err[object, object]") -> list[ErrorMessageModel]:
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
        self, error: "CombinedErrors[Error[dict[str, object]]]"
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

    def _from_field_errors(
        self, error: "FieldErrors[Error[dict[str, object]]]"
    ) -> list[ErrorMessageModel]:
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

    @staticmethod
    def _extract_detail(error: "Error[Mapping[str, object]]") -> str | None:
        """Pull a human-readable detail string from the error metadata."""
        ctx: Mapping[str, object] = error.metadata.context
        detail = ctx.get("detail")
        return detail if isinstance(detail, str) else None

    @staticmethod
    def _extract_field(error: "Error[Mapping[str, object]]") -> str | None:
        """Pull a field reference from the error metadata."""
        ctx: Mapping[str, object] = error.metadata.context
        field = ctx.get("field")
        return field if isinstance(field, str) else None
