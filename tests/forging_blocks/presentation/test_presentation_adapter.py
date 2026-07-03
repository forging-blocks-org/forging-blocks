# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for PresentationAdapter, RequestAdapter, ResponseAdapter, and ErrorStatusCodeMapper."""

import pytest

from forging_blocks.application.ports.inbound import UseCase
from forging_blocks.foundation import Error, ErrorMessage
from forging_blocks.foundation.result import Err, Ok, Result
from forging_blocks.presentation import (
    ErrorPresenter,
    ErrorStatusCodeMapper,
    ErrorViewModel,
    PresentationAdapter,
    RequestAdapter,
    ResponseAdapter,
)
from forging_blocks.presentation.error_message_model import ErrorMessageModel


class DictRequest:
    """Fake transport request."""

    def __init__(self, data: dict[str, str]) -> None:
        self.data = data


class DictResponse:
    """Fake transport response."""

    def __init__(self, body: dict[str, object], status: int = 200) -> None:
        self.body = body
        self.status = status


class FakeRequestAdapter(RequestAdapter[DictRequest, str]):
    """Extracts a value from a dict request."""

    def adapt(self, raw: DictRequest) -> str:
        return raw.data["name"]


class FakeResponseAdapter(ResponseAdapter[str, DictResponse]):
    """Wraps a string result into a dict response."""

    def adapt(self, output: str) -> DictResponse:
        return DictResponse({"result": output})

    def adapt_error(self, view_model: ErrorViewModel) -> DictResponse:
        messages = [
            {
                "title": m.title,
                "status_code": m.status_code,
                "code": m.code,
            }
            for m in view_model.messages
        ]
        status = (view_model.messages[0].status_code if view_model.messages else 500) or 500
        return DictResponse({"errors": messages}, status=status)


class SuccessUseCase(UseCase[str, str]):
    """Returns the input unchanged."""

    async def execute(self, request: str) -> str:
        return f"processed:{request}"


class ResultSuccessUseCase(UseCase[str, Result[str, object]]):
    """Returns Ok(input)."""

    async def execute(self, request: str) -> Result[str, object]:
        return Ok(f"result:{request}")


class ResultErrorUseCase(UseCase[str, Result[str, Error[dict[str, object]]]]):
    """Returns Err with a framework Error."""

    async def execute(self, request: str) -> Result[str, Error[dict[str, object]]]:
        error = Error(ErrorMessage("Use case failed"))
        return Err(error)


class ExceptionUseCase(UseCase[str, str]):
    """Raises an exception."""

    async def execute(self, request: str) -> str:
        raise ValueError("Something broke")


class DomainErrorUseCase(UseCase[str, str]):
    """Raises a framework Error."""

    async def execute(self, request: str) -> str:
        raise Error(ErrorMessage("Domain rule violated"))


@pytest.mark.unit
class TestRequestAdapter:
    """Tests for RequestAdapter protocol."""

    def test_adapter_translates_raw_to_input(self) -> None:
        adapter = FakeRequestAdapter()

        result = adapter.adapt(DictRequest({"name": "Alice"}))

        assert result == "Alice"


@pytest.mark.unit
class TestResponseAdapter:
    """Tests for ResponseAdapter protocol."""

    def test_adapter_translates_output_to_response(self) -> None:
        adapter = FakeResponseAdapter()

        result = adapter.adapt("hello")

        assert result.body == {"result": "hello"}
        assert result.status == 200

    def test_adapt_error_translates_view_model_to_response(self) -> None:
        adapter = FakeResponseAdapter()
        msg = ErrorMessageModel(title="Not found", code="NotFound", status_code=404)
        view_model = ErrorViewModel(messages=[msg])

        result = adapter.adapt_error(view_model)

        assert result.status == 404
        assert result.body == {
            "errors": [{"title": "Not found", "status_code": 404, "code": "NotFound"}]
        }


@pytest.mark.unit
class TestErrorStatusCodeMapper:
    """Tests for ErrorStatusCodeMapper."""

    def test_maps_validation_error_to_400(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Invalid", code="ValidationError")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 400

    def test_maps_rule_violation_to_409(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Conflict", code="RuleViolationError")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 409

    def test_maps_combined_errors_to_422(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Multiple", code="CombinedErrors")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 422

    def test_maps_unknown_code_to_500(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="Boom", code="SomethingElse")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 500

    def test_maps_none_code_to_500(self) -> None:
        mapper = ErrorStatusCodeMapper()
        msg = ErrorMessageModel(title="No code")
        view_model = ErrorViewModel(messages=[msg])

        result = mapper.map(view_model)

        assert result.messages[0].status_code == 500


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
