"""Use case module.

Auto-generated minimal module docstring.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class AsyncUseCase(ABC, Generic[TRequest, TResponse]):
    """Application inbound port for asynchronous use cases.

    Use cases orchestrate interactions between domain services, repositories,
    and other components to fulfill application-specific operations.

    This base class is for asynchronous use cases—implementations should define
    'async def execute(self, request: TRequest) -> TResponse'.
    """

    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        """Asynchronous execution of the use case with the provided request.

        This method should be implemented by concrete use case classes to
        perform the necessary operations and return a response.

        Args:
            request: The request object containing input data for the use case.

        Returns:
            TResponse: The response object containing the result of the use case
            execution.

        Raises:
            Exception: Any exceptions that occur during execution should be
            handled appropriately, such as validation errors or service failures.
        """


class SyncUseCase(ABC, Generic[TRequest, TResponse]):
    """Application inbound port for synchronous use cases.

    Use cases orchestrate interactions between domain services, repositories,
    and other components to fulfill application-specific operations.

    This base class is for synchronous use cases—implementations should define
    'def execute(self, request: TRequest) -> TResponse'.
    """

    @abstractmethod
    def execute(self, request: TRequest) -> TResponse:
        """Synchronous execution of the use case with the provided request.

        This method should be implemented by concrete use case classes to
        perform the necessary operations and return a response.

        Args:
            request: The request object containing input data for the use case.

        Returns:
            TResponse: The response object containing the result of the use case
            execution.

        Raises:
            Exception: Any exceptions that occur during execution should be
            handled appropriately, such as validation errors or service failures.
        """
