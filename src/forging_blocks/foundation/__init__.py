"""ForgingBlocks foundation modules."""

from .errors import (
    CantModifyImmutableAttributeError,
    CombinedErrors,
    CombinedRuleViolationErrors,
    CombinedValidationErrors,
    Error,
    ErrorMessage,
    ErrorMetadata,
    FieldErrors,
    FieldReference,
    NoneNotAllowedError,
    RuleViolationError,
    ValidationError,
    ValidationFieldErrors,
)
from .mapper import Mapper
from .meta import FinalMeta, runtime_final
from .ports import (
    InboundPort,
    InputPort,
    InputType,
    OutboundPort,
    OutputPort,
    OutputType,
    Port,
)
from .result import Err, Ok, Result, ResultAccessError
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
    "CombinedErrors",
    "CombinedRuleViolationErrors",
    "ErrorMessage",
    "ErrorMetadata",
    "FieldReference",
    "FieldErrors",
    "RuleViolationError",
    "ValidationError",
    "FinalMeta",
    "runtime_final",
    "ResultAccessError",
]
