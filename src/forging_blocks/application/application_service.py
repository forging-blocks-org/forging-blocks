"""Application service with middleware support.

Provides a base class for application services that can execute
use cases with middleware pipeline support.
"""

from abc import ABC
from collections.abc import Callable
from typing import Generic, TypeVar

from forging_blocks.application.ports.inbound.use_case import UseCase
from forging_blocks.application.service_context import ServiceContext

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")
TEventPayload = TypeVar("TEventPayload")

Middleware = Callable[[TRequest, ServiceContext[TEventPayload], Callable[[], TResponse]], TResponse]


class ApplicationService(Generic[TEventPayload], ABC):
    """Base class for application services with middleware support.

    Application services orchestrate use cases and provide a middleware
    pipeline for cross-cutting concerns like logging, validation,
    transaction management, etc.
    """

    def __init__(self, context: ServiceContext[TEventPayload]) -> None:
        """Initialize the application service.

        Args:
            context: The service context containing dependencies.
        """
        self._context = context
        self._middlewares: list[Middleware[TRequest, TResponse, TEventPayload]] = []

    @property
    def context(self) -> ServiceContext[TEventPayload]:
        """Get the service context."""
        return self._context

    def add_middleware(self, middleware: Middleware[TRequest, TResponse, TEventPayload]) -> None:
        """Add a middleware to the pipeline.

        Middlewares are executed in the order they are added.

        Args:
            middleware: A callable that takes (request, context, next) and returns a response.
        """
        self._middlewares.append(middleware)

    async def execute(self, use_case: UseCase[TRequest, TResponse], request: TRequest) -> TResponse:
        """Execute a use case through the middleware pipeline.

        Args:
            use_case: The use case to execute.
            request: The request to process.

        Returns:
            The response from the use case.
        """

        async def execute_use_case() -> TResponse:
            return await use_case.execute(request)

        # Build the middleware chain
        chain: Callable[[], TResponse] = execute_use_case
        for middleware in reversed(self._middlewares):
            next_chain = chain

            async def make_chain(
                mw: Middleware[TRequest, TResponse, TEventPayload], nxt: Callable[[], TResponse]
            ) -> Callable[[], TResponse]:
                async def chained() -> TResponse:
                    return await mw(request, self._context, nxt)

                return chained

            chain = await make_chain(middleware, next_chain)

        return await chain()


class MiddlewarePipeline(Generic[TRequest, TResponse, TEventPayload]):
    """Middleware pipeline for application services.

    Allows composing multiple middlewares into a single callable.
    """

    def __init__(self) -> None:
        self._middlewares: list[Middleware[TRequest, TResponse, TEventPayload]] = []

    def add(
        self, middleware: Middleware[TRequest, TResponse, TEventPayload]
    ) -> "MiddlewarePipeline[TRequest, TResponse, TEventPayload]":
        """Add a middleware to the pipeline."""
        self._middlewares.append(middleware)
        return self

    async def execute(
        self,
        request: TRequest,
        context: ServiceContext[TEventPayload],
        handler: Callable[[], TResponse],
    ) -> TResponse:
        """Execute the middleware pipeline.

        Args:
            request: The request to process.
            context: The service context.
            handler: The final handler to execute.

        Returns:
            The response from the handler.
        """
        chain: Callable[[], TResponse] = handler
        for middleware in reversed(self._middlewares):
            next_chain = chain

            async def make_chain(
                mw: Middleware[TRequest, TResponse, TEventPayload], nxt: Callable[[], TResponse]
            ) -> Callable[[], TResponse]:
                async def chained() -> TResponse:
                    return await mw(request, context, nxt)

                return chained

            chain = await make_chain(middleware, next_chain)

        return await chain()
