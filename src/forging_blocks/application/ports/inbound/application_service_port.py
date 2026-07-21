"""Inbound port for stateless application-service orchestrators."""

from abc import ABC, abstractmethod

from forging_blocks.foundation.ports import InboundPort, check_methods
from forging_blocks.foundation.result import Result


class ApplicationServicePort[RequestType, ResponseType](
    InboundPort[RequestType, Result[ResponseType, object]],
    ABC,
):
    """ABC for a stateless application-service orchestrator."""

    @abstractmethod
    async def execute(self, request: RequestType) -> Result[ResponseType, object]:
        """Execute the business logic for *request*."""
        ...

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        """Structural check: any class with ``execute`` satisfies this port."""
        if cls is ApplicationServicePort:
            return check_methods(subclass, "execute")
        return NotImplemented
