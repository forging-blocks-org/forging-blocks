"""A collection of error messages ready for presentation."""

from dataclasses import dataclass, field

from forging_blocks.foundation.autofreeze import auto_freeze
from forging_blocks.foundation.autohash import auto_hash
from forging_blocks.presentation.errors.error_message_model import ErrorMessageModel


@auto_hash
@auto_freeze
@dataclass
class ErrorViewModel:
    """Holds one or more ``ErrorMessageModel`` entries produced by an
    ``ErrorPresenter``.

    Multiple entries coexist when a single operation results in several
    validation or business-rule failures.
    """

    messages: tuple[ErrorMessageModel, ...] = field(default_factory=tuple[ErrorMessageModel])

    def __post_init__(self) -> None:
        """Ensure ``messages`` is stored as an immutable tuple."""
        self.messages = tuple(self.messages)
