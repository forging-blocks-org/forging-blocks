# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false, reportArgumentType=false
"""Tests for the Middleware protocol."""

import pytest

from forging_blocks.presentation import Middleware
from forging_blocks.presentation.next_handler import NextHandler


class FakeRequest:
    """A simple request type used in tests."""

    def __init__(self, value: str) -> None:
        self.value = value


class FakeResponse:
    """A simple response type used in tests."""

    def __init__(self, result: str) -> None:
        self.result = result


class IdentityMiddleware(Middleware[FakeRequest, FakeResponse]):
    """Middleware that passes the request through unchanged."""

    async def process(
        self,
        request: FakeRequest,
        next_handler: NextHandler[FakeRequest, FakeResponse],
    ) -> FakeResponse:
        return await next_handler(request)


@pytest.mark.unit
class TestMiddlewareProtocol:
    """Verify that Middleware implementations satisfy the protocol."""

    def test_implementation_satisfies_protocol(self) -> None:
        middleware = IdentityMiddleware()
        assert isinstance(middleware, Middleware)
