"""Presentation adapter implementations.

Concrete adapters that bridge transport concerns and the application layer.
"""

from .presentation_adapter import PresentationAdapter
from .request_adapter import RequestAdapter
from .response_adapter import ResponseAdapter

__all__ = [
    "PresentationAdapter",
    "RequestAdapter",
    "ResponseAdapter",
]
