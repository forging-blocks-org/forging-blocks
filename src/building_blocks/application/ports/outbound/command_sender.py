from building_blocks.application.ports.outbound.message_bus import MessageBus
from building_blocks.domain.messages.command import Command


class CommandSender:
    """
    Asynchronous outbound port for sending commands.
    This interface defines the contract for sending commands in a CQRS
    architecture. It is designed to be implemented by command bus or
    message broker services, allowing for asynchronous command handling and
    decoupling of components.
    Perfect for:
    - Command-driven architectures
    - Decoupling domain logic from command handling
    - Implementing command sourcing patterns
    - Integrating with message brokers or command buses
    """

    def __init__(self, message_bus: MessageBus) -> None:
        self._message_bus = message_bus

    async def send(self, command: Command) -> None:
        await self._message_bus.dispatch(command)
