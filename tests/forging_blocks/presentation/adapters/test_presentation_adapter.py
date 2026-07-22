# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for PresentationAdapter orchestrator."""

import pytest
from tests.forging_blocks.presentation.conftest import (
    DictRequest,
    DictResponse,
    DomainErrorUseCase,
    ExceptionUseCase,
    FailingRequestAdapter,
    FakeRequestAdapter,
    FakeResponseAdapter,
    NonExceptionErrorUseCase,
    ResultErrorUseCase,
    ResultSuccessUseCase,
    SuccessUseCase,
)

from forging_blocks.application.ports.inbound import UseCasePort
from forging_blocks.foundation import Error
from forging_blocks.foundation.result import Ok
from forging_blocks.presentation import (
    ErrorPresenter,
    NextHandler,
    Pipeline,
    PresentationAdapter,
)


@pytest.mark.unit
class TestPresentationAdapter:
    """Integration tests for PresentationAdapter orchestrator."""

    def _make_adapter(
        self,
        use_case: UseCasePort[str, object],
        error_presenter: ErrorPresenter | None = None,
        unwrap_use_case_result: bool = True,
    ) -> PresentationAdapter[DictRequest, str, object, DictResponse]:
        return PresentationAdapter(
            use_case=use_case,
            request_adapter=FakeRequestAdapter(),
            response_adapter=FakeResponseAdapter(),
            error_presenter=error_presenter,
            unwrap_use_case_result=unwrap_use_case_result,
        )

    async def test_handle_success_with_plain_output(self) -> None:
        adapter: PresentationAdapter[DictRequest, str, str, DictResponse] = PresentationAdapter(
            use_case=SuccessUseCase(),
            request_adapter=FakeRequestAdapter(),
            response_adapter=FakeResponseAdapter(),
            error_presenter=ErrorPresenter(),
        )
        response = await adapter.handle(DictRequest({"name": "Alice"}))
        assert response.body == {"result": "processed:Alice"}

    async def test_handle_success_with_result_ok(self) -> None:
        adapter = self._make_adapter(ResultSuccessUseCase())
        response = await adapter.handle(DictRequest({"name": "Alice"}))
        assert response.body == {"result": "result:Alice"}

    async def test_handle_result_error_maps_through_error_presenter(
        self,
    ) -> None:
        adapter = self._make_adapter(
            ResultErrorUseCase(),
            error_presenter=ErrorPresenter(),
        )
        response = await adapter.handle(DictRequest({"name": "test"}))
        errors = response.body["errors"]
        assert isinstance(errors, list)
        assert len(errors) == 1

    async def test_handle_exception_maps_through_error_presenter(
        self,
    ) -> None:
        adapter = self._make_adapter(
            ExceptionUseCase(),
            error_presenter=ErrorPresenter(),
        )
        response = await adapter.handle(DictRequest({"name": "test"}))
        assert response.status == 500

    async def test_handle_domain_error_maps_through_error_presenter(
        self,
    ) -> None:
        adapter = self._make_adapter(
            DomainErrorUseCase(),
            error_presenter=ErrorPresenter(),
        )
        response = await adapter.handle(DictRequest({"name": "test"}))
        assert response.status == 500

    async def test_handle_exception_without_error_presenter_propagates(
        self,
    ) -> None:
        adapter = self._make_adapter(ExceptionUseCase())
        with pytest.raises(ValueError, match="Something broke"):
            await adapter.handle(DictRequest({"name": "test"}))

    async def test_handle_result_error_without_error_presenter_raises(
        self,
    ) -> None:
        adapter = self._make_adapter(ResultErrorUseCase())
        with pytest.raises(Error):
            await adapter.handle(DictRequest({"name": "test"}))

    async def test_handle_with_pipeline_invokes_middleware(self) -> None:
        """Middleware in the pipeline should transform the request before use case."""
        call_log: list[str] = []

        class _RecordingMiddleware:
            async def process(
                self,
                request: str,
                next_handler: NextHandler[str, str],
            ) -> str:
                call_log.append("mw:in")
                result = await next_handler(f"[mw]{request}")
                call_log.append("mw:out")
                return result

        pipeline: Pipeline[str, str] = Pipeline(
            middlewares=[_RecordingMiddleware()],
            handler=SuccessUseCase().execute,
        )
        adapter = PresentationAdapter(
            use_case=SuccessUseCase(),
            request_adapter=FakeRequestAdapter(),
            response_adapter=FakeResponseAdapter(),
            pipeline=pipeline,
        )

        response = await adapter.handle(DictRequest({"name": "Alice"}))

        assert response.body == {"result": "processed:[mw]Alice"}
        assert call_log == ["mw:in", "mw:out"]

    async def test_handle_with_unwrap_disabled_passes_result_through(self) -> None:
        """When unwrap_use_case_result=False, the Result is passed to the
        response adapter unmodified."""
        adapter = self._make_adapter(ResultSuccessUseCase(), unwrap_use_case_result=False)

        response = await adapter.handle(DictRequest({"name": "Alice"}))

        assert response.body == {"result": Ok("result:Alice")}

    async def test_handle_request_adapter_failure_returns_400(self) -> None:
        """When the request adapter raises, the error response has status 400."""
        adapter = PresentationAdapter(
            use_case=SuccessUseCase(),
            request_adapter=FakeRequestAdapter(),
            response_adapter=FakeResponseAdapter(),
            error_presenter=ErrorPresenter(),
        )

        response = await adapter.handle(DictRequest({}))  # Missing "name" key

        assert response.status == 400

    async def test_handle_request_adapter_failure_without_error_presenter_propagates(
        self,
    ) -> None:
        """Without an error presenter, request-adapter failures propagate as raw exceptions."""
        adapter = PresentationAdapter(
            use_case=SuccessUseCase(),
            request_adapter=FailingRequestAdapter(),
            response_adapter=FakeResponseAdapter(),
            error_presenter=None,
        )

        with pytest.raises(TypeError, match="Cannot parse request"):
            await adapter.handle(DictRequest({"name": "test"}))

    async def test_handle_non_exception_result_error_without_error_presenter_wraps_in_runtime_error(
        self,
    ) -> None:
        """Without an error presenter, Result.Err with a non-exception error wraps in RuntimeError."""
        adapter = self._make_adapter(
            NonExceptionErrorUseCase(),
            error_presenter=None,
        )

        with pytest.raises(RuntimeError, match="plain error string"):
            await adapter.handle(DictRequest({"name": "test"}))
