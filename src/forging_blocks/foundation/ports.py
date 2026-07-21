"""Foundational port definition for the ForgingBlocks."""

import warnings
from typing import Protocol, runtime_checkable


class ArchitectureWarning(UserWarning):
    """Warning emitted when a port implementation violates dependency direction rules.

    Inbound ports belong in the application layer; outbound port implementations
    belong in infrastructure. This warning fires at class creation time when a
    port subclass is defined in a module that suggests the wrong architectural layer.
    """


@runtime_checkable
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
    """Alias for Port used as an inbound marker.

    Note:
        This class uses ``__init_subclass__`` to warn when subclasses are defined
        in modules whose name contains ``"infrastructure"``, which suggests the
        implementation lives in the wrong architectural layer. This check only
        fires on explicit inheritance (``class Foo(InboundPort)``). Classes that
        satisfy the InboundPort contract structurally (via ``Protocol`` duck-typing)
        without inheriting from it bypass this guard. Use the import-linter
        contract for authoritative enforcement.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        module = cls.__module__
        if "infrastructure" in module:
            warnings.warn(
                f"{cls.__qualname__} inherits from InboundPort but is defined "
                f"in an infrastructure module ('{module}'). "
                f"Inbound port implementations belong in the application layer.",
                ArchitectureWarning,
                stacklevel=3,
            )


class OutboundPort[InputType, OutputType](Port[InputType, OutputType], Protocol):
    """Alias for Port used as an outbound marker.

    Note:
        This class uses ``__init_subclass__`` to warn when subclasses are defined
        in modules whose name contains ``".ports.inbound"``, which suggests the
        implementation lives in the wrong architectural layer. This check only
        fires on explicit inheritance (``class Foo(OutboundPort)``). Classes that
        satisfy the OutboundPort contract structurally (via ``Protocol`` duck-typing)
        without inheriting from it bypass this guard. Use the import-linter
        contract for authoritative enforcement.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        module = cls.__module__
        if ".ports.inbound" in module:
            warnings.warn(
                f"{cls.__qualname__} inherits from OutboundPort but is defined "
                f"in an inbound port module ('{module}'). "
                f"Outbound port implementations belong in infrastructure.",
                ArchitectureWarning,
                stacklevel=3,
            )
