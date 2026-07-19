# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for ValidationMiddleware."""

import pytest

from forging_blocks.presentation.builtin.validation_middleware import ValidationMiddleware
from tests.forging_blocks.presentation.builtin.conftest import (
    FakeRequest,
    FakeResponse,
)


async def _echo_handler(request: FakeRequest) -> FakeResponse:
    return FakeResponse(f"echo:{request.value}")


@pytest.mark.unit
class TestValidationMiddleware:
    """Behavioural tests for ValidationMiddleware."""

    async def test_passes_through_when_validator_returns_none(self) -> None:
        """The downstream handler is called and its response returned."""
        validator_called: list[FakeRequest] = []

        def _validator(request: FakeRequest) -> FakeResponse | None:
            validator_called.append(request)
            return None

        middleware = ValidationMiddleware[FakeRequest, FakeResponse](_validator)
        response = await middleware.process(FakeRequest("hello"), _echo_handler)

        assert response.result == "echo:hello"
        assert len(validator_called) == 1
        assert validator_called[0].value == "hello"

    async def test_short_circuits_when_validator_returns_response(self) -> None:
        """The downstream handler is skipped; the validator's response is returned."""
        handler_called: list[FakeRequest] = []

        async def _tracking_handler(request: FakeRequest) -> FakeResponse:
            handler_called.append(request)
            return FakeResponse("should-not-reach")

        error_response = FakeResponse("validation-failed")

        def _validator(request: FakeRequest) -> FakeResponse | None:
            return error_response

        middleware = ValidationMiddleware[FakeRequest, FakeResponse](_validator)
        response = await middleware.process(FakeRequest("bad"), _tracking_handler)

        assert response is error_response
        assert len(handler_called) == 0

    async def test_does_not_catch_handler_exception(self) -> None:
        """Exceptions from the downstream handler propagate."""

        def _validator(request: FakeRequest) -> FakeResponse | None:
            return None

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise RuntimeError("boom")

        middleware = ValidationMiddleware[FakeRequest, FakeResponse](_validator)

        with pytest.raises(RuntimeError, match="boom"):
            await middleware.process(FakeRequest("x"), _failing)
