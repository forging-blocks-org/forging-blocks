# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for LoggingMiddleware."""

import pytest

from forging_blocks.presentation.builtin.logging_middleware import LoggingMiddleware
from tests.forging_blocks.presentation.builtin.conftest import (
    FakeLogger,
    FakeRequest,
    FakeResponse,
)


async def _echo_handler(request: FakeRequest) -> FakeResponse:
    return FakeResponse(f"echo:{request.value}")


@pytest.mark.unit
class TestLoggingMiddleware:
    """Behavioural tests for LoggingMiddleware."""

    async def test_logs_request_and_response_at_debug_level(self) -> None:
        logger = FakeLogger()
        middleware = LoggingMiddleware[FakeRequest, FakeResponse](logger)

        response = await middleware.process(FakeRequest("hello"), _echo_handler)

        assert response.result == "echo:hello"
        assert len(logger.messages) == 2
        assert logger.messages[0][0] == "Processing request: %s"
        assert logger.messages[0][1][0].value == "hello"  # type: ignore[reportAttributeAccessIssue]
        assert logger.messages[1][0] == "Request processed, response: %s"
        assert logger.messages[1][1][0].result == "echo:hello"  # type: ignore[reportAttributeAccessIssue]

    async def test_does_not_catch_handler_exception(self) -> None:
        logger = FakeLogger()
        middleware = LoggingMiddleware[FakeRequest, FakeResponse](logger)

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            await middleware.process(FakeRequest("x"), _failing)

        assert len(logger.messages) == 1
        assert logger.messages[0][0] == "Processing request: %s"
