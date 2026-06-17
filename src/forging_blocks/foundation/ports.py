"""Foundational port definition for the ForgingBlocks."""

from typing import Protocol


class Port[InputType, OutputType](Protocol):
    """Base protocol for defining interface contracts.

    Port is a generic Protocol that serves as the foundation for interface
    declarations. It provides type parameters (InputType, OutputType) and
    defines no methods — it's a marker protocol that you extend to create
    your own specific interfaces.

    TYPE PARAMETERS:
    - `InputType`: The type of data accepted by operations on this interface.
    - `OutputType`: The type of data returned by operations on this interface.
    """


class InboundPort[InputType, OutputType](Port[InputType, OutputType], Protocol):
    """Alias for Port used as an inbound marker."""


class OutboundPort[InputType, OutputType](Port[InputType, OutputType], Protocol):
    """Alias for Port used as an outbound marker."""
