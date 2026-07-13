"""A collection of error messages ready for presentation."""

from dataclasses import dataclass, field

from forging_blocks.foundation.autofreeze import auto_freeze
from forging_blocks.presentation.errors.error_message_model import ErrorMessageModel


@auto_freeze
@dataclass
class ErrorViewModel:
    """Holds one or more ``ErrorMessageModel`` entries produced by an
    ``ErrorPresenter``.

    Multiple entries coexist when a single operation results in several
    validation or business-rule failures.
    """

    messages: list[ErrorMessageModel] = field(default_factory=list[ErrorMessageModel])
