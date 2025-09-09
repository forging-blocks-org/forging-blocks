from building_blocks.foundation.errors.base import Error
from building_blocks.foundation.errors.core import ErrorMessage


class EntityIdCannotBeNoneError(Error):
    def __init__(self) -> None:
        message = ErrorMessage("Entity ID cannot be None.")
        super().__init__(message)


class EntityAssignError(RuntimeError):
    """
    Raised when trying to assign an id in an invalid way (already assigned, unhashable,
    etc.).
    """


class DraftEntityIsNotHashableError(Error):
    def __init__(self) -> None:
        message = ErrorMessage(
            "Draft entity is not hashable. Ensure all its fields are hashable."
        )
        super().__init__(message)
