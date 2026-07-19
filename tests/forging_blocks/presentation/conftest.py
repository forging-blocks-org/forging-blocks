# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Shared test doubles for presentation-layer tests."""

from forging_blocks.application.ports.inbound import UseCase
from forging_blocks.foundation import Error, ErrorMessage
from forging_blocks.foundation.result import Err, Ok, Result
from forging_blocks.presentation import RequestAdapter, ResponseAdapter
from forging_blocks.presentation.errors.error_view_model import ErrorViewModel


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


class NonExceptionErrorUseCase(UseCase[str, Result[str, str]]):
    """Returns Err with a plain string (not a BaseException)."""

    async def execute(self, request: str) -> Result[str, str]:
        return Err("plain error string")


class FailingRequestAdapter(RequestAdapter[DictRequest, str]):
    """Always raises — simulates an unparseable raw request."""

    def adapt(self, raw: DictRequest) -> str:
        raise TypeError("Cannot parse request")
