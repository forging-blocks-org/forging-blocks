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
- ``LoggingMiddleware``: Built-in middleware that traces every request.
- ``TimingMiddleware``: Built-in middleware that measures execution time.
"""

from .adapters.presentation_adapter import PresentationAdapter
from .adapters.request_adapter import RequestAdapter
from .adapters.response_adapter import ResponseAdapter
from .builtin import LoggingMiddleware, TimingMiddleware
from .errors.error_message_model import ErrorMessageModel
from .errors.error_presenter import ErrorPresenter
from .errors.error_status_code_mapper import ErrorStatusCodeMapper
from .errors.error_view_model import ErrorViewModel
from .middleware.middleware import Middleware
from .middleware.pipeline import Pipeline
from .presenter_contract import PresenterPort

__all__ = [
    "ErrorMessageModel",
    "ErrorPresenter",
    "ErrorStatusCodeMapper",
    "ErrorViewModel",
    "LoggingMiddleware",
    "Middleware",
    "Pipeline",
    "PresentationAdapter",
    "PresenterPort",
    "RequestAdapter",
    "ResponseAdapter",
    "TimingMiddleware",
]
