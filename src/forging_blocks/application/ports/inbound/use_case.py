"""Inbound application port for executing use cases.

Use cases define the application’s orchestration boundary: they coordinate
domain operations to fulfill a specific application intent. Use cases are
pure application-layer logic and must not depend on infrastructure details.

Responsibilities:
    - Orchestrate domain interactions.
    - Call repositories, outbound ports, and aggregates.
    - Maintain transactional consistency (via Unit of Work).

Non-Responsibilities:
    - Transport logic (HTTP, messaging systems).
    - Persistence implementation details.
    - UI or framework-specific concerns.
"""

from typing import Protocol, TypeVar

from forging_blocks.foundation.ports import InboundPort

RequestType = TypeVar("RequestType", contravariant=True)
ResponseType = TypeVar("ResponseType", covariant=True)


class UseCase(InboundPort[RequestType, ResponseType], Protocol):
    """Inbound port for defining application use case operations.

    A UseCase represents an application-level action that may involve multiple
    domain objects and outbound interactions. Use cases must remain free of
    infrastructure dependencies and must uphold application-level invariants.
    """

    async def execute(self, request: RequestType) -> ResponseType:
        """Execute the use case asynchronously.

        Args:
            request: The request DTO carrying user or system input.

        Returns:
            A DTO or domain object representing the outcome.

        Raises:
            ApplicationError: If the use case fails for domain reasons.

        Notes:
            This method is asynchronous and should not perform blocking operations.
        """
        ...
