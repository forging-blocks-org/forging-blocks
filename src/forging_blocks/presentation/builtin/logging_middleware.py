"""Middleware that logs each request before and after delegation."""

from forging_blocks.application.ports.outbound.logger_port import LoggerPort
from forging_blocks.presentation.middleware.middleware import Middleware
from forging_blocks.presentation.middleware.next_handler import NextHandler


class LoggingMiddleware[RequestType, ResponseType](Middleware[RequestType, ResponseType]):
    """Logs each request before delegation and the response after.

    Responsibilities:
        - Log the incoming request at debug level.
        - Delegate to the next handler unchanged.
        - Log the outgoing response at debug level.

    Non-Responsibilities:
        - Transform the request or response.
        - Handle errors raised by downstream middleware or the handler.
        - Measure execution time — use ``TimingMiddleware`` for that.
        - Sanitize sensitive data — requests and responses are logged
          via ``str()`` as-is. If your domain objects carry tokens,
          passwords, or PII, wrap this middleware with a sanitizing
          decorator or pass a ``LoggerPort`` that performs redaction.
    Example:
        >>> from forging_blocks.application.ports.outbound.logger_port import LoggerPort
        >>> from forging_blocks.presentation.builtin import LoggingMiddleware
        >>>
        >>> mw = LoggingMiddleware[MyRequest, MyResponse](logger=my_logger)
        >>> response = await mw.process(request, next_handler)
        >>> # Logs "Processing request: ..." and "Request processed, response: ..." at debug
    """

    __slots__ = ("_logger",)

    def __init__(self, logger: LoggerPort) -> None:
        """Wrap *logger* so every request is traced.

        Args:
            logger: A ``LoggerPort`` used for debug-level tracing.
        """
        self._logger = logger

    async def process(
        self,
        request: RequestType,
        next_handler: NextHandler[RequestType, ResponseType],
    ) -> ResponseType:
        """Log the request, delegate, then log the response.

        Args:
            request: The incoming request.
            next_handler: The next callable in the pipeline chain.

        Returns:
            The response produced by the downstream handler.
        """
        self._logger.debug("Processing request: %s", str(request))
        response = await next_handler(request)
        self._logger.debug("Request processed, response: %s", str(response))
        return response
