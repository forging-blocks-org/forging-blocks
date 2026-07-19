"""Middleware that validates requests before delegation and short-circuits on failure."""

from collections.abc import Callable

from forging_blocks.presentation.middleware.middleware import Middleware
from forging_blocks.presentation.middleware.next_handler import NextHandler


class ValidationMiddleware[RequestType, ResponseType](Middleware[RequestType, ResponseType]):
    """Validates each request before forwarding to the downstream handler.

    Delegates all validation logic to a caller-supplied ``validator``
    callable.  When the validator returns a response, the middleware
    short-circuits the pipeline — the downstream handler is never
    called.  When the validator returns ``None``, the request is
    considered valid and passes through unchanged.

    Responsibilities:
        - Invoke the validator with every incoming request.
        - Short-circuit and return the validator's response when
          it is not ``None``.
        - Pass the request through unchanged when the validator
          returns ``None``.

    Non-Responsibilities:
        - Define validation rules — those live in the caller.
        - Format error responses — the validator returns the
          final ``ResponseType`` directly.
        - Handle errors raised by downstream middleware or the handler.
    """

    __slots__ = ("_validator",)

    def __init__(self, validator: Callable[[RequestType], ResponseType | None]) -> None:
        """Wrap *validator* so every request is validated.

        Args:
            validator: A callable that receives the request and returns
                either a ``ResponseType`` (to short-circuit) or ``None``
                (to pass through).
        """
        self._validator = validator

    async def process(
        self,
        request: RequestType,
        next_handler: NextHandler[RequestType, ResponseType],
    ) -> ResponseType:
        """Validate the request, short-circuiting on failure.

        Args:
            request: The incoming request.
            next_handler: The next callable in the pipeline chain.

        Returns:
            - The validator's response when it short-circuits.
            - The downstream handler's response otherwise.
        """
        error_response = self._validator(request)
        if error_response is not None:
            return error_response
        return await next_handler(request)
