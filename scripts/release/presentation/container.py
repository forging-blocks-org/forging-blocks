# from __future__ import annotations
#
# from scripts.release.application.services.create_release_pull_request_service import (
#     CreateReleasePullRequestService,
# )
# from scripts.release.application.services.prepare_release_service import (
#     PrepareReleaseService,
# )
# from scripts.release.infrastructure.pull_requests.github_cli_pull_request_service import (
#     GitHubCliPullRequestService,
# )
# from scripts.release.infrastructure.transactions.in_memory_release_transaction import InMemoryReleaseTransaction
# from scripts.release.infrastructure.vcs.git_version_control import GitVersionControl
# from scripts.release.infrastructure.versioning.poetry_versioning_service import (
#     PoetryVersioningService,
# )
#
#
# class Container:
#     """
#     Minimal composition root for the release automation CLI.
#
#     Notes:
#     - Keep this module free of any CLI parsing concerns.
#     - Keep it free of domain rules (those belong in domain / application).
#     """
#
#     def prepare_release_use_case(self) -> PrepareReleaseService:
#         return PrepareReleaseService(
#             versioning_service=PoetryVersioningService(),
#             version_control=GitVersionControl(),
#             transaction=InMemoryReleaseTransaction(),
#             release_event_bus=InMemo
#         )
#
#     def create_release_pull_request_use_case(self) -> CreateReleasePullRequestService:
#         return CreateReleasePullRequestService(
#             pull_request_service=GitHubCliPullRequestService(),
#         )
