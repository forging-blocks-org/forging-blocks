from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ResultType = TypeVar("ResultType")
ErrorType = TypeVar("ErrorType")


class ResultError(Exception):
    """Base exception for Result errors."""

    pass


class ResultAccessError(ResultError):
    """Raised when accessing value or errors inappropriately on a Result variant."""

    pass


class Result(ABC, Generic[ResultType, ErrorType]):
    @property
    @abstractmethod
    def value(self) -> ResultType:
        """
        Returns the value if the Result is Ok.
        Raises ResultAccessError if the Result is Err.
        """
        pass

    @property
    @abstractmethod
    def error(self) -> ErrorType:
        """
        Returns the error if the Result is Err.
        Raises ResultAccessError if the Result is Ok.
        """
        pass

    @property
    def is_ok(self) -> bool:
        return isinstance(self, Ok)

    @property
    def is_err(self) -> bool:
        return isinstance(self, Err)


class Ok(Result, Generic[ResultType, ErrorType]):
    def __init__(self, value: ResultType) -> None:
        self._value = value

    @property
    def value(self) -> ResultType:
        return self._value

    @property
    def error(self) -> ErrorType:
        raise ResultAccessError("Cannot access error from an Ok Result.")

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"


class Err(Result, Generic[ResultType, ErrorType]):
    def __init__(self, error: ErrorType) -> None:
        self._error = error

    @property
    def value(self) -> ResultType:
        raise ResultAccessError("Cannot access value from an Err Result.")

    @property
    def error(self) -> ErrorType:
        return self._error

    def __repr__(self) -> str:
        return f"Err({self.error!r})"
