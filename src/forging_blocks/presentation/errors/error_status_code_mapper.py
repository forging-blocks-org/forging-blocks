"""Maps framework error types to HTTP-like status codes."""

from dataclasses import replace

from forging_blocks.presentation.errors.error_view_model import ErrorViewModel


class ErrorStatusCodeMapper:
    """Assigns status codes to ``ErrorMessageModel`` entries based on
    the error type.

    Default mapping:
        - ``ValidationError``        → 400
        - ``RuleViolationError``     → 409
        - ``CombinedErrors``/group   → 422
        - anything else              → 500
    """

    def map(self, view_model: ErrorViewModel) -> ErrorViewModel:
        """Return a new ``ErrorViewModel`` with ``status_code`` set on
        every message.

        Args:
            view_model: The view model produced by
                ``ErrorPresenter.to_view_model``.

        Returns:
            A new ``ErrorViewModel`` whose ``ErrorMessageModel``
            entries each carry the appropriate ``status_code``.

        """
        enriched = tuple(
            replace(msg, status_code=self._status_code_for(msg.code)) for msg in view_model.messages
        )
        return ErrorViewModel(messages=enriched)

    def _status_code_for(self, code: str | None) -> int:
        if code is None:
            return 500
        status_map: dict[str, int] = {
            "ValidationError": 400,
            "ValidationFieldErrors": 400,
            "CombinedValidationErrors": 400,
            "RuleViolationError": 409,
            "CombinedRuleViolationErrors": 409,
            "CombinedErrors": 422,
            "FieldErrors": 422,
        }
        return status_map.get(code, 500)
