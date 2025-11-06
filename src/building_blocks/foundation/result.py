"""Result type implementation inspired by Rust's Result enum."""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar

from building_blocks.foundation.errors.base import Error
from building_blocks.foundation.errors.core import ErrorMessage

ResultType = TypeVar("ResultType", covariant=True)
ErrorType = TypeVar("ErrorType", covariant=True)


class ResultAccessError(Error):
    """Exception raised when trying to access value or err from an inappropriate Result variant."""

    def __init__(self, message: ErrorMessage | None = None) -> None:
        if message is None:
            message = ErrorMessage("Invalid access on Result type.")
        self._error_message = message
        super().__init__(message)

    @classmethod
    def cannot_access_value(cls) -> ResultAccessError:
        """Create an error for accessing value from an Err Result."""
        return cls(ErrorMessage("Cannot access value from an Err Result."))

    @classmethod
    def cannot_access_error(cls) -> ResultAccessError:
        """Create an error for accessing error from an Ok Result."""
        return cls(ErrorMessage("Cannot access error from an Ok Result."))

    @property
    def message(self) -> ErrorMessage:
        """Return the stored message as a string."""
        return self._error_message

    def __str__(self) -> str:
        """Readable string representation."""
        return self._error_message.value


class Result(Protocol, Generic[ResultType, ErrorType]):
    """A type that represents either a success (Ok) or an error (Err)."""

    @property
    def is_ok(self) -> bool:
        """Guard method to check if that Result if an ok."""
        ...

    @property
    def is_err(self) -> bool:
        """Guard method to check if that Result if an err."""
        ...

    @property
    def value(self) -> ResultType | None:
        """Method to return the actual value."""
        ...

    @property
    def error(self) -> ErrorType | None:
        """Method to return the actual error."""
        ...


class Ok(Result[ResultType, ErrorType], Generic[ResultType, ErrorType]):
    """Represents a successful result."""

    def __init__(self, value: ResultType) -> None:
        self._value = value

    @property
    def is_err(self) -> bool:
        """Check if the result is an error."""
        return False

    @property
    def is_ok(self) -> bool:
        """Check if the result is ok."""
        return True

    @property
    def value(self) -> ResultType:
        """Get the successful value."""
        return self._value

    @property
    def error(self) -> None:
        """Attempting to get error from an Ok result raises an error."""
        raise ResultAccessError.cannot_access_error()

    def __repr__(self) -> str:
        """Return a string representation of the Ok result."""
        return f"Ok({self._value!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another Ok result."""
        return isinstance(other, Ok) and self._value == other._value

    def __hash__(self) -> int:
        """Return the hash of the Ok result."""
        return hash(self._value)

    def __str__(self) -> str:
        """Return a string representation of the Ok result."""
        return f"Ok({self._value})"


class Err(Result[ResultType, ErrorType], Generic[ResultType, ErrorType]):
    """Represents an error result."""

    def __init__(self, error: ErrorType) -> None:
        self._error = error

    @property
    def is_err(self) -> bool:
        """Check if the result is an error."""
        return True

    @property
    def is_ok(self) -> bool:
        """Check if the result is ok."""
        return False

    @property
    def value(self) -> None:
        """Attempting to get value from an Err result raises an error."""
        raise ResultAccessError.cannot_access_value()

    @property
    def error(self) -> ErrorType:
        """Get the error value."""
        return self._error

    def __repr__(self) -> str:
        """Return a string representation of the Err result."""
        return f"Err({self._error!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another Ok result."""
        return isinstance(other, Err) and self._error == other._error

    def __hash__(self) -> int:
        """Return the hash of the Ok result."""
        return hash(self._error)

    def __str__(self) -> str:
        """Return a string representation of the Ok result."""
        return f"Err({self._error})"
