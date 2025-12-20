from enum import IntEnum, StrEnum, auto


class ReleaseLevelEnum(StrEnum):
    PATCH = auto()
    MINOR = auto()
    MAJOR = auto()


class PullRequestTitleLengthBoundaries(IntEnum):
    MIN = 10
    MAX = 50
