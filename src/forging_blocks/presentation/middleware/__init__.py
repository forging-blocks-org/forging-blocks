"""Middleware protocol and composition primitives.

Defines the ``Middleware`` structural protocol, the ``NextHandler`` type alias,
and ``Pipeline`` for composing middleware into executable chains.
"""

from .middleware import Middleware
from .pipeline import Pipeline

__all__ = [
    "Middleware",
    "Pipeline",
]
