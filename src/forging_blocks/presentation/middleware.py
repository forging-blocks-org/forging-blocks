"""Protocol for middleware interceptors in the presentation layer.

``Middleware`` defines the contract for cross-cutting interceptors that
sit between the adapter and the application handler. Each middleware
may inspect, transform, or short-circuit the request before delegating
to the next handler in the chain.
"""

from typing import Protocol, runtime_checkable

from forging_blocks.presentation.next_handler import NextHandler


@runtime_checkable
class Middleware[RequestType, ResponseType](Protocol):
    """Structural protocol for a middleware interceptor.

    Implementations must not depend on infrastructure details.
    Middleware is exclusively a composition primitive — it does not
    extend ``Port`` because its shape ``(request, next_handler) ->
    response`` differs from the single-input, single-output port
    contract.

    Short-circuiting is supported: a middleware may return a response
    without calling *next_handler*, skipping all downstream middleware
    and the terminal handler.
    """

    async def process(
        self,
        request: RequestType,
        next_handler: NextHandler[RequestType, ResponseType],
    ) -> ResponseType:
        """Intercept *request* and optionally delegate to *next_handler*.

        Args:
            request: The incoming request to process.
            next_handler: The next callable in the pipeline chain.
                Must be called to continue processing. If not called,
                the chain short-circuits and this method's return
                value becomes the final response.

        Returns:
            The response after processing.
        """
        ...
