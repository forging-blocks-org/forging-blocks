"""Presentation adapter contract for the ForgingBlocks framework.

Defines ``PresenterPort``, the structural protocol that every presentation
adapter must satisfy. In hexagonal-architecture terms it is the primary port
through which the application delivers its output to the outside world.

Responsibilities:
    - Define a uniform contract for presenting application responses.
    - Define a uniform contract for presenting application errors.
    - Remain free of any transport or rendering concern.

Non-Responsibilities:
    - Rendering to a specific medium (HTML, JSON, terminal, etc.).
    - Transport or I/O logic.
    - Parsing or validating user input.
"""

from typing import Protocol, runtime_checkable

from forging_blocks.foundation.ports import InboundPort


@runtime_checkable
class PresenterPort[ResponseType](InboundPort[ResponseType, None], Protocol):
    """Structural protocol for presentation adapters.

    A ``PresenterPort`` receives an application response and renders it
    to the outside world. It also provides a dedicated method for
    presenting errors so that implementations can apply consistent
    formatting.

    Type Parameters:
        ResponseType: The type of the response object produced by the
            application layer (use case / query handler).

    Example::

        class CliPresenter(PresenterPort[MyUseCaseOutput]):
            def present(self, response: MyUseCaseOutput) -> None:
                print(f"Result: {response.summary}")

            def present_error(self, error: object) -> None:
                print(f"Error: {error}", file=sys.stderr)
    """

    def present(self, response: ResponseType) -> None:
        """Render a successful application response.

        Args:
            response: The response object produced by the application
                layer after a successful operation.

        Notes:
            Implementations must not raise exceptions from this method
            for normal error handling — use ``present_error`` for that.
        """
        ...

    def present_error(self, error: object) -> None:
        """Render an application-level error.

        Args:
            error: An error object — may be a framework ``Error``, a
                ``Result.Err``, a plain ``Exception``, or any other
                error representation the application produces.

        Notes:
            This method exists so that error formatting is a first-class
            concern of the presentation contract, rather than being
            handled via exceptions or ad-hoc logic.
        """
        ...
