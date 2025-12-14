"""ForgingBlocks foundation modules."""

from .errors import (
    CantModifyImmutableAttributeError,
    CombinedValidationErrors,
    Error,
    ErrorMessage,
    ErrorMetadata,
    FieldReference,
    NoneNotAllowedError,
    RuleViolationError,
    ValidationError,
    ValidationFieldErrors,
)
from .mapper import Mapper
from .ports import (
    InboundPort,
    InputPort,
    InputType,
    OutboundPort,
    OutputPort,
    OutputType,
    Port,
)
from .result import Err, Ok, Result
from .result_mapper import ResultMapper

__all__ = [
    "Port",
    "InboundPort",
    "OutboundPort",
    "InputPort",
    "OutputPort",
    "InputType",
    "OutputType",
    "Mapper",
    "Result",
    "Ok",
    "Err",
    "ResultMapper",
    "Error",
    "ValidationFieldErrors",
    "CombinedValidationErrors",
    "NoneNotAllowedError",
    "CantModifyImmutableAttributeError",
    "ErrorMessage",
    "ErrorMetadata",
    "FieldReference",
    "RuleViolationError",
    "ValidationError",
]
