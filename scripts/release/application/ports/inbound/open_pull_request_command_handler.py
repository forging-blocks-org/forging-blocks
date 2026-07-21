from forging_blocks.foundation.ports import InboundPort
from scripts.release.domain.commands import OpenPullRequestCommand


class OpenPullRequestCommandHandler(InboundPort[OpenPullRequestCommand, None]):
    async def handle(self, message: OpenPullRequestCommand) -> None:
        """Handle the OpenPullRequestCommand message.
        This method is called when a release has been prepared
        and a pull request needs to be opened.

        :param message: The OpenPullRequestCommand message to handle.

        :return: None
        """
        ...
