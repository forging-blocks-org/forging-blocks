import logging
from scripts.release.application.workflow import ReleaseContext, ReleaseStep
from scripts.release.application.errors.tag_already_exists_error import (
    TagAlreadyExistsError,
)
from scripts.release.domain.messages import OpenPullRequestCommand
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
    ReleaseTransaction,
    VersioningService,
    VersionControl,
    ChangelogGenerator,
    ChangelogRequest,
    ReleaseCommandBus,
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
        versioning_service: VersioningService,
        version_control: VersionControl,
        transaction: ReleaseTransaction,
        message_bus: ReleaseCommandBus,
        changelog_generator: ChangelogGenerator,
    ) -> None:
        self._versioning_service = versioning_service
        self._version_control = version_control
        self._transaction = transaction
        self._message_bus = message_bus
        self._changelog_generator = changelog_generator

    async def execute(self, request: PrepareReleaseInput) -> PrepareReleaseOutput:
        level = ReleaseLevel.from_str(request.level)

        current_version = self._versioning_service.current_version()
        next_version = self._versioning_service.compute_next_version(level)

        branch = ReleaseBranchName.from_version(next_version)
        tag = TagName.for_version(next_version)

        self._ensure_tag_doesnt_exist(tag)

        branch_exists = self._version_control.branch_exists(branch)

        context = ReleaseContext(
            previous_version=current_version,
            version=next_version,
            branch=branch,
            tag=tag,
            branch_exists=branch_exists,
            dry_run=request.dry_run,
        )

        await self._prepare_release_transactionally(context)
        await self._send_command(context)

        return self._make_output(context)

    def _ensure_tag_doesnt_exist(self, tag: TagName) -> None:
        if self._version_control.tag_exists(tag):
            logging.error(f"Tag {tag.value} already exists! Cannot proceed with release.")
            raise TagAlreadyExistsError(tag.value)

    def _make_output(self, context: ReleaseContext) -> PrepareReleaseOutput:
        return PrepareReleaseOutput(
            version=context.version.value,
            branch=context.branch.value,
            tag=context.tag.value,
        )

    async def _send_command(
        self,
        context: ReleaseContext,
    ) -> None:
        command = OpenPullRequestCommand(
            version=context.version.value, branch=context.branch.value, dry_run=context.dry_run
        )
        await self._message_bus.send(command)

    async def _prepare_release_transactionally(
        self,
        context: ReleaseContext,
    ) -> None:
        if context.dry_run:
            return

        async with self._transaction:
            self._global_setup()
            self._branch_handling(context)

            self._versioning_service.apply_version(context.version)

            await self._changelog_generator.generate(
                ChangelogRequest(from_version=context.previous_version.value)
            )

            self._version_control.commit_release_artifacts()

            # Note: Tag creation is handled by GitHub Actions after PR merge

    def _global_setup(self) -> None:
        self._transaction.register_step(
            ReleaseStep(
                name="checkout_main",
                undo=self._version_control.checkout_main,
            )
        )

    def _branch_handling(self, context: ReleaseContext) -> None:
        if context.branch_exists:
            self._version_control.checkout(context.branch)
        else:
            self._version_control.create_branch(context.branch)
            self._transaction.register_step(
                ReleaseStep(
                    name="delete_local_branch",
                    undo=lambda branch=context.branch: self._version_control.delete_local_branch(
                        branch
                    ),
                )
            )


