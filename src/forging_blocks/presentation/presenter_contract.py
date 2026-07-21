"""Contract for presentation adapters in a hexagonal architecture.

Presentation adapters format data for external consumers (CLI, web, API, etc.).
They define how application responses are rendered, keeping formatting logic
out of the application layer.
"""

from abc import ABC

from forging_blocks.foundation.ports import InboundPort, check_methods


class PresenterPort[ResponseType](InboundPort[ResponseType, None], ABC):
    """ABC for presentation adapters.

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

    async def present(self, response: ResponseType) -> None:
        """Render the application response to the output channel.

        Args:
            response: Domain/output data produced by the application.

        Notes:
            - Output channel (terminal, API, file) is adapter-specific.
            - Must not modify the response data.
        """
        ...

    async def present_error(self, error: Exception) -> None:
        """Render an error to the output channel.

        Args:
            error: Exception from the application layer.

        Notes:
            - Must preserve error context for diagnostics.
            - Output format is adapter-specific.
        """
        ...

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        """Structural check: any class with ``present`` and
        ``present_error`` satisfies this port.
        """
        if cls is PresenterPort:
            return check_methods(subclass, "present", "present_error")
        return NotImplemented
