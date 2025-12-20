from scripts.release.application.errors.tag_already_exists_error import (
    TagAlreadyExistsError,
)
from scripts.release.domain.value_objects import (
    ReleaseLevel,
    ReleaseBranchName,
    TagName,
)

from scripts.release.application.ports.inbound import (
    PrepareReleaseUseCase,
    PrepareReleaseInput,
    PrepareReleaseOutput,
)
from scripts.release.application.ports.outbound import (
    VersioningService,
    VersionControl,
)


class PrepareReleaseService(PrepareReleaseUseCase):
    """
    Application service responsible for preparing a release.

    Responsibilities:
    - compute next version
    - create or resume release branch
    - apply version bump (unless dry_run)
    - commit release artifacts (unless dry_run)
    - push branch (unless dry_run)
    """

    def __init__(
        self,
        *,
        versioning: VersioningService,
        vcs: VersionControl,
    ) -> None:
        self._versioning = versioning
        self._vcs = vcs

    async def execute(
        self,
        request: PrepareReleaseInput,
    ) -> PrepareReleaseOutput:
        level = ReleaseLevel.from_str(request.level)

        # 1. Compute next version
        version = self._versioning.compute_next_version(level)

        branch = ReleaseBranchName.from_version(version)
        tag = TagName.for_version(version)

        # 2. Enforce invariant: tag must not exist
        self._ensure_tag_does_not_exist(tag)

        if not request.dry_run:
            # 3. Create or resume release branch
            if self._vcs.branch_exists(branch):
                self._vcs.checkout(branch)
            else:
                self._vcs.create_branch(branch)
                self._versioning.apply_version(version)
                self._vcs.commit_release_artifacts()

            # 4. Push branch (no tags here)
            self._vcs.push(
                branch,
                push_tags=False,
            )

        return PrepareReleaseOutput(
            version=version.value,
            branch=branch.value,
            tag=tag.value,
        )

    def _ensure_tag_does_not_exist(self, tag_name: TagName) -> None:
        if self._vcs.tag_exists(tag_name):
            raise TagAlreadyExistsError(tag_name.value)
