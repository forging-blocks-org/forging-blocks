"""Detect port type references in type annotations.

Recursively unwraps generic aliases, union types, and nested
parameterised generics to determine whether any component references
a specific port type.
"""

from types import UnionType
from typing import get_args, get_origin


class PortReferenceDetector:
    """Detects whether a type annotation references a specific port type."""

    def __init__(self, target_port: type) -> None:
        self._target_port = target_port

    def detects_in(self, parameter_type: object) -> bool:
        """Return ``True`` when *parameter_type* references the target port."""
        if isinstance(parameter_type, UnionType):
            return any(self.detects_in(argument) for argument in get_args(parameter_type))
        if isinstance(parameter_type, type) and self._target_port in parameter_type.__mro__:
            return True
        origin = get_origin(parameter_type)
        if origin is not None and origin is not parameter_type:
            return any(self.detects_in(argument) for argument in get_args(parameter_type))
        return False
