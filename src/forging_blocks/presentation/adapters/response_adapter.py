"""Protocol for translating application output into transport-level responses."""

from typing import Protocol

from forging_blocks.presentation.errors.error_view_model import ErrorViewModel


class ResponseAdapter[UseCaseOutput, RawResponse](Protocol):
    """Translates application-layer output into a transport response.

    Implementations handle transport-specific serialization (e.g.
    JSON encoding, setting HTTP status headers, formatting CLI
    output) and produce the raw response type consumed by the
    transport framework.
    """

    def adapt(self, output: UseCaseOutput) -> RawResponse:
        """Convert successful use-case output into a transport response.

        Args:
            output: The value returned by ``UseCasePort.execute`` on
                success.

        Returns:
            A transport-level response ready to send to the caller.

        """
        ...

    def adapt_error(self, view_model: ErrorViewModel) -> RawResponse:
        """Convert an ``ErrorViewModel`` into a transport error response.

        Args:
            view_model: The error view model produced by
                ``ErrorPresenter.to_view_model``, optionally enriched
                with status codes by ``ErrorStatusCodeMapper``.

        Returns:
            A transport-level error response (e.g. an HTTP response
            with the appropriate status code and JSON body).

        """
        ...
