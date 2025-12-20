from forging_blocks.foundation.ports import OutputPort

from scripts.release.domain.value_objects import (
    ReleaseLevel,
    ReleaseVersion,
)


class VersioningService(OutputPort):
    """
    Computes and applies semantic versions to the package definition.

    Must be non-interactive and deterministic.
    """

    def current_version(self) -> ReleaseVersion:
        """
        Read the currently configured version (e.g., from pyproject.toml via Poetry).
        """
        ...

    def compute_next_version(
        self,
        level: ReleaseLevel,
    ) -> ReleaseVersion:
        """
        Compute the next version without mutating state.
        """
        ...

    def apply_version(
        self,
        version: ReleaseVersion,
    ) -> None:
        """
        Mutate version to the given target.
        """
        ...

    def rollback_version(
        self,
        previous: ReleaseVersion,
    ) -> None:
        """
        Restore the previously captured version.
        Typically implemented as apply_version(previous).
        """
        ...
