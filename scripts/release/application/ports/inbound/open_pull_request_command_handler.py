from typing import Protocol

from scripts.release.domain.messages import OpenPullRequestCommand


class OpenPullRequestCommandHandler(Protocol):
    async def handle(self, message: OpenPullRequestCommand) -> None:
        """
        Handle the OpenPullRequestCommand message.
        This method is called when a release has been prepared
        and a pull request needs to be opened.

        :param message: The OpenPullRequestCommand message to handle.

        :return: None
        """
        ...
