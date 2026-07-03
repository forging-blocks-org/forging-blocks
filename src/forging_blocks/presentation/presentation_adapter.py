"""Orchestrator that wires transport adapters to a use case with error handling.

``PresentationAdapter`` handles both ``Result.Err`` and raised
``Exception`` / ``Error``, so callers may choose their error-signalling
style without changing the adapter.
"""

from typing import TYPE_CHECKING, cast

from forging_blocks.foundation.result import Result
from forging_blocks.presentation.error_presenter import ErrorPresenter
from forging_blocks.presentation.error_status_code_mapper import (
    ErrorStatusCodeMapper,
)
from forging_blocks.presentation.request_adapter import RequestAdapter
from forging_blocks.presentation.response_adapter import ResponseAdapter

if TYPE_CHECKING:
    from forging_blocks.application.ports.inbound import UseCase


class PresentationAdapter[RawRequest, UseCaseInput, UseCaseOutput, RawResponse]:
    """Orchestrates the full request/response lifecycle for a use case.

    Usage::

        adapter = PresentationAdapter(
            use_case=create_order_use_case,
            request_adapter=JsonRequestAdapter(),
            response_adapter=JsonResponseAdapter(),
            error_presenter=ErrorPresenter(),
        )
        response = await adapter.handle(http_request)
    """

    __slots__ = (
        "_error_presenter",
        "_request_adapter",
        "_response_adapter",
        "_status_mapper",
        "_use_case",
    )

    def __init__(
        self,
        use_case: "UseCase[UseCaseInput, UseCaseOutput]",
        request_adapter: RequestAdapter[RawRequest, UseCaseInput],
        response_adapter: ResponseAdapter[UseCaseOutput, RawResponse],
        error_presenter: ErrorPresenter | None = None,
    ) -> None:
        """Wire the adapter with its collaborators.

        Args:
            use_case: The application use case to invoke.
            request_adapter: Translates transport requests into
                use-case input.
            response_adapter: Translates use-case output into
                transport responses (success and error).
            error_presenter: Optional error formatter. When omitted,
                exceptions propagate unchanged.
        """
        self._use_case = use_case
        self._request_adapter = request_adapter
        self._response_adapter = response_adapter
        self._error_presenter = error_presenter
        self._status_mapper = ErrorStatusCodeMapper()

    async def handle(self, raw_request: RawRequest) -> RawResponse:
        """Process *raw_request* through the full lifecycle.

        Handles both ``Result.Err`` (if the use case returns a
        ``Result``) and raised exceptions so callers may choose
        their preferred error style.

        Args:
            raw_request: The transport-level request.

        Returns:
            A transport-level response (success or error, depending
            on the outcome).

        Raises:
            Exception: When *error_presenter* is ``None`` and the
                use case raises, the original exception propagates.
        """
        try:
            use_case_input = self._request_adapter.adapt(raw_request)
            use_case_output = await self._use_case.execute(use_case_input)
        except Exception as exc:
            if self._error_presenter is None:
                raise
            view_model = self._error_presenter.to_view_model(exc)
            mapped = self._status_mapper.map(view_model)
            return self._response_adapter.adapt_error(mapped)

        if isinstance(use_case_output, Result):
            result = cast("Result[UseCaseOutput, object]", use_case_output)
            if result.is_err:
                if self._error_presenter is None:
                    error_value = result.error
                    if isinstance(error_value, BaseException):
                        raise error_value
                    raise RuntimeError(str(error_value))
                view_model = self._error_presenter.to_view_model(result.error)
                mapped = self._status_mapper.map(view_model)
                return self._response_adapter.adapt_error(mapped)
            return self._response_adapter.adapt(result.value)

        return self._response_adapter.adapt(use_case_output)
