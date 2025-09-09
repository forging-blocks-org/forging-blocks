from __future__ import annotations

from typing import Generic, Protocol, TypeVar

ResultType = TypeVar("ResultType", covariant=True)
ErrorType = TypeVar("ErrorType", covariant=True)


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


class Result(Protocol, Generic[ResultType, ErrorType]):
    @property
    def is_ok(self) -> bool: ...

    @property
    def is_err(self) -> bool: ...

    @property
    def value(self) -> ResultType: ...

    @property
    def error(self) -> ErrorType: ...


class Ok(Result[ResultType, ErrorType], Generic[ResultType, ErrorType]):
    def __init__(self, value) -> None:
        self._value = value

    @property
    def is_err(self) -> bool:
        return False

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def value(self) -> ResultType:
        return self._value

    @property
    def error(self) -> None:
        raise ResultAccessError.cannot_access_error()

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"


class Err(Result[ResultType, ErrorType], Generic[ResultType, ErrorType]):
    def __init__(self, error) -> None:
        self._error = error

    @property
    def is_err(self) -> bool:
        return True

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def value(self) -> None:
        raise ResultAccessError.cannot_access_value()

    @property
    def error(self) -> ErrorType:
        return self._error

    def __repr__(self) -> str:
        return f"Err({self._error!r})"
