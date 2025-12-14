"""Foundational port definition for the ForgingBlocks."""

# pyright: reportInvalidTypeVarUse=false
# mypy: disable-error-code=misc

from typing import Generic, Protocol, TypeAlias, TypeVar

InputType = TypeVar("InputType", contravariant=True)
OutputType = TypeVar("OutputType", covariant=True)


class Port(Protocol, Generic[InputType, OutputType]):
    """Base protocol for defining interface contracts.

    Port is a generic Protocol that serves as the foundation for interface
    declarations. It provides type parameters (InputType, OutputType) and
    defines no methods — it's a marker protocol that you extend to create your
    own specific interfaces.

    TYPE PARAMETERS:
    - `InputType`: The type of data accepted by operations on this interface (contravariant).
    - `OutputType`: The type of data returned by operations on this interface (covariant).
    """

    ...


InboundPort: TypeAlias = Port[InputType, OutputType]
OutboundPort: TypeAlias = Port[InputType, OutputType]

InputPort: TypeAlias = InboundPort
OutputPort: TypeAlias = OutboundPort
