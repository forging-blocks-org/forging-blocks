from scripts.release.application.workflow import ReleaseContext, ReleaseStep
from scripts.release.application.errors.tag_already_exists_error import (
    TagAlreadyExistsError,
)
from scripts.release.domain.events.release_prepared_event import ReleasePreparedEvent
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
    ReleaseMessageBus,
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
        message_bus: ReleaseMessageBus,
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

        # Branch and tag always refer to the NEXT version
        branch = ReleaseBranchName.from_version(next_version)
        tag = TagName.for_version(next_version)

        # Strong idempotency guard
        self._ensure_tag_doesnt_exist(tag)

        branch_exists = self._version_control.branch_exists(branch)

        context = ReleaseContext(
            previous_version=current_version,
            version=next_version,
            branch=branch,
            tag=tag,
            branch_exists=branch_exists,
        )

        if request.dry_run:
            return self._make_output(context)

        async with self._transaction:
            # 0. Global cleanup — registered FIRST, executed LAST
            self._transaction.register_step(
                ReleaseStep(
                    name="checkout_main",
                    undo=self._version_control.checkout_main,
                )
            )

            # 1. Branch handling
            if branch_exists:
                self._version_control.checkout(branch)
            else:
                self._version_control.create_branch(branch)
                self._transaction.register_step(
                    ReleaseStep(
                        name="delete_local_branch",
                        undo=lambda b=branch: self._version_control.delete_local_branch(
                            b
                        ),
                    )
                )

            # 2. Mutations on release branch
            self._versioning_service.apply_version(next_version)

            await self._changelog_generator.generate(
                ChangelogRequest(
                    from_version=current_version.value,
                    to_version=next_version.value,
                )
            )

            # 3. Commit artifacts
            self._version_control.commit_release_artifacts()

            # 4. Tag the release commit
            self._version_control.create_tag(tag)
            self._transaction.register_step(
                ReleaseStep(
                    name="delete_tag",
                    undo=lambda t=tag: self._version_control.delete_tag(t),
                )
            )

        # Publish only after successful transaction
        await self._message_bus.publish(
            ReleasePreparedEvent(
                version=next_version.value,
                branch=branch.value,
            )
        )

        return self._make_output(context)

    def _ensure_tag_doesnt_exist(self, tag: TagName) -> None:
        if self._version_control.tag_exists(tag):
            raise TagAlreadyExistsError(tag.value)

    def _make_output(self, context: ReleaseContext) -> PrepareReleaseOutput:
        return PrepareReleaseOutput(
            version=context.version.value,
            branch=context.branch.value,
            tag=context.tag.value,
        )
