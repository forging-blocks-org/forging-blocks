from forging_blocks.application.ports.inbound.message_handler_port import MessageHandlerPort
from scripts.release.domain.commands import OpenPullRequestCommand


class OpenPullRequestCommandHandler(MessageHandlerPort[OpenPullRequestCommand, None]):
    """Handler for opening release pull requests.

    Responsibilities:
        - Receive an OpenPullRequestCommand.
        - Construct PR input from command data.
        - Delegate PR creation to the use case.
    """
