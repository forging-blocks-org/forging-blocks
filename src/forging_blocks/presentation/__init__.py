"""Presentation layer contracts for the ForgingBlocks framework.

The presentation layer defines the contracts (ports) that drive the application
from the primary/adapter side. It includes:

- ``PresenterPort``: The core contract that all presentation adapters must
  implement, defining how to present success responses and errors.
- ``ErrorPresenter``: A utility for formatting structured errors
  (``Error``, exceptions, and ``Result`` errors) into user-friendly messages.
- ``ErrorMessageModel``: A single error message ready for display.
- ``ErrorViewModel``: A collection of error messages ready for presentation.
- ``Middleware``: Protocol for cross-cutting interceptors that sit between
  the adapter and the application handler.
- ``Pipeline``: Composes middleware into an immutable, executable chain.
"""

from .error_message_model import ErrorMessageModel
from .error_presenter import ErrorPresenter
from .error_status_code_mapper import ErrorStatusCodeMapper
from .error_view_model import ErrorViewModel
from .middleware import Middleware
from .pipeline import Pipeline
from .presentation_adapter import PresentationAdapter
from .presenter_contract import PresenterPort
from .request_adapter import RequestAdapter
from .response_adapter import ResponseAdapter

__all__ = [
    "ErrorMessageModel",
    "ErrorPresenter",
    "ErrorStatusCodeMapper",
    "ErrorViewModel",
    "Middleware",
    "Pipeline",
    "PresentationAdapter",
    "PresenterPort",
    "RequestAdapter",
    "ResponseAdapter",
]
