"""Inbound port for stateless application-service orchestrators."""

from typing import Protocol, runtime_checkable

from forging_blocks.foundation.ports import InboundPort
from forging_blocks.foundation.result import Result


@runtime_checkable
class ApplicationService[RequestType, ResponseType, ErrorType](
    InboundPort[RequestType, Result[ResponseType, ErrorType]],
    Protocol,
):
    """Protocol for a stateless application-service orchestrator."""

    async def execute(self, request: RequestType) -> Result[ResponseType, ErrorType]:
        """Execute the business logic for *request*."""
        ...
