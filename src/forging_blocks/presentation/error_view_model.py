"""A collection of error messages ready for presentation."""

from dataclasses import dataclass, field

from forging_blocks.presentation.error_message_model import ErrorMessageModel


@dataclass(frozen=True)
class ErrorViewModel:
    """Holds one or more ``ErrorMessageModel`` entries produced by an
    ``ErrorPresenter``.

    Multiple entries coexist when a single operation results in several
    validation or business-rule failures.
    """

    messages: list[ErrorMessageModel] = field(default_factory=list[ErrorMessageModel])
