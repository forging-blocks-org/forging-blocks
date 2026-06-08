"""Foundational port definition for the ForgingBlocks."""

from typing import Protocol, TypeVar

InputType = TypeVar("InputType", contravariant=True)
OutputType = TypeVar("OutputType", covariant=True)


class Port(Protocol[InputType, OutputType]):  # type: ignore[reportInvalidTypeVarUse]
    """Base protocol for defining interface contracts.

    Port is a generic Protocol that serves as the foundation for interface
    declarations. It provides type parameters (InputType, OutputType) and
    defines no methods — it's a marker protocol that you extend to create
    your own specific interfaces.

    TYPE PARAMETERS:
    - `InputType`: The type of data accepted by operations on this interface.
    - `OutputType`: The type of data returned by operations on this interface.
    """


class InboundPort(Port[InputType, OutputType], Protocol):  # type: ignore[reportInvalidTypeVarUse]
    """Alias for Port used as an inbound marker."""


class OutboundPort(Port[InputType, OutputType], Protocol):  # type: ignore[reportInvalidTypeVarUse]
    """Alias for Port used as an outbound marker."""


class InputPort(InboundPort[InputType, OutputType], Protocol):  # type: ignore[reportInvalidTypeVarUse]
    """Alias for InboundPort."""


class OutputPort(OutboundPort[InputType, OutputType], Protocol):  # type: ignore[reportInvalidTypeVarUse]
    """Alias for OutboundPort."""
