from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ResultType = TypeVar("ResultType")
ErrorType = TypeVar("ErrorType")


class ResultAccessError(Exception):
    def __init__(self, message: str = "ResultAccessError") -> None:
        super().__init__(message)

    @classmethod
    def cannot_access_value(cls) -> ResultAccessError:
        return cls("Cannot access value from an Err Result.")

    @classmethod
    def cannot_access_error(cls) -> ResultAccessError:
        return cls("Cannot access error from an Ok Result.")

    @property
    def message(self) -> str:
        return str(self.args[0])


class Result(ABC, Generic[ResultType, ErrorType]):
    @property
    @abstractmethod
    def value(self) -> ResultType:
        pass

    @property
    @abstractmethod
    def error(self) -> ErrorType:
        pass

    @property
    def is_ok(self) -> bool:
        return isinstance(self, Ok)

    @property
    def is_err(self) -> bool:
        return isinstance(self, Err)


class Ok(Result[ResultType, None], Generic[ResultType]):
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self) -> ResultType:
        return self._value

    @property
    def error(self) -> None:
        raise ResultAccessError.cannot_access_error()


class Err(Result[None, ErrorType], Generic[ErrorType]):
    def __init__(self, error) -> None:
        self._error = error

    @property
    def value(self) -> None:
        raise ResultAccessError.cannot_access_value()

    @property
    def error(self) -> ErrorType:
        return self._error
