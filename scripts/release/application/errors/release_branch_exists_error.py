"""Error raised when a release branch already exists with the same changes."""

from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.error import Error


class ReleaseBranchExistsError(Error[dict[str, object]]):
    """Raised when attempting to create a release branch that already exists with same changes."""

    def __init__(self, branch_name: str) -> None:
        self.branch_name = branch_name
        super().__init__(
            ErrorMessage(f"Release branch '{branch_name}' already exists with the same changes")
        )
