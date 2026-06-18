"""Standard middleware implementations for application services.

Provides common middleware for cross-cutting concerns like
logging, transaction management, validation, etc.
"""

from collections.abc import Callable
from typing import Generic, TypeVar

from forging_blocks.application.service_context import ServiceContext
from forging_blocks.infrastructure.logging.stdlib_logger import StdlibLogger

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")
TEventPayload = TypeVar("TEventPayload")

Middleware = Callable[[TRequest, ServiceContext[TEventPayload], Callable[[], TResponse]], TResponse]


async def logging_middleware(
    request: TRequest,
    context: ServiceContext[TEventPayload],
    next_handler: Callable[[], TResponse],
) -> TResponse:
    """Middleware that logs request/response information.

    Args:
        request: The incoming request.
        context: The service context.
        next_handler: The next handler in the chain.

    Returns:
        The response from the next handler.
    """
    logger = StdlibLogger("forging_blocks.application.middleware")
    logger.info("Processing request: %s", type(request).__name__)

    try:
        response = await next_handler()
        logger.info("Request completed successfully: %s", type(request).__name__)
        return response
    except Exception as e:
        logger.error("Request failed: %s - %s", type(request).__name__, str(e))
        raise


async def transaction_middleware(
    request: TRequest,
    context: ServiceContext[TEventPayload],
    next_handler: Callable[[], TResponse],
) -> TResponse:
    """Middleware that manages transaction boundaries.

    Uses the Unit of Work from the context to ensure
    atomic commit/rollback of changes.

    Args:
        request: The incoming request.
        context: The service context.
        next_handler: The next handler in the chain.

    Returns:
        The response from the next handler.
    """
    unit_of_work = context.unit_of_work

    async with unit_of_work:
        return await next_handler()


async def validation_middleware(
    request: TRequest,
    context: ServiceContext[TEventPayload],
    next_handler: Callable[[], TResponse],
) -> TResponse:
    """Middleware that validates the request before processing.

    Args:
        request: The incoming request.
        context: The service context.
        next_handler: The next handler in the chain.

    Returns:
        The response from the next handler.

    Raises:
        ValidationError: If the request fails validation.
    """
    # Check if request has a validate method
    if hasattr(request, "validate") and callable(request.validate):
        request.validate()

    return await next_handler()


class MiddlewareBuilder(Generic[TRequest, TResponse, TEventPayload]):
    """Builder for composing middleware pipelines.

    Provides a fluent API for building middleware chains.
    """

    def __init__(self) -> None:
        self._middlewares: list[Middleware[TRequest, TResponse, TEventPayload]] = []

    def add_logging(self) -> "MiddlewareBuilder[TRequest, TResponse, TEventPayload]":
        """Add logging middleware."""
        self._middlewares.append(logging_middleware)
        return self

    def add_transaction(self) -> "MiddlewareBuilder[TRequest, TResponse, TEventPayload]":
        """Add transaction middleware."""
        self._middlewares.append(transaction_middleware)
        return self

    def add_validation(self) -> "MiddlewareBuilder[TRequest, TResponse, TEventPayload]":
        """Add validation middleware."""
        self._middlewares.append(validation_middleware)
        return self

    def add(
        self, middleware: Middleware[TRequest, TResponse, TEventPayload]
    ) -> "MiddlewareBuilder[TRequest, TResponse, TEventPayload]":
        """Add a custom middleware."""
        self._middlewares.append(middleware)
        return self

    def build(self) -> list[Middleware[TRequest, TResponse, TEventPayload]]:
        """Build the middleware list."""
        return self._middlewares.copy()
