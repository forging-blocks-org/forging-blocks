from typing import Collection, Iterator, Optional

from .core import ErrorMessage, ErrorMetadata, FieldReference


class Error:
    """
    The base class for all errors in the system.
    This provides a concrete implementation of an error with a message and metadata.
    """

    def __init__(self, message: ErrorMessage, metadata: Optional[ErrorMetadata] = None):
        self._message = message
        self._metadata = metadata or ErrorMetadata(context={})

    @property
    def message(self) -> ErrorMessage:
        return self._message

    @property
    def metadata(self) -> ErrorMetadata:
        return self._metadata

    def __str__(self) -> str:
        return f"{self.message.value}{self._format_context()}"

    def _format_context(self) -> str:
        if self.metadata.context:
            return f" | Context: {self.metadata.context}"
        return ""


class Errors:
    """
    The base class for all collections of errors.
    It provides a concrete implementation for wrapping a collection of 'Error' objects.
    """

    def __init__(
        self, field: FieldReference, errors: Optional[Collection[Error]] = None
    ):
        self._field = field
        self._initialize_errors(errors)

    @property
    def field(self) -> FieldReference:
        return self._field

    @property
    def errors(self) -> Collection[Error]:
        return self._errors

    def __iter__(self) -> Iterator[Error]:
        return iter(self._errors)

    def __len__(self) -> int:
        return len(self._errors)

    def __str__(self) -> str:
        error_messages = "\n".join(f" - {str(error)}" for error in self.errors)
        return f"Errors for field '{self.field.value}':\n{error_messages}"

    def _initialize_errors(self, errors: Optional[Collection[Error]]) -> None:
        if errors:
            self._errors = list(errors)
        else:
            self._errors = []
