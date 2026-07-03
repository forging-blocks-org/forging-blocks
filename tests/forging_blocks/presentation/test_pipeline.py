# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for the Pipeline class."""

import pytest

from forging_blocks.presentation import Pipeline
from forging_blocks.presentation.next_handler import NextHandler


class FakeRequest:
    """A simple request type used in tests."""

    def __init__(self, value: str) -> None:
        self.value = value


class FakeResponse:
    """A simple response type used in tests."""

    def __init__(self, result: str) -> None:
        self.result = result


class IdentityMiddleware:
    """Middleware that passes the request through unchanged."""

    async def process(
        self,
        request: FakeRequest,
        next_handler: NextHandler[FakeRequest, FakeResponse],
    ) -> FakeResponse:
        return await next_handler(request)


class PrefixMiddleware:
    """Middleware that prepends a prefix to the request value."""

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix

    async def process(
        self,
        request: FakeRequest,
        next_handler: NextHandler[FakeRequest, FakeResponse],
    ) -> FakeResponse:
        modified = FakeRequest(f"[{self._prefix}]{request.value}")
        return await next_handler(modified)


class ShortCircuitMiddleware:
    """Middleware that returns a response without calling next_handler."""

    def __init__(self, fixed_result: str) -> None:
        self._fixed_result = fixed_result

    async def process(
        self,
        request: FakeRequest,
        next_handler: NextHandler[FakeRequest, FakeResponse],
    ) -> FakeResponse:
        return FakeResponse(self._fixed_result)


class RecordingMiddleware:
    """Middleware that records the order it was called."""

    def __init__(self, name: str, log: list[str]) -> None:
        self._name = name
        self._log = log

    async def process(
        self,
        request: FakeRequest,
        next_handler: NextHandler[FakeRequest, FakeResponse],
    ) -> FakeResponse:
        self._log.append(f"{self._name}:in")
        response = await next_handler(request)
        self._log.append(f"{self._name}:out")
        return response


class ExceptionMiddleware:
    """Middleware that raises an exception."""

    def __init__(self, message: str) -> None:
        self._message = message

    async def process(
        self,
        request: FakeRequest,
        next_handler: NextHandler[FakeRequest, FakeResponse],
    ) -> FakeResponse:
        raise RuntimeError(self._message)


@pytest.mark.unit
class TestPipeline:
    """Behavioural tests for Pipeline."""

    async def _handler(self, request: FakeRequest) -> FakeResponse:
        return FakeResponse(f"handled:{request.value}")

    async def test_execute_empty_pipeline_calls_handler_directly(self) -> None:
        pipeline = Pipeline([], self._handler)

        response = await pipeline.execute(FakeRequest("test"))

        assert response.result == "handled:test"

    async def test_execute_single_middleware_wraps_handler(self) -> None:
        middleware = PrefixMiddleware("pre")
        pipeline = Pipeline([middleware], self._handler)

        response = await pipeline.execute(FakeRequest("test"))

        assert response.result == "handled:[pre]test"

    async def test_execute_multiple_middleware_applied_in_order(self) -> None:
        log: list[str] = []
        first = RecordingMiddleware("first", log)
        second = RecordingMiddleware("second", log)
        third = RecordingMiddleware("third", log)
        pipeline = Pipeline([first, second, third], self._handler)

        await pipeline.execute(FakeRequest("test"))

        assert log == [
            "first:in",
            "second:in",
            "third:in",
            "third:out",
            "second:out",
            "first:out",
        ]

    async def test_execute_middleware_transforms_request_on_way_in(
        self,
    ) -> None:
        pipeline = Pipeline(
            [PrefixMiddleware("outer"), PrefixMiddleware("inner")],
            self._handler,
        )

        response = await pipeline.execute(FakeRequest("test"))

        assert response.result == "handled:[inner][outer]test"

    async def test_execute_short_circuit_skips_handler(self) -> None:
        pipeline = Pipeline([ShortCircuitMiddleware("short-circuited")], self._handler)

        response = await pipeline.execute(FakeRequest("ignored"))

        assert response.result == "short-circuited"

    async def test_execute_short_circuit_skips_downstream_middleware(
        self,
    ) -> None:
        log: list[str] = []
        pipeline = Pipeline(
            [
                ShortCircuitMiddleware("blocked"),
                RecordingMiddleware("skipped", log),
            ],
            self._handler,
        )

        response = await pipeline.execute(FakeRequest("test"))

        assert response.result == "blocked"
        assert log == []

    async def test_execute_exception_propagates_unchanged(self) -> None:
        pipeline = Pipeline([ExceptionMiddleware("boom")], self._handler)

        with pytest.raises(RuntimeError, match="boom"):
            await pipeline.execute(FakeRequest("test"))

    async def test_execute_exception_propagates_through_outer_middleware(
        self,
    ) -> None:
        log: list[str] = []
        pipeline = Pipeline(
            [
                RecordingMiddleware("outer", log),
                ExceptionMiddleware("boom"),
            ],
            self._handler,
        )

        with pytest.raises(RuntimeError, match="boom"):
            await pipeline.execute(FakeRequest("test"))

        assert log == ["outer:in"]

    async def test_middlewares_property_returns_immutable_tuple(self) -> None:
        middleware = IdentityMiddleware()
        pipeline = Pipeline([middleware], self._handler)

        result = pipeline.middlewares

        assert isinstance(result, tuple)
        assert len(result) == 1
        assert result[0] is middleware

    async def test_middlewares_property_on_empty_pipeline(self) -> None:
        pipeline = Pipeline([], self._handler)

        result = pipeline.middlewares

        assert result == ()

    async def test_identity_middleware_produces_same_result_as_handler(
        self,
    ) -> None:
        pipeline = Pipeline([IdentityMiddleware()], self._handler)

        response = await pipeline.execute(FakeRequest("direct"))

        assert response.result == "handled:direct"
