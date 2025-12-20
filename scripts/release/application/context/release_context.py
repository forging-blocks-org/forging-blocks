from dataclasses import dataclass

from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    ReleaseVersion,
    TagName,
)


@dataclass(frozen=True)
class ReleaseContext:
    version: ReleaseVersion
    previous_version: ReleaseVersion
    branch: ReleaseBranchName
    tag: TagName
