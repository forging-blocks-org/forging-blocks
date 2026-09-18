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
from typing import TYPE_CHECKING, NoReturn, cast

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

    Example:
        ```python
        adapter = PresentationAdapter(
            use_case=create_order_use_case,
            request_adapter=JsonRequestAdapter(),
            response_adapter=JsonResponseAdapter(),
            error_presenter=ErrorPresenter(),
        )
        response = await adapter.handle(http_request)
        ```
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

    def _adapt_request(self, raw_request: RawRequest) -> UseCaseInput:
        return self._request_adapter.adapt(raw_request)

    def _handle_request_adaptation_error(self, exc: Exception) -> RawResponse:
        if self._error_presenter is None:
            raise exc
        view_model = self._error_presenter.to_view_model(exc)
        mapped = ErrorViewModel(
            messages=tuple(replace(msg, status_code=400) for msg in view_model.messages)
        )
        return self._response_adapter.adapt_error(mapped)

    async def _execute_use_case(self, use_case_input: UseCaseInput) -> UseCaseOutput:
        if self._pipeline is not None:
            return await self._pipeline.execute(use_case_input)
        return await self._use_case.execute(use_case_input)

    def _handle_execution_error(self, exc: Exception) -> RawResponse:
        if self._error_presenter is None:
            raise exc
        view_model = self._error_presenter.to_view_model(exc)
        mapped = self._status_mapper.map(view_model)
        return self._response_adapter.adapt_error(mapped)

    def _should_unwrap_result(self, output: object) -> bool:
        return self._unwrap_use_case_result and isinstance(output, Result)

    def _raise_unpresented_error(self, error_value: object) -> NoReturn:
        if isinstance(error_value, BaseException):
            raise error_value
        raise RuntimeError(str(error_value))

    def _handle_err_result(self, error_value: object) -> RawResponse:
        if self._error_presenter is None:
            self._raise_unpresented_error(error_value)
        view_model = self._error_presenter.to_view_model(error_value)
        mapped = self._status_mapper.map(view_model)
        return self._response_adapter.adapt_error(mapped)

    def _handle_result_output(self, result: Result[UseCaseOutput, object]) -> RawResponse:
        if result.is_err:
            return self._handle_err_result(result.error)
        return self._response_adapter.adapt(result.value)

    def _handle_use_case_output(
        self, output: UseCaseOutput | Result[UseCaseOutput, object]
    ) -> RawResponse:
        if self._should_unwrap_result(output):
            return self._handle_result_output(cast("Result[UseCaseOutput, object]", output))
        return self._response_adapter.adapt(cast(UseCaseOutput, output))

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
            use_case_input = self._adapt_request(raw_request)
        except Exception as exc:
            return self._handle_request_adaptation_error(exc)

        try:
            use_case_output = await self._execute_use_case(use_case_input)
        except Exception as exc:
            return self._handle_execution_error(exc)

        return self._handle_use_case_output(use_case_output)
