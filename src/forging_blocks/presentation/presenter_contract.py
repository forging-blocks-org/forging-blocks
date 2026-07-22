"""Contract for presentation adapters in a hexagonal architecture.

Presentation adapters format data for external consumers (CLI, web, API, etc.).
They define how application responses are rendered, keeping formatting logic
out of the application layer.
"""

from abc import abstractmethod

from forging_blocks.foundation.ports import InboundPort


class PresenterPort[ResponseType](InboundPort):
    """Contract for presentation adapters.

    Responsibilities:
        - Define the contract for formatting application responses.
        - Keep presentation logic outside the application core.
        - Support multiple output formats (CLI, API, UI).

    Non-Responsibilities:
        - Implement business logic.
        - Handle infrastructure concerns (HTTP, I/O) — those are adapters.

    Example:
        >>> from forging_blocks.presentation.presenter_contract import PresenterPort
        >>> class CliPresenter(PresenterPort[str]):
        ...     async def present(self, response: str) -> None:
        ...         print(f"Result: {response}")
        ...
        ...     async def present_error(self, error: Exception) -> None:
        ...         print(f"Error: {error}", file=sys.stderr)
    """

    @abstractmethod
    async def present(self, response: ResponseType) -> None:
        """Render the application response to the output channel.

        Args:
            response: Domain/output data produced by the application.

        Notes:
            - Output channel (terminal, API, file) is adapter-specific.
            - Must not modify the response data.
        """
        ...

    @abstractmethod
    async def present_error(self, error: Exception) -> None:
        """Render an error to the output channel.

        Args:
            error: Exception from the application layer.

        Notes:
            - Must preserve error context for diagnostics.
            - Output format is adapter-specific.
        """
        ...
