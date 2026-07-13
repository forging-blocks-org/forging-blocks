"""Error modelling and presentation utilities.

Types and transformers that convert application errors into user-facing messages.
"""

from .error_message_model import ErrorMessageModel
from .error_presenter import ErrorPresenter
from .error_status_code_mapper import ErrorStatusCodeMapper
from .error_view_model import ErrorViewModel

__all__ = [
    "ErrorMessageModel",
    "ErrorPresenter",
    "ErrorStatusCodeMapper",
    "ErrorViewModel",
]
