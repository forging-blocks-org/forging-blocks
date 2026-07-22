"""Orchestrator that wires transport adapters to a use case with error handling.

``PresentationAdapter`` handles both returned ``Err`` and raised
``Exception`` / ``Error``, so callers may choose their error-signalling
style without changing the adapter. Result unwrapping is opt-in via
*unwrap_use_case_result* — disable it when the use case's natural output
type is itself a ``Result``.

An optional ``Pipeline`` wraps the use case in cross-cutting middleware
(logging, timing, etc.) that executes before and after the handler.
"""

from dataclasses import replace
from typing import TYPE_CHECKING, cast

from forging_blocks.foundation.result import Result
from forging_blocks.presentation.adapters.request_adapter import RequestAdapter
from forging_blocks.presentation.adapters.response_adapter import ResponseAdapter
from forging_blocks.presentation.errors.error_presenter import ErrorPresenter
from forging_blocks.presentation.errors.error_status_code_mapper import (
    ErrorStatusCodeMapper,
)
from forging_blocks.presentation.errors.error_view_model import ErrorViewModel
from forging_blocks.presentation.middleware.pipeline import Pipeline

if TYPE_CHECKING:
    from forging_blocks.application.ports.inbound import UseCasePort


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
        "_pipeline",
        "_request_adapter",
        "_response_adapter",
        "_status_mapper",
        "_unwrap_use_case_result",
        "_use_case",
    )

    def __init__(
        self,
        use_case: "UseCasePort[UseCaseInput, UseCaseOutput]",
        request_adapter: RequestAdapter[RawRequest, UseCaseInput],
        response_adapter: ResponseAdapter[UseCaseOutput, RawResponse],
        error_presenter: ErrorPresenter | None = None,
        pipeline: Pipeline[UseCaseInput, UseCaseOutput] | None = None,
        unwrap_use_case_result: bool = True,
    ) -> None:
        """Wire the adapter with its collaborators.

        Args:
            use_case: The application use case to invoke.
                When *pipeline* is provided this instance is unused
                at runtime — the pipeline's terminal handler is
                invoked instead. It is still required as a fallback
                when *pipeline* is ``None``.
            request_adapter: Translates transport requests into
                use-case input.
            response_adapter: Translates use-case output into
                transport responses (success and error).
            error_presenter: Optional error formatter. When omitted,
                exceptions propagate unchanged.
            pipeline: Optional pre-built middleware pipeline that
                wraps *use_case*. When provided, ``pipeline.execute``
                is called instead of ``use_case.execute`` directly.
                The pipeline's terminal handler should be the use
                case's ``execute`` method.
            unwrap_use_case_result: When ``True`` (default), a use
                case that returns ``Result[T, E]`` has its ``Ok``
                value extracted before passing to
                ``response_adapter.adapt``, and ``Err`` values are
                routed through the *error_presenter*. Set to
                ``False`` when the use case's output type is itself
                a ``Result`` that the response adapter should receive
                unmodified.

        """
        self._use_case = use_case
        self._request_adapter = request_adapter
        self._response_adapter = response_adapter
        self._error_presenter = error_presenter
        self._pipeline = pipeline
        self._unwrap_use_case_result = unwrap_use_case_result
        self._status_mapper = ErrorStatusCodeMapper()

    async def handle(self, raw_request: RawRequest) -> RawResponse:
        """Process *raw_request* through the full lifecycle.

        Handles both ``Result.Err`` (when *unwrap_use_case_result* is
        ``True``) and raised exceptions so callers may choose their
        preferred error style.

        Request-adapter failures are treated as transport-level input
        errors (status 400). Application errors are mapped through
        ``ErrorStatusCodeMapper``.

        Args:
            raw_request: The transport-level request.

        Returns:
            A transport-level response (success or error, depending
            on the outcome).

        Raises:
            Exception: When *error_presenter* is ``None`` and a use
                case raises, or a ``Result.Err`` is encountered
                without an error presenter, the original exception
                (or a ``RuntimeError`` for non-exception errors)
                propagates.

        """
        try:
            use_case_input = self._request_adapter.adapt(raw_request)
        except Exception as exc:
            if self._error_presenter is None:
                raise
            view_model = self._error_presenter.to_view_model(exc)
            mapped = ErrorViewModel(
                messages=tuple(replace(msg, status_code=400) for msg in view_model.messages)
            )
            return self._response_adapter.adapt_error(mapped)

        try:
            if self._pipeline is not None:
                use_case_output = await self._pipeline.execute(use_case_input)
            else:
                use_case_output = await self._use_case.execute(use_case_input)
        except Exception as exc:
            if self._error_presenter is None:
                raise
            view_model = self._error_presenter.to_view_model(exc)
            mapped = self._status_mapper.map(view_model)
            return self._response_adapter.adapt_error(mapped)

        if self._unwrap_use_case_result and isinstance(use_case_output, Result):
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
