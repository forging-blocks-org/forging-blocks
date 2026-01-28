"""Error raised when a release branch already exists with the same changes."""


class ReleaseBranchExistsError(Exception):
    """Raised when attempting to create a release branch that already exists with same changes."""

    def __init__(self, branch_name: str) -> None:
        self.branch_name = branch_name
        super().__init__(f"Release branch '{branch_name}' already exists with the same changes")
