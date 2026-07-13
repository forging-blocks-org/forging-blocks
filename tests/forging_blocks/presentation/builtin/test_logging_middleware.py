# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for LoggingMiddleware."""

import pytest

from forging_blocks.presentation.builtin.logging_middleware import LoggingMiddleware


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


async def _echo_handler(request: _FakeRequest) -> _FakeResponse:
    return _FakeResponse(f"echo:{request.value}")


@pytest.mark.unit
class TestLoggingMiddleware:
    """Behavioural tests for LoggingMiddleware."""

    async def test_logs_request_and_response_at_debug_level(self) -> None:
        logger = _FakeLogger()
        middleware: LoggingMiddleware[_FakeRequest, _FakeResponse] = LoggingMiddleware(logger)

        response = await middleware.process(_FakeRequest("hello"), _echo_handler)

        assert response.result == "echo:hello"
        assert len(logger.messages) == 2
        # First message — request
        assert logger.messages[0][0] == "Processing request: %s"
        assert logger.messages[0][1][0].value == "hello"  # type: ignore[reportAttributeAccessIssue]
        # Second message — response
        assert logger.messages[1][0] == "Request processed, response: %s"
        assert logger.messages[1][1][0].result == "echo:hello"  # type: ignore[reportAttributeAccessIssue]

    async def test_does_not_catch_handler_exception(self) -> None:
        logger = _FakeLogger()
        middleware: LoggingMiddleware[_FakeRequest, _FakeResponse] = LoggingMiddleware(logger)

        async def _failing(_request: _FakeRequest) -> _FakeResponse:
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            await middleware.process(_FakeRequest("x"), _failing)

        # Only the request log should have been emitted
        assert len(logger.messages) == 1
        assert logger.messages[0][0] == "Processing request: %s"
