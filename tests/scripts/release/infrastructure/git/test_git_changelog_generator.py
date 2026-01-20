from __future__ import annotations

from typing import Protocol

from scripts.release.infrastructure.git.git_changelog_generator import (
    GitChangelogGenerator, ChangelogRequest
)


class GitRepository(Protocol):
    def write_file(self, name: str, content: str) -> None:
        ...

    def  commit(self, message: str) -> None:
        ...

    def last_commit_message(self) -> str:
        ...


class TestGitChangelogGeneratorIntegration:
    async def test_generate_when_commits_exist_then_entries_returned(
        self,
        git_repo: GitRepository,
    ) -> None:
        # Arrange
        git_repo.write_file("file.txt", "x")
        git_repo.commit("feat: new feature")

        generator = GitChangelogGenerator()
        request = ChangelogRequest(from_version="0.0.0")

        # Act
        response = await generator.generate(request)

        # Assert
        assert any("feat: new feature" in entry for entry in response.entries)
