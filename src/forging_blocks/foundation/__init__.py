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
    ResultAccessError,
    RuleViolationError,
    ValidationError,
    ValidationFieldErrors,
)
from .identified import Identified
from .mapper import Mapper
from .messages import Command, Event, Message, Query
from .meta import FinalABCMeta, FinalMeta, runtime_final
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
    "CombinedErrors",
    "CombinedRuleViolationErrors",
    "ErrorMessage",
    "ErrorMetadata",
    "FieldReference",
    "FieldErrors",
    "Identified",
    "RuleViolationError",
    "ValidationError",
    "FinalABCMeta",
    "FinalMeta",
    "runtime_final",
    "ResultAccessError",
    "Command",
    "Query",
    "Event",
    "Message",
]
