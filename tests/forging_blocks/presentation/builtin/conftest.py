"""Shared test doubles for builtin middleware tests."""

from forging_blocks.application.ports.outbound.logger_port import LoggerPort


class FakeLogger(LoggerPort[str]):
    """Captures all log messages for inspection in tests."""

    __slots__ = ("messages",)

    def __init__(self) -> None:
        self.messages: list[tuple[str, tuple[object, ...]]] = []

    def debug(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))

    def info(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))

    def warning(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))

    def error(self, msg: str, *args: object) -> None:
        self.messages.append((msg, args))


class FakeRequest:
    """Minimal request stub for middleware tests."""

    __slots__ = ("value",)

    def __init__(self, value: str) -> None:
        self.value = value


class FakeResponse:
    """Minimal response stub for middleware tests."""

    __slots__ = ("result",)

    def __init__(self, result: str) -> None:
        self.result = result
