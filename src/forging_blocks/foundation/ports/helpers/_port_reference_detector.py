"""Detect port type references in type annotations.

Recursively unwraps generic aliases, union types, and nested
parameterised generics to determine whether any component references
a specific port type.
"""

from types import UnionType
from typing import cast, get_args, get_origin


class PortReferenceDetector:
    """Detects whether a type annotation references a specific port type.

    Example:
        ```python
        class MyBase: ...


        class MySubclass(MyBase): ...


        detector = PortReferenceDetector(target_port=MyBase)
        detector.detects_in(MySubclass)  # True (MyBase in MRO)
        detector.detects_in(str)  # False
        ```
    """

    def __init__(self, target_port: type) -> None:
        self._target_port = target_port

    def detects_in(self, parameter_type: object) -> bool:
        """Return ``True`` when *parameter_type* references the target port."""
        return bool(self.referenced_ports(parameter_type))

    def referenced_ports(self, parameter_type: object) -> set[type]:
        """Return every port class in *parameter_type* (target or subclass)."""
        found: set[type] = set()
        self._collect(parameter_type, found)
        return found

    def _collect_type_args(self, parameter_type: object, found: set[type]) -> None:
        for argument in get_args(parameter_type):
            self._collect(argument, found)

    def _is_target_port(self, parameter_type: object) -> bool:
        if not isinstance(parameter_type, type):
            return False
        return self._target_port in parameter_type.__mro__

    def _is_generic_with_origin(self, parameter_type: object) -> bool:
        origin = get_origin(parameter_type)
        return origin is not None and origin is not parameter_type

    def _collect(self, parameter_type: object, found: set[type]) -> None:
        if isinstance(parameter_type, UnionType):
            self._collect_type_args(parameter_type, found)
            return
        if self._is_target_port(parameter_type):
            found.add(cast(type, parameter_type))
            return
        if self._is_generic_with_origin(parameter_type):
            self._collect_type_args(parameter_type, found)
