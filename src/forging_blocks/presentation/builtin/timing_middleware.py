"""Middleware that records wall-clock execution time of the downstream pipeline."""

import time

from forging_blocks.application.ports.outbound.logger_port import LoggerPort
from forging_blocks.presentation.middleware.middleware import Middleware
from forging_blocks.presentation.middleware.next_handler import NextHandler


class TimingMiddleware[RequestType, ResponseType](Middleware[RequestType, ResponseType]):
    """Measures and logs the wall-clock time of downstream execution.

    Uses ``time.monotonic()`` so measurements are unaffected by system
    clock adjustments.  Timing is reported at info level *after* the
    handler returns, even when the handler raises an exception (the
    elapsed time is logged in a ``finally`` block).

    Responsibilities:
        - Record the elapsed wall-clock time for the downstream handler.
        - Log the elapsed time at info level.
        - Report timing even when the handler raises.

    Non-Responsibilities:
        - Transform the request or response.
        - Handle errors raised downstream.
    """

    __slots__ = ("_logger",)

    def __init__(self, logger: LoggerPort) -> None:
        """Wrap *logger* so every request is timed.

        Args:
            logger: A ``LoggerPort`` used for info-level timing messages.
        """
        self._logger = logger

    async def process(
        self,
        request: RequestType,
        next_handler: NextHandler[RequestType, ResponseType],
    ) -> ResponseType:
        """Delegate to *next_handler* and log the elapsed time.

        Args:
            request: The incoming request.
            next_handler: The next callable in the pipeline chain.

        Returns:
            The response produced by the downstream handler.
        """
        start = time.monotonic()
        try:
            return await next_handler(request)
        finally:
            elapsed = time.monotonic() - start
            self._logger.info("Request handled in %s seconds", f"{elapsed:.4f}")
