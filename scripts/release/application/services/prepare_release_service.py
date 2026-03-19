from scripts.release.application.ports.inbound import (
    PrepareReleaseInput,
    PrepareReleaseOutput,
    PrepareReleaseUseCase,
)
from scripts.release.application.ports.outbound import (
    ChangelogGenerator,
    ChangelogRequest,
    ReleaseCommandBus,
    ReleaseTransaction,
    VersionControl,
    VersioningService,
)
from scripts.release.application.workflow import ReleaseContext, ReleaseStep
from scripts.release.domain.messages import OpenPullRequestCommand
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    ReleaseLevel,
    TagName,
)


class PrepareReleaseService(PrepareReleaseUseCase):
    """Service for preparing the release synchonosly and send a command to open a PR.

    Responsibilities:
    - calculate the next version
    - create a release branch
    - instantiate tag name
    - check if the branch already exists
    - prepare a release
    - check if its a dry run to avoid modifying the repo
    - delegate to infrastructure
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

        if not context.dry_run:
            await self._send_command(context)

        return self._make_output(context)

    def _make_output(self, context: ReleaseContext) -> PrepareReleaseOutput:
        return PrepareReleaseOutput(
            version=context.version.value,
            branch=context.branch.value,
            tag=context.tag.value,
        )

    async def _send_command(self, context: ReleaseContext) -> None:
        command = OpenPullRequestCommand(
            version=context.version.value,
            branch=context.branch.value,
            dry_run=context.dry_run,
        )
        await self._message_bus.send(command)

    async def _prepare_release_transactionally(self, context: ReleaseContext) -> None:
        if context.dry_run:
            return

        async with self._transaction:
            self._transaction.register_step(
                ReleaseStep(
                    name="checkout_main",
                    undo=self._version_control.checkout_main,
                )
            )

            self._branch_handling(context)
            self._apply_version(context)
            await self._generate_changelog(context)

            self._version_control.commit_release_artifacts()
            self._push_branch(context)

    def _branch_handling(self, context: ReleaseContext) -> None:
        if context.branch_exists:
            self._version_control.checkout(context.branch)
        else:
            self._version_control.create_branch(context.branch)
            self._transaction.register_step(
                ReleaseStep(
                    name="delete_local_branch",
                    undo=lambda: self._version_control.delete_local_branch(context.branch),
                )
            )

    def _apply_version(self, context: ReleaseContext) -> None:
        self._transaction.register_step(
            ReleaseStep(
                name="rollback_version",
                undo=lambda: self._versioning_service.rollback_version(context.previous_version),
            )
        )
        self._versioning_service.apply_version(context.version)

    async def _generate_changelog(self, context: ReleaseContext) -> None:
        await self._changelog_generator.generate(
            ChangelogRequest(from_version=context.previous_version.value)
        )

    def _push_branch(self, context: ReleaseContext) -> None:
        self._transaction.register_step(
            ReleaseStep(
                name="delete_remote_branch",
                undo=lambda: self._version_control.delete_remote_branch(context.branch),
            )
        )

        self._version_control.push(context.branch)
