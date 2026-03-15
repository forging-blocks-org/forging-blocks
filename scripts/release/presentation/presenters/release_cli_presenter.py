import sys
from logging import Logger
from typing import Sequence

from scripts.release.application.errors.release_branch_exists_error import ReleaseBranchExistsError
from scripts.release.application.errors.tag_already_exists_error import TagAlreadyExistsError
from scripts.release.application.ports.inbound.prepare_release_use_case import PrepareReleaseInput
from scripts.release.infrastructure.container import Container
from scripts.release.presentation.parsers import ReleaseCliParser


class ReleaseCliPresenter:
    def __init__(self, parser: ReleaseCliParser, container: Container) -> None:
        self._parser = parser
        self._container = container
        self._logger = Logger(__name__)

    async def present(self, argv: Sequence[str] | None = None) -> None:
        try:
            self._logger.info("Parsing CLI arguments")

            parsed_input = self._parser.parse(argv)

            dry_run = not parsed_input.execute

            msg = f"Preparing release with level: {parsed_input.level}, dry_run: {dry_run}"
            self._logger.info(msg)

            service_input = PrepareReleaseInput(level=parsed_input.level, dry_run=dry_run)

            self._logger.debug(f"Service input: {service_input}")

            prepare_release_use_case = self._container.get_prepare_release_use_case()

            service_output = await prepare_release_use_case.execute(service_input)

            self._logger.info("Release preparation completed")
            self._logger.debug(f"Service output: {service_output}")

            if dry_run:
                self._logger.info("Dry run mode - no changes were made")
            else:
                self._logger.info("Release executed successfully")

        except TagAlreadyExistsError as e:
            self._handle_tag_exists_error(e)
        except ReleaseBranchExistsError as e:
            self._handle_branch_exists_error(e)
        except RuntimeError as e:
            self._handle_command_error(e)
        except Exception as e:
            self._handle_unexpected_error(e)

    def _handle_branch_exists_error(self, error: ReleaseBranchExistsError) -> None:
        """Handle the case where a release branch already exists with the same changes."""
        self._logger.error("\nRelease Failed: Branch already exists with these changes")
        self._logger.error(f"Branch '{error.branch_name}' already contains the release artifacts.")
        self._logger.error("\nTo fix this:")
        self._logger.error("   • Delete the existing release branch:")
        self._logger.error(f"     git branch -D {error.branch_name}")
        self._logger.error(f"     git push origin --delete {error.branch_name}")
        self._logger.error("   • Then run the release command again")
        self._logger.error("\n   Or if you want to continue with the existing branch:")
        self._logger.error(f"   • Push the existing branch: git push origin {error.branch_name}")
        self._logger.error("   • Open a PR manually on GitHub")
        sys.exit(1)

    def _handle_tag_exists_error(self, error: TagAlreadyExistsError) -> None:
        """Handle the case where a release tag already exists."""
        print("\nRelease Failed: Tag already exists")
        print(f"   Tag '{error}' already exists in the repository.")
        print("\nTo fix this:")
        print("   • Delete the existing tag:")
        print(f"     git tag -d {error} && git push origin --delete {error}")
        print("   • Or bump to the next version level")
        sys.exit(1)

    def _handle_command_error(self, error: RuntimeError) -> None:
        """Handle command execution failures with user-friendly messages."""
        error_msg = str(error)

        if "git commit" in error_msg and "nothing to commit" in error_msg:
            print("\nRelease Failed: Nothing to commit")
            print("   The release branch already exists with the same changes.")
            print("\nTo fix this:")
            print("   • Delete the existing release branch:")
            print("     git branch -D release/v* && git push origin --delete release/v*")
            print("   • Then run the release command again")
        elif "git commit" in error_msg:
            print("\nRelease Failed: Git commit error")
            print("   Could not commit release artifacts.")
            print("\nTo fix this:")
            print("   • Check git status: git status")
            print("   • Ensure working directory is clean")
            print("   • Check for pre-commit hook issues")
        elif "git push" in error_msg:
            print("\nRelease Failed: Git push error")
            print("   Could not push release branch to remote.")
            print("\nTo fix this:")
            print("   • Check network connection")
            print("   • Verify Git credentials are set up")
            print("   • Check if branch protection rules block push")
        elif "gh pr create" in error_msg:
            print("\nRelease Failed: Pull request creation error")
            print("   Could not create pull request.")
            print("\nTo fix this:")
            print("   • Install GitHub CLI: gh --version")
            print("   • Login to GitHub: gh auth login")
            print("   • Or create the PR manually on GitHub")
        else:
            print("\nRelease Failed: Command error")
            print(f"   {self._extract_user_friendly_message(error_msg)}")
            print("\nTo debug:")
            print("   • Check the logs above for specific command that failed")
            print("   • Run with increased verbosity for more details")

        sys.exit(1)

    def _handle_unexpected_error(self, error: Exception) -> None:
        """Handle unexpected errors."""
        print("\n Release Failed: Unexpected error")
        print(f"   {type(error).__name__}: {error}")
        print("\n This is an unexpected error. Please:")
        print("   • Check if all dependencies are installed")
        print("   • Report this issue with the error details")
        sys.exit(1)

    def _extract_user_friendly_message(self, error_msg: str) -> str:
        """Extract the most relevant part of the error message."""
        # Remove stack trace and get just the command failure
        if "Command failed:" in error_msg:
            lines = error_msg.split("\n")
            for line in lines:
                if line.strip() and not line.startswith("  "):
                    return line.strip()
        return error_msg[:200] + "..." if len(error_msg) > 200 else error_msg
