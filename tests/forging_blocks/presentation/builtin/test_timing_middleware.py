# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for TimingMiddleware."""

import pytest

from forging_blocks.presentation.builtin.timing_middleware import TimingMiddleware


class _FakeLogger:
    """LoggerPort stub that captures logged messages."""

    def __init__(self) -> None:
        self.messages: list[tuple[str, tuple[object, ...]]] = []

    def debug(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))

    def info(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))

    def warning(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))

    def error(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))


class _FakeRequest:
    def __init__(self, value: str) -> None:
        self.value = value


class _FakeResponse:
    def __init__(self, result: str) -> None:
        self.result = result


@pytest.mark.unit
class TestTimingMiddleware:
    """Behavioural tests for TimingMiddleware."""

    async def test_logs_elapsed_time_on_success(self) -> None:
        logger = _FakeLogger()
        middleware: TimingMiddleware[_FakeRequest, _FakeResponse] = TimingMiddleware(logger)

        async def _handler(request: _FakeRequest) -> _FakeResponse:
            return _FakeResponse(f"ok:{request.value}")

        response = await middleware.process(_FakeRequest("hi"), _handler)

        assert response.result == "ok:hi"
        assert len(logger.messages) == 1
        assert logger.messages[0][0] == "Request handled in %.4f seconds"
        elapsed: float = logger.messages[0][1][0]  # type: ignore[assignment]
        assert elapsed >= 0.0

    async def test_logs_elapsed_time_on_handler_exception(self) -> None:
        logger = _FakeLogger()
        middleware: TimingMiddleware[_FakeRequest, _FakeResponse] = TimingMiddleware(logger)

        async def _failing(_request: _FakeRequest) -> _FakeResponse:
            raise ValueError("fail")

        with pytest.raises(ValueError, match="fail"):
            await middleware.process(_FakeRequest("x"), _failing)

        # Timing should still be logged in the finally block
        assert len(logger.messages) == 1
        assert logger.messages[0][0] == "Request handled in %.4f seconds"
        elapsed: float = logger.messages[0][1][0]  # type: ignore[assignment]
        assert elapsed >= 0.0
