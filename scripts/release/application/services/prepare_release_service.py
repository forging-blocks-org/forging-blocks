from scripts.release.application.context import ReleaseContext
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

    This use case is transactional:
    - either the release branch is fully prepared
    - or the system is rolled back to its original state
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

        previous_version = self._versioning.current_version()
        next_version = self._versioning.compute_next_version(level)

        branch = ReleaseBranchName.from_version(next_version)
        tag = TagName.for_version(next_version)

        context = ReleaseContext(
            version=next_version,
            previous_version=previous_version,
            branch=branch,
            tag=tag,
        )

        self._ensure_tag_does_not_exist(tag)

        if request.dry_run:
            return self._output(context)

        try:
            self._prepare_branch(context)
            return self._output(context)
        except Exception:
            self._rollback(context)
            raise

    def _prepare_branch(self, ctx: ReleaseContext) -> None:
        if self._vcs.branch_exists(ctx.branch):
            self._vcs.checkout(ctx.branch)
        else:
            self._vcs.create_branch(ctx.branch)
            self._versioning.apply_version(ctx.version)
            self._vcs.commit_release_artifacts()

        self._vcs.push(ctx.branch, push_tags=False)

    def _rollback(self, ctx: ReleaseContext) -> None:
        # Rollback must never raise
        try:
            self._vcs.checkout_main()
        except Exception:
            pass

        try:
            self._vcs.delete_branch(ctx.branch)
        except Exception:
            pass

        try:
            self._vcs.delete_remote_branch(ctx.branch)
        except Exception:
            pass

        try:
            self._vcs.delete_tag(ctx.tag)
        except Exception:
            pass

        try:
            self._versioning.rollback_version(ctx.previous_version)
        except Exception:
            pass

    def _ensure_tag_does_not_exist(self, tag: TagName) -> None:
        if self._vcs.tag_exists(tag):
            raise TagAlreadyExistsError(tag.value)

    def _output(self, ctx: ReleaseContext) -> PrepareReleaseOutput:
        return PrepareReleaseOutput(
            version=ctx.version.value,
            branch=ctx.branch.value,
            tag=ctx.tag.value,
        )
