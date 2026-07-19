"""Middleware that catches unhandled exceptions and maps them to error responses."""

from collections.abc import Callable

from forging_blocks.application.ports.outbound.logger_port import LoggerPort
from forging_blocks.presentation.errors.error_presenter import ErrorPresenter
from forging_blocks.presentation.errors.error_view_model import ErrorViewModel
from forging_blocks.presentation.middleware.middleware import Middleware
from forging_blocks.presentation.middleware.next_handler import NextHandler


class ErrorHandlingMiddleware[RequestType, ResponseType](Middleware[RequestType, ResponseType]):
    """Catches exceptions from downstream and maps them to responses.

    Wraps the downstream handler in a try/except that catches
    ``Exception`` (not ``BaseException`` — ``KeyboardInterrupt``,
    ``SystemExit`` and friends propagate).  Caught exceptions are
    converted to an ``ErrorViewModel`` via ``ErrorPresenter`` and then
    mapped to a ``ResponseType`` by the required ``on_error`` callable.

    An optional ``LoggerPort`` logs the exception at error level before
    mapping.

    Responsibilities:
        - Catch ``Exception`` raised by the downstream handler.
        - Convert the exception to an ``ErrorViewModel``.
        - Map the view model to a ``ResponseType`` via ``on_error``.
        - Optionally log the exception before mapping.

    Non-Responsibilities:
        - Catch ``BaseException`` (``KeyboardInterrupt``, ``SystemExit``).
        - Define the error response shape — that lives in ``on_error``.
        - Handle errors from middleware upstream of this one.
    """

    __slots__ = ("_error_presenter", "_on_error", "_logger")

    def __init__(
        self,
        on_error: Callable[[ErrorViewModel], ResponseType],
        error_presenter: ErrorPresenter | None = None,
        logger: LoggerPort | None = None,
    ) -> None:
        """Wrap the pipeline with exception-to-response mapping.

        Args:
            on_error: Required callable that maps an ``ErrorViewModel``
                to a ``ResponseType`` (e.g. ``response_adapter.adapt_error``).
            error_presenter: The ``ErrorPresenter`` used to convert
                exceptions into view models.  Defaults to a fresh
                ``ErrorPresenter()`` when omitted.
            logger: An optional ``LoggerPort``.  When provided, caught
                exceptions are logged at error level before mapping.
        """
        self._on_error = on_error
        self._error_presenter = error_presenter if error_presenter is not None else ErrorPresenter()
        self._logger = logger

    async def process(
        self,
        request: RequestType,
        next_handler: NextHandler[RequestType, ResponseType],
    ) -> ResponseType:
        """Delegate to *next_handler*, catching ``Exception`` on failure.

        Args:
            request: The incoming request.
            next_handler: The next callable in the pipeline chain.

        Returns:
            The downstream handler's response on success, or the result
            of ``on_error`` when an exception is caught.
        """
        try:
            return await next_handler(request)
        except Exception as exc:
            if self._logger is not None:
                self._logger.error("Unhandled exception in pipeline: %s", str(exc))
            view_model = self._error_presenter.to_view_model(exc)
            return self._on_error(view_model)
