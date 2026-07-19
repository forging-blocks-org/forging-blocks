# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for TimingMiddleware."""

import pytest

from forging_blocks.presentation.builtin.timing_middleware import TimingMiddleware
from tests.forging_blocks.presentation.builtin.conftest import (
    FakeLogger,
    FakeRequest,
    FakeResponse,
)


@pytest.mark.unit
class TestTimingMiddleware:
    """Behavioural tests for TimingMiddleware."""

    async def test_logs_elapsed_time_on_success(self) -> None:
        logger = FakeLogger()
        middleware = TimingMiddleware[FakeRequest, FakeResponse](logger)

        async def _handler(request: FakeRequest) -> FakeResponse:
            return FakeResponse(f"ok:{request.value}")

        response = await middleware.process(FakeRequest("hi"), _handler)

        assert response.result == "ok:hi"
        assert len(logger.messages) == 1
        assert logger.messages[0][0] == "Request handled in %s seconds"
        elapsed: float = float(logger.messages[0][1][0])  # type: ignore[assignment]
        assert elapsed >= 0.0

    async def test_logs_elapsed_time_on_handler_exception(self) -> None:
        logger = FakeLogger()
        middleware = TimingMiddleware[FakeRequest, FakeResponse](logger)

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise ValueError("fail")

        with pytest.raises(ValueError, match="fail"):
            await middleware.process(FakeRequest("x"), _failing)

        assert len(logger.messages) == 1
        assert logger.messages[0][0] == "Request handled in %s seconds"
        elapsed: float = float(logger.messages[0][1][0])  # type: ignore[assignment]
        assert elapsed >= 0.0
