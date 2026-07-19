# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for ErrorHandlingMiddleware."""

import pytest

from forging_blocks.presentation.builtin.error_handling_middleware import ErrorHandlingMiddleware
from tests.forging_blocks.presentation.builtin.conftest import (
    FakeLogger,
    FakeRequest,
    FakeResponse,
)


async def _echo_handler(request: FakeRequest) -> FakeResponse:
    return FakeResponse(f"echo:{request.value}")


@pytest.mark.unit
class TestErrorHandlingMiddleware:
    """Behavioural tests for ErrorHandlingMiddleware."""

    async def test_passes_through_on_success(self) -> None:
        """Response passes through unchanged; on_error is never called."""
        on_error_called: list[object] = []

        def _on_error(view_model: object) -> FakeResponse:
            on_error_called.append(view_model)
            return FakeResponse("error")

        middleware = ErrorHandlingMiddleware[FakeRequest, FakeResponse](_on_error)
        response = await middleware.process(FakeRequest("hello"), _echo_handler)

        assert response.result == "echo:hello"
        assert len(on_error_called) == 0

    async def test_catches_exception_and_maps_through_error_presenter(self) -> None:
        """Handler raises ValueError; middleware catches, maps, returns error response."""
        caught_view_models: list[object] = []

        def _on_error(view_model: object) -> FakeResponse:
            caught_view_models.append(view_model)
            return FakeResponse("mapped-error")

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise ValueError("bad")

        middleware = ErrorHandlingMiddleware[FakeRequest, FakeResponse](_on_error)
        response = await middleware.process(FakeRequest("x"), _failing)

        assert response.result == "mapped-error"
        assert len(caught_view_models) == 1
        assert len(caught_view_models[0].messages) >= 1  # type: ignore[reportAttributeAccessIssue]
        assert caught_view_models[0].messages[0].title == "bad"  # type: ignore[reportAttributeAccessIssue]

    async def test_logs_exception_when_logger_provided(self) -> None:
        """When a logger is provided, the exception is logged at error level."""
        logger = FakeLogger()
        caught_view_models: list[object] = []

        def _on_error(view_model: object) -> FakeResponse:
            caught_view_models.append(view_model)
            return FakeResponse("mapped-error")

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise ValueError("logged-failure")

        middleware = ErrorHandlingMiddleware[FakeRequest, FakeResponse](
            _on_error,
            logger=logger,
        )
        response = await middleware.process(FakeRequest("x"), _failing)

        assert response.result == "mapped-error"
        assert len(logger.messages) == 1
        assert logger.messages[0][0] == "Unhandled exception in pipeline: %s"
        assert logger.messages[0][1][0] == "logged-failure"

    async def test_does_not_log_when_logger_is_none(self) -> None:
        """When logger is None (default), no crash occurs and no logging happens."""

        def _on_error(view_model: object) -> FakeResponse:
            return FakeResponse("mapped-error")

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise ValueError("silent-failure")

        middleware = ErrorHandlingMiddleware[FakeRequest, FakeResponse](_on_error)
        response = await middleware.process(FakeRequest("x"), _failing)

        assert response.result == "mapped-error"

    async def test_does_not_catch_base_exception(self) -> None:
        """KeyboardInterrupt propagates; it is not caught by the middleware."""

        def _on_error(view_model: object) -> FakeResponse:
            pytest.fail("on_error should not be called for BaseException")

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise KeyboardInterrupt

        middleware = ErrorHandlingMiddleware[FakeRequest, FakeResponse](_on_error)

        with pytest.raises(KeyboardInterrupt):
            await middleware.process(FakeRequest("x"), _failing)

    async def test_uses_default_error_presenter_when_none_passed(self) -> None:
        """When error_presenter=None, a default ErrorPresenter() is used."""

        def _on_error(view_model: object) -> FakeResponse:
            return FakeResponse("mapped-error")

        async def _failing(_request: FakeRequest) -> FakeResponse:
            raise ValueError("default-presenter")

        middleware = ErrorHandlingMiddleware[FakeRequest, FakeResponse](
            _on_error,
            error_presenter=None,
        )
        response = await middleware.process(FakeRequest("x"), _failing)

        assert response.result == "mapped-error"
