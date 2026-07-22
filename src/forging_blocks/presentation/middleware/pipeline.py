"""Immutable middleware pipeline that composes interceptors into a
single executable chain.

``Pipeline`` is assembled once at wiring time and executed repeatedly
thereafter. Middleware is applied right-to-left so that the first
element in the list is the outermost wrapper — it executes first on
the way in and last on the way out.
"""

from collections.abc import Awaitable, Callable, Sequence

from forging_blocks.presentation.middleware.middleware import Middleware


class Pipeline[RequestType, ResponseType]:
    """Composes a sequence of middleware around a terminal handler.

    Usage::

        async def handler(req: MyRequest) -> MyResponse:
            return MyResponse(...)


        pipeline = Pipeline([logging_mw, auth_mw, metrics_mw], handler)
        response = await pipeline.execute(request)
    """

    __slots__ = ("_middlewares", "_handler", "_chain")

    def __init__(
        self,
        middlewares: Sequence[Middleware[RequestType, ResponseType]],
        handler: Callable[[RequestType], Awaitable[ResponseType]],
    ) -> None:
        """Build the pipeline from *middlewares* and a terminal *handler*.

        Middleware is stored as an immutable tuple internally and
        composed right-to-left into a single callable chain. The
        chain is pre-built during construction so that each call to
        ``execute`` is a single delegation.

        Args:
            middlewares: Ordered sequence of middleware to compose.
                The first element wraps all subsequent elements.
            handler: The terminal handler invoked after all middleware
                has delegated.

        """
        self._middlewares: tuple[Middleware[RequestType, ResponseType], ...] = tuple(middlewares)
        self._handler = handler
        self._chain = self._build_chain()

    async def execute(self, request: RequestType) -> ResponseType:
        """Execute the pipeline by delegating to the pre-built chain.

        Args:
            request: The request to process through the pipeline.

        Returns:
            The response produced by the terminal handler (possibly
            transformed by middleware on the way out).

        """
        return await self._chain(request)

    @property
    def middlewares(
        self,
    ) -> tuple[Middleware[RequestType, ResponseType], ...]:
        """The immutable sequence of middleware in this pipeline."""
        return self._middlewares

    def _build_chain(
        self,
    ) -> Callable[[RequestType], Awaitable[ResponseType]]:
        chain: Callable[[RequestType], Awaitable[ResponseType]] = self._handler
        for middleware in reversed(self._middlewares):
            chain = _wrap(middleware, chain)
        return chain


def _wrap[RequestType, ResponseType](
    middleware: Middleware[RequestType, ResponseType],
    next_handler: Callable[[RequestType], Awaitable[ResponseType]],
) -> Callable[[RequestType], Awaitable[ResponseType]]:
    """Wrap *next_handler* inside *middleware* so the middleware
    executes first on the way in and *next_handler* executes after
    it on the way out.
    """

    async def wrapped(request: RequestType) -> ResponseType:
        return await middleware.process(request, next_handler)

    return wrapped
