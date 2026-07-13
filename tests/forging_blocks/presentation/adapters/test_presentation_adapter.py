# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for PresentationAdapter orchestrator."""

import pytest
from tests.forging_blocks.presentation.conftest import (
    DictRequest,
    DictResponse,
    DomainErrorUseCase,
    ExceptionUseCase,
    FakeRequestAdapter,
    FakeResponseAdapter,
    ResultErrorUseCase,
    ResultSuccessUseCase,
    SuccessUseCase,
)

from forging_blocks.application.ports.inbound import UseCase
from forging_blocks.foundation import Error
from forging_blocks.presentation import (
    ErrorPresenter,
    Pipeline,
    PresentationAdapter,
)


@pytest.mark.unit
class TestPresentationAdapter:
    """Integration tests for PresentationAdapter orchestrator."""

    def _make_adapter(
        self,
        use_case: UseCase[str, object],
        error_presenter: ErrorPresenter | None = None,
    ) -> PresentationAdapter[DictRequest, str, object, DictResponse]:
        return PresentationAdapter(
            use_case=use_case,
            request_adapter=FakeRequestAdapter(),
            response_adapter=FakeResponseAdapter(),
            error_presenter=error_presenter,
        )

    async def test_handle_success_with_plain_output(self) -> None:
        adapter: PresentationAdapter[DictRequest, str, str, DictResponse] = PresentationAdapter(
            use_case=SuccessUseCase(),
            request_adapter=FakeRequestAdapter(),
            response_adapter=FakeResponseAdapter(),
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

        assert response.status == 500
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
                next_handler: object,
            ) -> str:
                call_log.append("mw:in")
                result = await next_handler(f"[mw]{request}")  # type: ignore[misc]
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
