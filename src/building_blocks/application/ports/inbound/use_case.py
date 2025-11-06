"""Asynchronous use case inbound port definition."""

from typing import Protocol, TypeVar

from building_blocks.foundation.ports import InboundPort

RequestType = TypeVar("RequestType", contravariant=True)
ResponseType = TypeVar("ResponseType", covariant=True)


class UseCase(InboundPort[RequestType, ResponseType], Protocol):
    """Application inbound port for asynchronous use cases.

    Use cases orchestrate interactions between domain services, repositories,
    and other components to fulfill application-specific operations.

    This base class is for asynchronous use cases—implementations should define
    'async def execute(self, request: TRequest) -> ResponseType'.
    """

    async def execute(self, request: RequestType) -> ResponseType:
        """Asynchronous execution of the use case with the provided request.

        This method should be implemented by concrete use case classes to
        perform the necessary operations and return a response.

        Args:
            request: The request object containing input data for the use case.

        Returns:
            ResponseType: The response object containing the result of the use case
            execution.

        Raises:
            Exception: Any exceptions that occur during execution should be
            handled appropriately, such as validation errors or service failures.
        """
        ...
